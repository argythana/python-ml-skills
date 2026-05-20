---
name: uv-deps
description: >
  Use when the task is to manage dependencies in a `uv` project — either
  a single-package project (one `pyproject.toml`) or a `uv` workspace
  monorepo (multiple per-package `pyproject.toml` files plus a root
  `uv.lock`). Covers add, remove, update, sync, lock, build, export, or
  reorganize packages, dependency groups, extras, and workspace sources
  via `uv` commands rather than hand-editing `pyproject.toml`. Trigger
  for requests like 'add
  a package', 'uv sync', 'move this to dev dependencies', 'update uv
  deps', 'remove X from package Y', 'regenerate constraints.txt', or
  'build a wheel'. Do NOT use for Poetry/pip/conda/pip-tools workflows,
  manual virtualenv setup or activation, import sorting, or unrelated
  `pyproject.toml` edits such as project metadata or build config.
---

# uv dependency management

Manage dependencies in any `uv` project — single-package or workspace
monorepo. `direnv` handles environment activation, so do not create or
manually activate virtual environments.

## Detecting the project mode

Before any dependency change, determine whether the project is
**single-package** or a **workspace monorepo**. The mode changes which
flags and rules apply for the rest of the work.

Check the root `pyproject.toml` for `[tool.uv.workspace]`:

```toml
[tool.uv.workspace]
members = ["packages/*"]
```

- **Present** → workspace monorepo. The "Workspace monorepo mode"
  section applies; `--package <name>` is required on `uv add` / `uv
  remove`.
- **Absent** → single-package project. The "Single-package mode"
  section applies; `--package` does not apply.

Cross-check by counting `pyproject.toml` files in the repo:

```bash
find . -name pyproject.toml -not -path '*/.venv/*'
```

One result → single-package; multiple → workspace.

Once you have the mode, ignore the section for the other mode for the
remainder of the task. The two sets of rules don't conflict — they're
just disjoint.

## Scope

- Use `uv` commands for dependency changes rather than hand-editing
  `pyproject.toml`, unless the task explicitly requires a manual edit
  that `uv` doesn't expose (e.g. tweaking a build-system config).
- Keep changes limited to dependency-related updates: dependencies,
  groups, extras, optional features, workspace sources, and the
  resulting `uv.lock` refresh.

## Core operations (both modes)

These commands behave identically regardless of project shape. The
single difference is the optional `--package <name>` flag, which is
required in workspace mode and not applicable in single-package mode.

```bash
# Sync the venv with the lockfile
uv sync                          # single-package or workspace (active project)
uv sync --all-packages           # workspace: all members

# Refresh the lockfile without upgrading any package
uv lock

# Upgrade every dep to the latest compatible version
uv lock --upgrade

# Upgrade a single package
uv lock --upgrade-package pandas

# Show the dependency tree
uv tree

# Export resolved versions to a pip-style constraints file
uv export > constraints.txt
```

## Single-package mode

A single `pyproject.toml` at the repo root, no `[tool.uv.workspace]`,
one `uv.lock` covering that one project.

### Adding and removing dependencies

```bash
# Add a runtime dependency
uv add pandas

# Add with a version constraint
uv add 'pandas>=2.0,<3.0'

# Add multiple at once
uv add pandas numpy scikit-learn

# Remove a dependency
uv remove pandas
```

No `--package` flag — there is only one project.

### Dev / tooling dependencies (PEP 735)

Use **PEP 735 dependency groups** via `uv add --group <name>`. Groups
live under `[dependency-groups]` in `pyproject.toml` and are the
ecosystem's direction for non-runtime tooling — prefer them over
`[project.optional-dependencies]` for anything downstream users don't
need at install time.

```bash
# Add a dev tool to the default `dev` group
uv add --dev pytest              # shorthand for --group dev

# Add to a named group
uv add --group docs sphinx mkdocs
uv add --group typecheck mypy
```

Resulting `pyproject.toml`:

```toml
[dependency-groups]
dev = ["pytest>=8.0"]
docs = ["sphinx", "mkdocs"]
typecheck = ["mypy"]
```

`uv sync` includes the `dev` group by default. Sync other groups
explicitly with `--group <name>`, or all of them with `--all-groups`.

### Optional runtime extras

Use `[project.optional-dependencies]` (extras) only for *runtime*
features your *users* opt into at install time:

```bash
uv add --optional db psycopg2
```

That writes:

```toml
[project.optional-dependencies]
db = ["psycopg2"]
```

Install with the extra:

```bash
uv sync --extra db
```

### Heuristic: groups vs extras

- **Group** when the dependency supports *your* workflow (testing,
  linting, type checking, docs, dev tools). Downstream installers
  never need it.
- **Extra** when the dependency is part of an optional *runtime*
  feature of your package that downstream users select at install
  time.

## Workspace monorepo mode

Multiple `pyproject.toml` files (one per workspace member) under a root
`pyproject.toml` that declares `[tool.uv.workspace]`. One root
`uv.lock` covers the whole workspace.

### Workspace rules

- **Per-package declarations:** a dependency must be declared in the
  `pyproject.toml` of *every* package that directly imports it. Do not
  rely on transitive availability from another workspace member.
- **Root `pyproject.toml` is for workspace-level tooling only** (e.g.
  `pytest`, `ruff`, `mypy`). Do not add application libraries such as
  `pandas` or `numpy` to the root `pyproject.toml`.
- **Single lockfile:** the root `uv.lock` is the single source of truth
  for resolved versions across the whole workspace. Commit it.
- **Shared constraints must match:** if you pin a shared dependency
  (e.g. `pandas<2.0`) in one package, apply the same constraint in
  every other `pyproject.toml` that depends on it. `uv` refuses to
  resolve conflicting constraints.
- **Internal packages use workspace sources:** when one workspace
  member depends on another, declare the dependency normally and add a
  `[tool.uv.sources]` entry marking it as `workspace = true`.
- **`requires-python`:** declare it in every package's
  `pyproject.toml`; keep the value consistent across packages.

### Adding dependencies

Always target a specific workspace member with `--package <name>`, run
from the repository root:

```bash
# Add a runtime dep to a specific workspace package
uv add pandas --package team-ds-library

# Add multiple
uv add pandas numpy scikit-learn --package team-ds-library

# Add with a version constraint (apply the SAME constraint in every
# other package that also depends on it)
uv add 'pandas<2.0' --package team-ds-library

# Add an internal workspace package as a dependency
uv add team-utils --package team-ds-library
# then ensure the per-package pyproject.toml has:
#   [tool.uv.sources]
#   team-utils = { workspace = true }
```

### Dev / tooling dependencies

Workspace-wide tooling lives in the root `pyproject.toml` under
`[dependency-groups]`. Do not duplicate per-package.

```bash
# Add to the default dev group (root pyproject.toml)
uv add --dev pytest
uv add --dev ruff mypy

# Add to a named group
uv add --group docs sphinx
```

### Optional runtime extras

Live on the target package, not at the workspace root:

```bash
uv add --optional db psycopg2 --package team-ds-library
```

### Dependency classification (workspace)

| Category                           | Where to declare                                          | Examples                              |
|------------------------------------|-----------------------------------------------------------|---------------------------------------|
| Direct imports in a package        | that package's `pyproject.toml`                           | `pandas`, `numpy`, `sqlalchemy`       |
| Internal workspace package         | that package's `pyproject.toml` + `[tool.uv.sources]`     | `team-utils`, `team-ds-library`       |
| Testing / linting / type checking  | root `pyproject.toml` group                               | `pytest`, `ruff`, `mypy`              |
| Type stubs for a direct import     | same package as the import                                | `types-requests`, `pandas-stubs`      |
| Docs tooling                       | root `pyproject.toml` group                               | `sphinx`, `mkdocs`                    |
| Optional runtime features          | target package, as an extra                               | `psycopg2` under a `db` extra         |

### Workspace-only common operations

```bash
# Sync every workspace member
uv sync --all-packages

# Remove a dep from a specific package
uv remove pandas --package team-ds-library

# Tree for one package
uv tree --package team-ds-library

# Build a wheel for a specific member
uv build --package team-ds-library

# Export resolved versions for CI/Docker
uv export --all-packages --all-extras > constraints.txt
```

## Environment activation (direnv) — both modes

- `direnv` activates the project's virtual environment automatically
  on `cd` into the repository. Do not run `python -m venv`, `source
  .venv/bin/activate`, or `conda activate` as part of a dependency
  task.
- `uv` itself must be installed *outside* any virtual environment. If
  the user reports `uv: command not found`, point them to the official
  installer (`curl -LsSf https://astral.sh/uv/install.sh | sh`); do not
  try to install `uv` into the project's `.venv`.
- If `direnv` appears to be inactive (commands run against the system
  Python), surface that to the user rather than manually activating
  the venv.

## Procedure

1. **Detect the project mode** by checking the root `pyproject.toml`
   for `[tool.uv.workspace]` (see "Detecting the project mode" above). The mode you find decides
   which section of this skill applies for the rest of the task —
   ignore the other.
2. **Classify the dependency**:
   - Runtime dep used in code → main `[project.dependencies]`
     (single-package) or the target package's `pyproject.toml`
     (workspace).
   - Dev / tooling (pytest, ruff, mypy, sphinx, …) →
     `[dependency-groups]` via `--group <name>` or `--dev`. In
     workspace mode this lives in the root `pyproject.toml`.
   - Optional runtime feature for downstream users → extras via
     `--optional`.
3. **If workspace mode**, identify the target workspace member and
   pass `--package <name>` to every `uv add` / `uv remove`. When
   pinning a shared dep, apply the same constraint in every other
   package that depends on it.
4. **Run `uv` from the repository root.** `uv` updates `uv.lock`
   automatically; stop there — do not manually re-sync unless the
   user asks.
5. **For new internal workspace dependencies (workspace mode only)**,
   confirm the per-package `[tool.uv.sources]` entry marks the dep as
   `workspace = true`.
6. **If the task involves CI/Docker** (constraints file, wheels, GPU
   builds), regenerate the artifacts via the documented commands
   (`uv export`, `uv build`) rather than hand-editing.
