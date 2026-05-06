# Self-Audit Table (R5)

Before returning the review, emit the Self-Audit Table. One row per citation, one column per rule, each cell `PASS` / `FAIL` / `N/A` with a one-line reason. Compute the table by **re-reading your own output**, not by self-report.

This is the rule that closes the loop. The other rules (R1, R2, R3, R4, R6) define what a valid citation looks like; R5 forces you to verify that the citations you actually emitted satisfy them.

## Required table

```
| Citation | R1a metadata API call | R1b full-text retrieval | R2 verbatim quote ≥25w + locator | R3 paywall handled | R6 authors copied from API |
|----------|------------------------|--------------------------|----------------------------------|---------------------|------------------------------|
| C1       | PASS — Crossref JSON pasted | PASS — PDF fetched     | PASS — § 4.2, 31 words           | N/A — full text retrieved | PASS — Helber matches Crossref |
| C2       | PASS — catalog page noted   | FAIL — full text 403   | N/A — metadata-only              | PASS — downgraded, claim_supported=NONE | N/A — institutional author |
```

## Per-cell semantics

### R1a (metadata API call)

- **PASS** — Crossref or arXiv response is pasted in the citation's verification block, contains author/title/date/DOI fields.
- **FAIL** — no API response in the verification block, or the response is paraphrased/summarized rather than pasted.

A FAIL on R1a means the citation must be removed entirely. There is no metadata-only fallback for an unverified citation.

### R1b (full-text retrieval)

- **PASS** — `retrieval_method` and `retrieval_url_or_path` are filled, retrieval actually returned content.
- **FAIL** — retrieval did not happen, or returned only an abstract / paywall splash. Apply R3 downgrade or remove.

A FAIL on R1b is acceptable **only if** R3 is also PASS (citation is downgraded to metadata-only).

### R2 (verbatim quote)

- **PASS** — quote of ≥ 25 words present, locator filled, quote entails `claim_supported`.
- **FAIL** — quote shorter than 25 words, no locator, or quote does not actually entail the claim.
- **N/A** — citation is metadata-only per R3; quote is correctly absent.

### R3 (paywall handled)

- **PASS** — citation is metadata-only AND `claim_supported = "NONE — content not verified"` AND warning line present.
- **FAIL** — citation is metadata-only but makes a content claim (this is the failure mode R3 exists to block).
- **N/A** — citation has full text; R3 not applicable.

### R6 (authors from API)

- **PASS** — first author in citation matches first author in pasted API response, byte-for-byte.
- **FAIL** — author name in citation differs from API response, or no API response was pasted.
- **N/A** — institutional/corporate author with no individual names (e.g. "Food and Agriculture Organization of the United Nations").

## Negative Findings sanity check

After the per-citation table, include:

- Number of sub-questions: N
- Sub-questions with zero usable citations: M
- Failed queries logged: K
- Plausibility statement: if `M = 0 and K = 0`, explain why. This is a red flag that often hides silent omission.

## Final disposition block

```
- Citations emitted: N
- Citations downgraded to metadata-only: M
- Citations dropped during audit: K
- All FAIL cells resolved: YES — review may be returned | NO — do not return until resolved
```

If any FAIL cell remains unresolved, **do not return the review**. Either remove the offending citation, downgrade it per R3, or fix the underlying gap (rerun retrieval, find the quote, redo metadata lookup).

## Why "re-read the output" matters

The audit is computed from the output, not from memory of what you intended. This catches:

- Citations where the verification block was forgotten.
- Quotes that were drafted at < 25 words.
- Author names that drifted between draft and final.
- Metadata-only citations that smuggled in a content claim.

Self-reported compliance does not catch any of these. Re-reading does.
