"""Small benchmark comparing subprocess (CLI) invocation vs in-process analysis.

Usage:
    python docs/benchmarks/benchmark.py

What it does:
- Generates a sample CSV dataset in /tmp
- Attempts to run the real `column_dist.py` CLI from the repo as a subprocess.
  If that fails, it falls back to `mock_cli.py` bundled with this benchmark.
- Runs an equivalent in-process analysis (same CSV, using csv module) to simulate
  an MCP-style in-process handler.
- Prints timing statistics and estimated token sizes for outputs.

Notes:
- This benchmark focuses on measuring subprocess startup + runtime overhead
  vs in-process execution. It does not exercise the full MCP protocol.
- Token estimates use a simple bytes->tokens heuristic: tokens ~= bytes / 4.
"""

from __future__ import annotations

import csv
import json
import random
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CLI_SCRIPT = ROOT / "packages" / "skill-eda" / "src" / "skill_eda" / "column_dist.py"
MOCK_CLI = Path(__file__).resolve().parent / "mock_cli.py"

SAMPLE_ROWS = 100_000
CATEGORIES = ["completed", "pending", "cancelled", "refunded", "processing"]
ITERATIONS = 3


def generate_sample_csv(path: Path, rows: int = SAMPLE_ROWS) -> None:
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "status"])
        for i in range(rows):
            status = random.choices(CATEGORIES, weights=[0.8, 0.1, 0.05, 0.04, 0.01])[0]  # noqa: S311
            writer.writerow([i, status])


def in_process_analysis(path: Path, column: str = "status") -> str:
    # Simple in-process distribution (simulates MCP handler returning JSON)
    counts = Counter()
    total = 0
    nulls = 0
    with path.open("r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            val = row.get(column)
            if val is None or val == "":
                nulls += 1
            else:
                counts[val] += 1
    rows = []
    cumulative = 0.0
    for value, cnt in counts.most_common():
        pct = cnt / total * 100
        cumulative += pct
        rows.append({"value": value, "count": cnt, "percentage": pct, "cumulative": cumulative})

    result = {
        "summary": {
            "total": total,
            "nulls": nulls,
            "non_null": total - nulls,
            "unique": len(counts),
        },
        "distribution": rows,
    }
    return json.dumps(result)


def run_subprocess_cli(script_path: Path, source: Path, column: str = "status") -> tuple[int, str]:
    # Validate inputs: script_path must be one of our known safe scripts
    if script_path not in (CLI_SCRIPT, MOCK_CLI):
        raise ValueError(f"Untrusted script path: {script_path}")
    if not source.exists():
        raise ValueError(f"Source file does not exist: {source}")
    cmd = [sys.executable, str(script_path), "--source", str(source), "--column", column]
    start = time.perf_counter()
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)  # noqa: S603
    end = time.perf_counter()
    duration = end - start
    output = proc.stdout if proc.returncode == 0 else (proc.stdout + "\n" + proc.stderr)
    return int(duration * 1000), output


def estimate_tokens(text: str) -> int:
    # heuristic: 1 token ~= 4 bytes
    return max(1, len(text.encode("utf-8")) // 4)


def main() -> int:
    tmp = Path(tempfile.gettempdir()) / f"eda_bench_{int(time.time())}.csv"
    print("Generating sample CSV:", tmp)
    generate_sample_csv(tmp)

    # Try real CLI; if it fails, use mock CLI supplied here
    cli_to_use = CLI_SCRIPT if CLI_SCRIPT.exists() else MOCK_CLI
    if not cli_to_use.exists():
        print("No CLI script available; ensure repo's skill-eda is present or mock_cli.py exists.")
        return 2

    print(f"Using CLI: {cli_to_use}")

    # Warm up in-process once
    print("Warming up in-process analysis...")
    _ = in_process_analysis(tmp)

    # Benchmark subprocess CLI
    cli_times = []
    cli_token_estimates = []
    for i in range(ITERATIONS):
        ms, out = run_subprocess_cli(cli_to_use, tmp)
        cli_times.append(ms)
        cli_token_estimates.append(estimate_tokens(out))
        print(f"CLI run {i + 1}: {ms} ms, approx tokens: {cli_token_estimates[-1]}")

    # Benchmark in-process (simulated MCP handler)
    ip_times = []
    ip_token_estimates = []
    for i in range(ITERATIONS):
        start = time.perf_counter()
        out = in_process_analysis(tmp)
        end = time.perf_counter()
        ms = int((end - start) * 1000)
        ip_times.append(ms)
        ip_token_estimates.append(estimate_tokens(out))
        print(f"In-process run {i + 1}: {ms} ms, approx tokens: {ip_token_estimates[-1]}")

    print("\nSummary (median over runs):")
    cli_med = sorted(cli_times)[len(cli_times) // 2]
    ip_med = sorted(ip_times)[len(ip_times) // 2]
    cli_tok = sorted(cli_token_estimates)[len(cli_token_estimates) // 2]
    ip_tok = sorted(ip_token_estimates)[len(ip_token_estimates) // 2]

    print(f"CLI median time: {cli_med} ms")
    print(f"In-process median time: {ip_med} ms")
    print(f"CLI median estimated tokens: {cli_tok}")
    print(f"In-process median estimated tokens: {ip_tok}")

    print("\nInterpretation:")
    print("- The CLI measurement includes subprocess startup overhead and full human-readable formatting.")
    print("- The in-process run simulates MCP-style compact JSON responses and avoids process startup.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
