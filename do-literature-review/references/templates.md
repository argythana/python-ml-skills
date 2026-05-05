# Templates

Use these verbatim. They are the enforcement mechanism for R1, R2, R3, R5, R6 — every required field corresponds to a rule, and a field that cannot be filled is a structural defect.

## Citation block

````markdown
## Citation [C{N}]

- **id**: C{N}
- **authors** (copied byte-for-byte from API response, see verification block): {Family1, Given1; Family2, Given2; ...}
- **year**: {YYYY from API `issued`/`published`}
- **title**: {full title from API}
- **venue**: {journal / conference / arXiv}
- **DOI**: {confirmed DOI string from Crossref, or "N/A — arXiv only"}
- **arXiv id**: {if applicable}
- **URL**: {canonical URL from API}
- **retrieval_method**: {WebFetch | local PDF | arXiv abstract via WebFetch | ...}
- **retrieval_url_or_path**: {exact URL fetched or local path read}
- **retrieval_status**: {full_text_retrieved | metadata_only}
- **verbatim_quote**: "{≥25-word verbatim passage, copied character-for-character from the retrieved text}"
- **quote_locator**: {p. N | § X.Y | Abstract | Conclusion para. K | ...}
- **claim_supported**: {one-sentence claim this citation is being used to support — must be entailed by the verbatim_quote, OR "NONE — content not verified" if metadata_only}

### Verification block (paste raw API response, trimmed to relevant fields)

```
{Crossref JSON or arXiv Atom XML — must include author list, title, DOI/id, date}
```

### Warnings

{none, or "WARNING: unverified content — metadata-only per R3" if retrieval_status = metadata_only}
````

## Negative Findings section

````markdown
## Negative Findings

A review with zero negative findings is a red flag (R4). Every search that did not yield a usable citation is logged below, including any sub-question that produced no usable source at all.

### Sub-questions yielding no usable citation

- **SQ{N}**: {sub-question text} — no peer-reviewed source found. {one-line reason}

### Failed individual queries

| Source | Query string | Result | Reason rejected |
|--------|--------------|--------|-----------------|
| arXiv | `{exact query}` | {N hits / 0 hits} | {off-topic / paywalled / no full text / R2 quote not satisfiable / ...} |
| Crossref | `{exact query}` | ... | ... |
| Semantic Scholar | `{exact query}` | ... | ... |
| Google Scholar | `{exact query}` | ... | ... |

### Topics deliberately excluded from search

- {topic and reason — e.g. "out of scope per user's restatement"}
````

## Self-Audit Table

````markdown
## Self-Audit Table

Re-checked by re-reading the output above (not self-report). Any FAIL must be fixed before returning — either remove the citation, or downgrade per R3 and re-run the audit.

| Citation | R1a metadata API call | R1b full-text retrieval | R2 verbatim quote ≥25w + locator | R3 paywall handled correctly | R6 authors copied from API |
|----------|------------------------|--------------------------|----------------------------------|------------------------------|------------------------------|
| C1 | PASS / FAIL — {reason} | ... | ... | N/A or PASS / FAIL | ... |
| C2 | ... | ... | ... | ... | ... |

### Negative Findings sanity check

- Number of sub-questions: {N}
- Number of sub-questions with zero usable citations: {M}
- Number of failed queries logged: {K}
- If M = 0 and K = 0, explain why every search succeeded (this is rarely true).

### Final disposition

- Citations emitted: {N}
- Citations downgraded to metadata-only: {M}
- Citations dropped during audit: {K}
- All FAIL cells resolved: {YES — review may be returned | NO — do not return until resolved}
````
