---
name: code-review-loop
description: >
  Use this skill when the user wants an iterative `code-review` loop over
  Python changes: review a Python diff, PR, branch, or commit range with
  `code-review`, fix the actionable Critical, High, and Moderate findings, run
  the relevant checks
  and tests, and repeat until 5 consecutive clean PASS reviews,
  `insufficient evidence`, or max cycles. Trigger on "run code-review until
  clean", "keep reviewing and fixing this Python PR until it passes", or "fix
  the code-review findings and rerun review until acceptable". If the target
  repo, diff, branch, commit, or commit range is referenced but unavailable,
  ask after routing. Do NOT use for a single review-only pass; use
  `code-review`. Do NOT use for pytest-suite-specific audit loops; use
  `pytest-suite-review-loop`. Do NOT use for implementing a task against
  Acceptance Criteria; use `task-implementation-loop`. Do NOT use for
  non-Python code, dependency-only changes, or writing new features from
  scratch.
---

# Python code review loop

Run repeated strict `code-review` passes, fixes, and verification over a Python
change until the reviewed scope reaches 5 consecutive clean PASS reviews.

## Boundaries

Use this skill only when the main task explicitly combines all of these:

- `code-review`-style review of Python changes (diff, PR, branch, commit, or
  commit range)
- fixing those actionable review findings
- rerunning review and verification until a terminal stopping condition

Use `code-review` instead for a single review-only pass with no fix-and-rerun
loop.

Use `pytest-suite-review-loop` instead when the loop is specifically about
pytest tests, fixtures, or pytest infrastructure rather than general Python
change quality.

Use `task-implementation-loop` instead when the loop implements a task against
explicit Acceptance Criteria from a task spec or tracker item, rather than
driving a code-review quality verdict.

Review only Python code, as in `code-review`. Do not use this skill for
non-Python code, dependency-only changes, or authoring brand-new features from
requirements.

If the target repo, diff, branch, commit, or commit range is missing, ask for
the missing input after routing.

## Definitions

- Actionable finding: any `Critical`, `High`, or `Moderate` finding from
  `code-review`. `Low` findings are reported but do not block convergence and do
  not reset the clean-review count.
- Production-code issue: an implementation bug surfaced during review or while
  fixing findings that must be fixed for the in-scope findings or required
  verification to be correct.
- Clean review: `code-review` returns `Status: PASS` with zero actionable
  (`Critical`/`High`/`Moderate`) findings.
- Insufficient evidence: the reviewer cannot determine correctness from the
  available files, diff, tests, or surrounding code.
- Required verification: the `code-review` automated checks (`ruff`,
  `vulture`, `mypy` on the changed files) plus the relevant targeted tests for
  the changed code, plus the repository's canonical aggregate verification
  command when one is discoverable. Any selected verification must pass before
  any commit.

## Verification selection

Do not assume `poe check` exists.

Select the aggregate verification command from the most authoritative available
source:

- explicit user or task instructions
- repository docs or contributor instructions
- configured task runners such as Poe, Make, Just, Tox, Nox, Hatch, noxfile,
  `pyproject.toml` scripts, or `pre-commit`
- CI configuration when it clearly maps to a local command

Prefer a single canonical command such as `poe check`, `make check`,
`just check`, `tox`, `nox`, or `pre-commit run --all-files` when the repository
defines one. If no aggregate command is discoverable, run the `code-review`
automated checks plus the relevant targeted tests, and report that no
repository-level verification command was found. Do not invent a project-wide
command.

## Git index discipline

Before starting the loop, check repository state:

- Confirm the target is inside a git worktree. If it is not, stop unless the
  user explicitly authorizes running without git index guarantees.
- Record the pre-loop staged baseline with `git diff --cached --name-only` and
  enough staged diff detail to distinguish existing index work from loop-owned
  changes.
- Record the pre-loop unstaged and untracked baseline with `git status
  --short`, `git diff --name-only`, and `git ls-files --others
  --exclude-standard`.
- Accept existing staged changes. Treat them as part of the reviewed baseline
  when they match the requested review scope. Do not require a clean index
  before starting this loop.
- If existing staged changes are unrelated to the requested review scope or make
  the review target ambiguous, stop and ask how to scope the loop instead of
  silently mixing unrelated staged work.
- Do not unstage, discard, or rewrite existing staged work unless the user
  explicitly asks.

When the loop reaches any terminal outcome:

- Stage the file changes made by the loop before the terminal notification and
  final response.
- Preserve the pre-loop staged baseline. The final index may contain both the
  original staged changes and loop-owned changes that build on them.
- Stage only the loop's own new paths or hunks beyond the recorded baseline.
  Do not stage pre-existing unstaged or untracked user work.
- If a file contains both baseline user changes and loop changes, stage only
  the loop's hunks when they can be identified with confidence. If they cannot
  be separated safely, leave the file partly or fully unstaged and report the
  blocker.
- After staging, verify the staged diff contains the pre-loop staged baseline
  plus only loop-owned additions. If unrelated changes were staged accidentally,
  unstage those changes before the final response.

## State

Initialize:

- `consecutive_clean_reviews = 0`
- `review_cycles = 0`
- `max_review_cycles = 15`, unless the user gives a different limit
- `reviewed_target` as the current working tree, staged diff, branch, commit,
  or commit range being reviewed
- `pre_loop_staged_baseline` as the git index state recorded before review or
  fix work starts
- `pre_loop_worktree_baseline` as the unstaged and untracked git state recorded
  before review or fix work starts
- `loop_owned_changes` as the paths and hunks created or modified by the loop

If the reviewed target is ambiguous, resolve it from the user's request and
local repository state before starting the loop. Do not silently mix unrelated
worktree changes into the reviewed target.

## Loop

Do not start more than `max_review_cycles` review passes.

For each cycle:

1. Increment `review_cycles`.
2. Run `code-review` on `reviewed_target`.
   - Apply the `code-review` checklists (architecture, security, quality,
     testing, documentation, deployment, consistency).
   - Expand inspection radius as needed for callers, helpers, and nearby
     production code.
   - Require findings to be evidence-based and tied to concrete files and
     lines.
   - Require the exact `Status` and severity contract from `code-review`.
3. If the result is `insufficient evidence`, stop and report the missing
   evidence.
4. If there are any actionable findings (`Critical`, `High`, or `Moderate`),
   or `Status` is `BLOCKED` or `NEEDS_WORK`:
   - Fix the actionable findings, highest severity first.
   - If the review or fixes reveal production-code issues, fix those too.
   - Run required verification.
   - If committing fixes, commit only after verification passes.
   - If fixes were committed, update `reviewed_target` to the latest commit or
     commit range.
   - If fixes were not committed, update `reviewed_target` to the current
     working tree.
   - Reset `consecutive_clean_reviews = 0`.
   - Continue to the next cycle.
5. If `Status` is `PASS` with no actionable findings:
   - Increment `consecutive_clean_reviews`.
   - Record any `Low` findings for the final report, but do not fix them in the
     loop unless the user asks; they do not reset the clean count.
   - If `consecutive_clean_reviews < 5`, continue to the next cycle.

Before declaring terminal success, required verification must have passed since
the latest change. If it has not, run the `code-review` automated checks plus
the relevant targeted tests, plus the selected aggregate verification command
when one was discovered. If verification fails for an in-scope issue, fix it,
reset `consecutive_clean_reviews = 0`, update `reviewed_target`, and continue.
If verification cannot be judged from available evidence, stop as
`insufficient evidence`.

If the loop reaches `max_review_cycles` without 5 consecutive clean reviews,
stop and report the remaining findings or source of churn.

## Notifications

The review loop owns notifications because it owns cycle count, clean review
count, verification status, commit status, and terminal outcome.

Use `agent-notify` for workflow notifications. Do not call raw backend
notifiers directly.

Send exactly one terminal notification after the loop stops. Pass each
notification line as a separate `agent-notify` argument: line 1 is
`code-review: STATUS`, and line 2 is the concise details. Do not add a
`skillz:` prefix.

If the user explicitly asks for per-round notifications, send exactly one
`agent-notify` notification after each review cycle, including cycle count,
status, clean-review count, and whether fixes or verification ran.

Use simple quoted arguments only. Do not use ANSI-C `$'...\n...'` quoting,
heredocs, command substitution, pipes, `&&`, `||`, command separators such as
`;`, or shell variable expansion for notification commands; those shell
features can trigger sandbox approval when a direct `agent-notify` invocation
would not. Keep notification text itself free of shell control characters; use
commas or plain words in detail lines.

If `agent-notify` fails because of sandboxed network access or notifier access,
rerun the same direct invocation with escalation. If `agent-notify` still
fails, report that notification could not be sent in the final response.

Examples:

```sh
agent-notify 'code-review: round 4/15 NEEDS_WORK' 'fixed 2 High findings, clean reviews reset'
agent-notify 'code-review: round 7/15 PASS' 'clean reviews 1/5, verification pending'
agent-notify 'code-review: CONVERGED' 'clean reviews 5/5, cycles 11/15'
agent-notify 'code-review: INSUFFICIENT_EVIDENCE' 'missing surrounding production code, cycles 2/15'
agent-notify 'code-review: MAX_CYCLES' 'remaining High findings, cycles 15/15'
```

Do not send per-round notifications unless the user explicitly asks for them.

## Final response

Report:

- terminal status
- review cycles used
- consecutive clean reviews reached
- fixes made, grouped by severity
- any `Low` findings left unaddressed by design
- verification commands and results
- staged loop-owned paths or hunks, including any files left unstaged because
  loop changes could not be separated from pre-existing user work
- commits made, if any
- remaining findings or missing evidence, if the loop did not converge
