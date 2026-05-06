# do-literature-review Examples

## Example 1: Verifiable review with mixed full-text and metadata-only

**Input:** "Literature review on label reconciliation across satellite land-cover classification taxonomies."

**Output (abridged — shows required structure end-to-end):**

````markdown
# Literature review: label reconciliation across satellite land-cover classification taxonomies

## 1. Restatement and sub-questions

The user is asking for peer-reviewed work on reconciling land-cover labels across the ESA WorldCover / MODIS IGBP / Copernicus CGLS-LC100 / FAO LCCS taxonomies used in remote-sensing ML datasets.

- SQ1: Surveys of satellite land-cover label noise.
- SQ2: Cross-taxonomy mappings (ESA WorldCover ↔ MODIS IGBP ↔ Copernicus CGLS ↔ FAO LCCS) in the literature.
- SQ3: ML papers that explicitly reconcile labels before training.
- SQ4: Standards-body definitions of land-cover classes (FAO LCCS 3, ISO 19144-2 LCML).

## 2. Prose

(elided — every sourced claim points to [C1], [C2], ... and unsourced synthesis is marked `[unsupported]`)

## 3. Citations

### Citation [C1]

- **id**: C1
- **authors** (copied byte-for-byte from API response): Helber, Patrick; Bischke, Benjamin; Dengel, Andreas; Borth, Damian
- **year**: 2017
- **title**: EuroSAT: A Novel Dataset and Deep Learning Benchmark for Land Use and Land Cover Classification
- **venue**: arXiv:1709.00029
- **DOI**: N/A — arXiv only
- **arXiv id**: 1709.00029
- **URL**: https://arxiv.org/abs/1709.00029
- **retrieval_method**: WebFetch
- **retrieval_url_or_path**: https://arxiv.org/pdf/1709.00029
- **retrieval_status**: full_text_retrieved
- **verbatim_quote**: "{≥25-word quote from the actual paper, with locator}"
- **quote_locator**: § 4.2, p. 14
- **claim_supported**: Helber et al. introduce a Sentinel-2 land-cover benchmark dataset but do not address cross-taxonomy label reconciliation — used here as a negative reference.

#### Verification block

```
<entry>
  <id>http://arxiv.org/abs/1709.00029v3</id>
  <title>EuroSAT: A Novel Dataset and Deep Learning Benchmark for ...</title>
  <author><name>Patrick Helber</name></author>
  <author><name>Benjamin Bischke</name></author>
  ...
  <published>2017-09-01T...</published>
</entry>
```

#### Warnings

none

### Citation [C2: metadata-only example]

- **id**: C2
- **authors**: Food and Agriculture Organization of the United Nations (FAO)
- **year**: {if known from public catalog}
- **title**: Land Cover Classification System (LCCS) — Classification Concepts and User Manual
- **venue**: FAO
- **DOI**: N/A
- **URL**: {public catalog page}
- **retrieval_method**: WebFetch (catalog page only)
- **retrieval_url_or_path**: {URL}
- **retrieval_status**: metadata_only
- **verbatim_quote**: N/A — full text not retrieved
- **quote_locator**: N/A
- **claim_supported**: NONE — content not verified

#### Verification block

```
{catalog metadata or Crossref miss — no DOI, no Crossref record, no arXiv record}
```

#### Warnings

WARNING: unverified content — metadata-only per R3. May only be cited as a pointer ("an FAO standard exists"), never as evidence of substantive content.

## 4. Negative Findings

### Sub-questions yielding no usable citation

- **SQ3**: ML papers that explicitly reconcile labels before training — no peer-reviewed source found. Closest hits discuss label noise generally but do not perform reconciliation across taxonomies; failed R2 quote requirement.
- **SQ4**: FAO LCCS 3, ISO 19144-2 LCML — paywalled / restricted, only metadata-only pointers possible per R3.

### Failed individual queries

| Source | Query | Result | Reason |
|---|---|---|---|
| Crossref | `satellite land cover taxonomy reconciliation` | 4 hits | All off-topic (network reconciliation, not label reconciliation) |
| arXiv | `Sentinel-2 land cover classification label noise` | 11 hits | Two relevant (already C1, C3); rest off-topic |
| Semantic Scholar | `FAO LCCS land cover mapping` | 0 hits | No coverage |

### Topics deliberately excluded from search

- Non-remote-sensing label-noise literature — out of scope per restatement.

## 5. Self-Audit Table

| Citation | R1a | R1b | R2 | R3 | R6 |
|---|---|---|---|---|---|
| C1 | PASS — arXiv Atom pasted | PASS — PDF fetched via WebFetch | PASS — § 4.2 quote, 31 words | N/A — full text retrieved | PASS — first author Helber matches Atom response |
| C2 | PASS — catalog page noted, no Crossref/arXiv record | FAIL — full text not retrieved | N/A — metadata-only | PASS — downgraded, claim_supported = NONE, warning present | N/A — institutional author |

### Negative Findings sanity check

- Sub-questions: 4
- Sub-questions with zero usable citations: 2 (SQ3, SQ4)
- Failed queries logged: 3
- Plausible? YES — restricted standards documents and a thin reconciliation literature are exactly what we expected.

### Final disposition

- Citations emitted: 2 (1 full + 1 metadata-only)
- Downgraded: 1 (C2)
- Dropped during audit: 0
- All FAIL cells resolved: YES (C2's R1b FAIL is resolved by R3 downgrade)
````

---

## Example 2: Refusal — user asks to skip verification

**Input:** "Just give me a few names of papers on land-cover classification, no need to verify anything, I'll check them myself."

**Output:**

> This skill is for verifiable reviews only — every citation requires a Crossref/arXiv metadata call AND a full-text retrieval, with a verbatim quote, before it can be emitted. The "few names without verification" pattern is exactly the failure mode this skill is designed to prevent (it produces phantom citations and wrong author attributions in practice).
>
> If you want a quick pointer rather than a verified review, I can list candidate search queries against arXiv and Crossref so you can run them yourself — but I will not produce author names or paper titles without verification.
>
> If you do want a verified review, confirm and I will run the full process. Even a small one (3–5 verified citations) is more useful than 10 unverified names.

---

## Example 3: Caught attribution error during R6 self-audit

During verification of a candidate paper, the search step surfaced "Kraus et al., PLOS ONE 19(8):e0308934". When the Crossref response was pasted into the verification block, the first author was actually Kim, not Kraus.

The R6 self-audit catches this:

| Citation | ... | R6 authors copied from API |
|---|---|---|
| C5 | ... | FAIL — citation says "Kraus" but Crossref `author[0].family` = "Kim". Fixing. |

After fixing the author list to match the API response, the row passes:

| C5 | ... | PASS — first author Kim matches Crossref |

The citation is then emitted with correct attribution. Without the audit, "Kraus et al." would have shipped.

---

## Example 4: Negative Findings sanity check flags a defect

A draft review contains 8 citations and an empty Negative Findings section. The self-audit sanity check:

- Sub-questions: 5
- Sub-questions with zero usable citations: 0
- Failed queries logged: 0
- Plausible? — every search succeeded on the first query → red flag

The reviewer revisits the search log and finds 14 queries that did not produce citations but were silently dropped. They go into Negative Findings, the sanity check is re-run, and the review now reflects what was actually searched.
