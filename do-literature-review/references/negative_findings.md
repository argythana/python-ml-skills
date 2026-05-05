# Negative Findings (R4)

Every literature review must include a **Negative Findings** section. The section's job is to make silent omission visible: every search that did not produce a usable citation is logged, with reason. A review with zero negative findings is a red flag and must be challenged in the self-audit.

## What goes in this section

### Sub-questions yielding no usable citation

For every sub-question from the restatement step, if it produced zero usable citations, list it explicitly:

> **SQ3**: ML papers that explicitly reconcile labels across maritime taxonomies — no peer-reviewed source found. Closest hits discuss label noise generally but do not perform reconciliation; failed R2 quote requirement.

If a sub-question yielded only metadata-only (R3) citations, that also counts as "no usable citation" for content claims and should be listed.

### Failed individual queries

A table with one row per query that did not yield a citation that survived verification:

| Source | Query string | Result | Reason rejected |
|---|---|---|---|
| arXiv | `AIS vessel classification label noise` | 11 hits | 2 already cited; rest off-topic |
| Crossref | `Statcode 5 ship type mapping` | 0 hits | No coverage |
| Semantic Scholar | `military vessel track classification fine-grained` | 4 hits | All paywalled; R3 only |

The "Query string" column must contain the actual string passed to the API. Paraphrases or summaries are not acceptable — the column exists so the user can re-run the query themselves.

### Topics deliberately excluded from search

If you decided not to search a topic that the user might expect, say so:

> Excluded: non-maritime label-noise literature — out of scope per restatement.
> Excluded: pre-2015 work on AIS clustering — superseded by post-2020 deep-learning papers.

## Why this is structural

The section is **mandatory**. Its absence is a structural defect that the self-audit must catch. With the section in place:

- Silent omission becomes loud — the reader sees the failed queries.
- The reviewer (you, in the self-audit) is forced to confront whether the success/failure ratio is plausible.
- The user can re-run the failed queries and confirm or refute the negative findings.

Without the section, "I found 5 papers" looks comprehensive even when it represents 5 hits out of 200 attempted searches that were all dropped.

## Sanity checks (run during R5 self-audit)

The self-audit table must include these counts:

- Number of sub-questions: N
- Sub-questions with zero usable citations: M
- Failed queries logged: K

If `M = 0 and K = 0`, that is the red-flag case. Either the question was very narrow and well-covered (defensible — explain), or the section is hiding failures (defect — fix). Default to suspecting the latter.

## What does not go in this section

- Speculation about papers that "should exist" but were not searched. Either search them, or do not mention them.
- Failures unrelated to literature search (network errors, tool failures). Re-run the query instead of logging the tool error.
- Papers that *did* yield a usable citation. Those go in the citation list, not here.
