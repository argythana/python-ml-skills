---
name: tutorial-expand
description: >
  Use when expanding, annotating, rewriting, or drafting a section or
  whole notebook of an official tutorial for a Python data/ML library
  (e.g. scikit-learn, PyTorch, pandas, matplotlib, NumPy, SciPy,
  Plotly) so it is friendlier for beginner data scientists and CS
  students. Trigger on prompts like "expand this scikit-learn
  section", "explain this pandas concept better", "make this PyTorch
  notebook beginner-friendly", or "why does this feature exist". If
  the target notebook or cell is unclear, ask after routing. Do NOT
  use for general Python tutorial writing unrelated to data/ML
  libraries (Django, Flask, application code), editing the upstream
  library itself, non-tutorial docs (`README.md`, `CLAUDE.md`), or
  non-teaching notebook changes (file moves, dependency bumps,
  formatting, kernel metadata). If a library-specific tutorial-expand
  skill is installed (e.g. `mlflow-tutorial-expand`), prefer that. For
  deps use `uv-deps`; for staging use `git-staging`; for messages use
  `commit-message`.
---

# Tutorial expand

Editorial skill for adapting an official tutorial of a Python data or
ML library into a clearer, beginner-friendly version. The expansion
stays recognizable as the original tutorial — wrap upstream cells
with prerequisites, terminology, motivation, and "what changed in
version X" notes rather than rewriting them.

## Audience

Researchers, data scientists, and CS students who already know Python
and are working with the specific target library for the first time.
Do not presuppose ML knowledge unless the library itself is an ML
library (PyTorch, scikit-learn, …); a pandas or matplotlib reader may
be data-curious without an ML background. Assume zero library-specific
knowledge; do not assume production deployment experience.

## Editorial principles

Follow these in order of priority. If a draft violates one, prefer
trimming over justifying.

### 1. Lead with the problem, not the API

For every library feature, the expansion answers **why** before **how**:

- What goes wrong without this feature? (lost experiments, broken
  pipelines, misleading defaults, silent data corruption, performance
  cliffs.)
- What does it replace in the reader's current workflow? (a
  spreadsheet, a NumPy loop, copy-paste, "ask a colleague".)
- What workflow concern does it serve? — reproducibility, correctness,
  performance, observability, collaboration, governance.

Only after the problem is named, show the API call.

### 2. Define terminology once, concisely

Define library jargon the first time it appears. Prefer:

- a one-sentence definition, or
- a compact table when several related terms appear together
  (e.g. `Series` vs `DataFrame` vs `Index` in pandas; `Tensor` vs
  `Module` vs `Optimizer` in PyTorch; `Figure` vs `Axes` vs `Artist`
  in matplotlib).

Do not redefine the same term in every section. Do not write a
glossary appendix — define terms where they are first used.

### 3. Add examples only when they teach something new

A second example must contrast with the first: a different parameter,
an error case, an alternate API path, a contrasting result.
Variations that only relabel inputs belong on the cutting-room floor.

### 4. Keep notebooks short

If an expansion pushes a notebook past one focused topic, split into
a new lettered notebook (`a_`, `b_`, `c_`, …) rather than letting one
notebook sprawl. Each notebook should be readable in one sitting.

### 5. Surface library version drift

Most data/ML libraries change defaults, deprecate APIs, or shift the
recommended pattern between major versions. When a reader following
older blog posts or pre-current-version tutorials would be misled, add
a short "what changed in version X" note. Do not write a full
version-history dump — only flag changes that affect the current step.

### 6. Annotate the upstream relationship with inline bold callouts

When an addition relates to upstream content — correcting,
supplementing, or deliberately diverging from it — open the paragraph
with one of four **inline bold callouts**. Do not use them as heading
prefixes. A paragraph can carry at most one label; pick the one that
most accurately names the relationship.

| Label | When to use | Example |
|---|---|---|
| `**Bug in upstream tutorial:**` | Upstream code or claim is factually wrong or no longer runs (deprecated API, removed kwarg, incorrect statement). | scikit-learn's `LogisticRegression(multi_class="auto")` was removed in 1.7; upstream's copy-pasted code raises `TypeError`. |
| `**Stale in upstream tutorial:**` | Upstream is out of date but not broken: defaults shifted in a new version, help text references retired behaviour, recommended-but-not-yet-default practices. | pandas `copy_on_write` became the only behaviour in 3.0; upstream still discusses the chained-assignment caveat as a live concern. |
| `**Missing from upstream tutorial:**` | Upstream skips a prerequisite the reader needs for the code to run at all. The upstream code is fine *if* you do this first. | A matplotlib tutorial uses `%matplotlib inline` without explaining that the magic is what makes plots display inline in Jupyter (and is unnecessary in scripts). |
| `**Diverges from upstream tutorial:**` | Upstream is fine, but this repo deliberately does it differently as a house policy. Name the policy briefly so the reader does not infer upstream is wrong. | Upstream uses `pip install pandas`; this repo uses `uv add pandas` because `pyproject.toml` + `uv.lock` are the single source of truth. |

Standalone topics — additions that have no upstream counterpart at all
(e.g. a clarification of a widely-misreported library claim, or a deep
dive on a topic upstream doesn't cover) — get a plain `## <Topic>`
heading with no callout. Labeling them anything is performative.

Do not rewrite upstream prose. Leave the original markdown cells
recognizable and add new cells around them.

## House patterns

These patterns generalize across libraries and should be reused when
they fit:

- **Comparison tables** for parallel concepts (e.g. `loc` vs `iloc` vs
  `at` in pandas; `nn.Module.train()` vs `eval()` mode in PyTorch;
  pyplot vs object-oriented API in matplotlib).
- **"What changed in version X"** callouts when defaults shifted or
  APIs moved. Most data/ML libraries have meaningful major-version
  churn (pandas 1→2→3, scikit-learn 1.x deprecations, PyTorch
  pre-2.0 → post-2.0 compile/dynamo, NumPy 2.0 dtype shifts).
- **"Inspecting it (optional)"** subsections with a one-liner that
  lets the reader peek at state (`df.dtypes`, `tensor.shape`,
  `fig.axes`, `sklearn.__version__`) — useful for learning, optional
  in the flow.
- **"Overriding it"** subsections showing the keyword, env var, or
  config option to customise the default, with one realistic
  alternative — not an exhaustive flag listing.
- **"For local learning, leaving the defaults alone is the right call"**
  — give the reader permission to skip configuration rabbit holes.

## Workflow

1. Identify the target library and the section or concept to expand.
   Read the surrounding cells so the addition fits the flow.
2. Decide the upstream relationship of the addition (see principle 6):
   - **bug** → inline `**Bug in upstream tutorial:**` callout
   - **stale** → inline `**Stale in upstream tutorial:**` callout
   - **missing** → inline `**Missing from upstream tutorial:**` callout
   - **diverges** → inline `**Diverges from upstream tutorial:**`
     callout
   - **standalone topic** (no upstream counterpart) → plain
     `## <Topic>` heading, no callout
3. Draft the expansion in this order:
   - **Problem** — what breaks without it.
   - **Concept / definition** — one paragraph or table.
   - **Default behaviour in the target library's current version** —
     the happy path.
   - **What changed / version note** — only if a stale tutorial would
     mislead the reader.
   - **Optional inspect / override** — one example each, not more.
4. Re-read the draft and cut anything that does not pass the "does
   this add value the reader cannot get from the official docs?" test.
5. Confirm the notebook still reads in one sitting. If not, propose a
   split into another lettered notebook.

## Anti-patterns

Stop and rewrite if the draft does any of these:

- Opens with an API call before establishing the problem.
- Repeats a definition already given earlier in the notebook.
- Includes a second example that does not contrast with the first.
- Treats the library as a black box ("just call this") without
  naming the workflow concern.
- Adds a "history of the library" paragraph unrelated to the current
  step.
- Inlines reference-style content that belongs in the official docs
  (full API tables, exhaustive parameter listings).
- Rewrites or paraphrases upstream cells instead of wrapping them.
- Edits notebook JSON metadata (kernelspec, execution counts,
  formatting) under the guise of "expansion". Those are not teaching
  changes and do not belong to this skill.
- Stacks multiple upstream-relationship callouts on one paragraph.
  Pick the single label that most accurately names the relationship.

## Forking this into a library-specific sibling

This skill is intentionally written as a **template**: the editorial
principles, the four-callout convention, the anti-patterns, and the
workflow generalize across Python data/ML libraries. To create a
dedicated skill for a single library (e.g. `pandas-tutorial-expand`,
`pytorch-tutorial-expand`), hand-fork this `SKILL.md` and customize
five places. Existing example: `mlflow-tutorial-expand` in the
`teach-mlflow` repo, which predates this generic skill and follows
the same pattern.

### Five customization points

1. **`name` frontmatter** — set to `<library>-tutorial-expand`
   (lowercase, hyphenated).
2. **`description` frontmatter** — narrow the library scope from the
   open list to the one target library. Tighten the path scope to
   wherever that library's tutorials live in the target repo (e.g.
   `src/official_tutorials/`). Drop the deferral clause (the one that
   defers to library-specific siblings) since the new skill *is* the
   library-specific sibling. Adjust the handoff list if the target
   repo has companion skills the new sibling should reference.
3. **Audience section** — narrow to the readers actually likely to use
   the target library. An MLflow tutorial reader probably has ML
   literacy; a pandas tutorial reader may not.
4. **Principle 6 example table** — replace the four illustrative rows
   (`multi_class`, `copy_on_write`, `%matplotlib inline`, `pip` vs
   `uv`) with actual library-specific bug / stale / missing-from /
   diverges cases that anchor in the target tutorial repo. The MLflow
   sibling uses the hardcoded `run_id` placeholder as its Bug example
   and the stale `./mlruns` help-text as its Stale example, both real
   callouts in the repo's notebooks.
5. **House patterns section** — replace the cross-library examples
   with the library's actual recurring patterns. For MLflow this is
   the three-store table and the "what changed in MLflow 3" callout
   shape. For pandas it might be `loc` vs `iloc` vs `at`, the
   chained-assignment / `SettingWithCopyWarning` discussion, or "what
   changed in pandas 2.0 / 3.0". For PyTorch it might be
   `nn.Module.train()` vs `eval()` mode tables and device-placement
   patterns.

### What to keep verbatim

- Editorial principles 1–4 (problem-first, define-once,
  contrast-examples, keep-short) — library-agnostic.
- The four-callout convention itself: the labels, the rule that they
  go inline-bold rather than as heading prefixes, the "standalone
  topic = plain heading" rule. This is the family-wide convention.
- The anti-patterns list (possibly add library-specific ones, but
  don't drop the shared ones).
- The five-step workflow shape.

### When NOT to fork

- One-off cross-library work — this generic skill is enough.
- A library you teach occasionally rather than systematically.
- A library that doesn't have a meaningful "official tutorial" to
  expand from. The whole pattern depends on upstream content to wrap.

### After forking

Run `skill-tighten` on the new sibling to audit its description and
trigger phrases, then `skill-boundary-review` against this generic
skill plus any other siblings, to catch routing overlap before
installing.

## Out of scope

- Editing the upstream library's source code or filing issues against
  it.
- Tutorials for things outside the Python data/ML library scope (web
  frameworks, application code, deployment infrastructure, language
  features alone).
- Adding dependencies (use `uv-deps`).
- Staging and committing the resulting edits (use `git-staging` and
  `commit-message`).
- Setting up CI, deployment, or non-teaching infrastructure.
- Tutorial expansion for libraries that have a dedicated
  `<library>-tutorial-expand` skill installed; defer to that skill,
  which can encode library-specific idioms and conventions this
  generic skill cannot.
