---
name: do-literature-review
description: >
  Use this skill when the user asks for a verifiable literature review or
  peer-reviewed citations for an ADR, design doc, paper, or technical decision,
  with prompts like "literature review on X", "find papers on X", "survey the
  literature on X", or "cite peer-reviewed sources for X". Enforce structural
  verification: every emitted citation needs metadata lookup, full-text
  retrieval, a supporting quote with locator, byte-for-byte author attribution,
  Negative Findings, and a self-audit table. Do NOT use it for single-URL
  summarization, drafting the surrounding ADR, casual citation pointers where
  verification is explicitly waived, fictional references, or unsourced
  factual questions.
---

# do-literature-review

Produce literature reviews where every citation is **structurally verified** before it is emitted. The skill exists to make four documented failure modes impossible to commit:

1. **Phantom citations** — referencing paywalled or proprietary documents that were never read.
2. **Scope overreach** — citing a real paper for a claim it does not actually support.
3. **Author-attribution errors** — wrong first author, wrong year, wrong DOI from sloppy sub-research.
4. **Silent omission** — listing only successful hits and hiding the searches that returned nothing.

Imperative rules ("be careful", "verify everything") do not work — agents self-report compliance falsely. Every rule below is therefore enforced by a **required tool call whose result is pasted verbatim into the output**, or by a **required output field that cannot be filled without the tool call having happened**. If you cannot fill a field, refuse to emit the citation.

## Process

1. **Restate and decompose** — one paragraph restatement of the question + 3–8 sub-questions as a checklist.
2. **Search** — run queries against ≥ 2 of {arXiv, Crossref, Semantic Scholar, Google Scholar (last resort)}. Log every query string. Failed queries flow into Negative Findings.
3. **Per-paper verification** — see [verification.md](references/verification.md). Two mandatory tool calls per citation; raw API response pasted into the citation block.
4. **Compose prose** — every sourced claim points to a citation block by ID. Synthesis without a citation is marked `[unsupported]` inline, not deleted.
5. **Negative Findings** — see [negative_findings.md](references/negative_findings.md). Every failed query and every empty sub-question listed with reason.
6. **Self-audit** — see [self_audit.md](references/self_audit.md). Re-check every citation against R1–R6 by re-reading the output, not by self-report.
7. **Return** in order: restatement, prose, citation blocks, Negative Findings, Self-Audit Table.

## Hard rules

| Rule | Enforces | Reference |
|------|----------|-----------|
| **R1** | Two tool calls per citation: metadata API + full-text retrieval; raw response pasted | [verification.md](references/verification.md) |
| **R2** | Verbatim quote ≥ 25 words with page/section locator, supporting the specific claim | [verification.md](references/verification.md) |
| **R3** | Paywall / no-full-text → metadata-only downgrade, no content claim allowed | [paywall.md](references/paywall.md) |
| **R4** | Negative Findings section is mandatory; zero-failures result is a red flag | [negative_findings.md](references/negative_findings.md) |
| **R5** | Self-Audit Table is mandatory; computed by re-reading the output | [self_audit.md](references/self_audit.md) |
| **R6** | Authors copied byte-for-byte from the API response, not from memory or snippets | [verification.md](references/verification.md) |
| **R7** | Refusal posture: cannot fill a required field → drop the citation, do not guess | — |

API choices and response shapes are in [apis.md](references/apis.md). Citation, Negative Findings, and Self-Audit templates are in [templates.md](references/templates.md). A worked example is in [examples.md](examples.md).

## Anti-patterns (have happened, do not repeat)

- *"NATO STANAG 1241 defines vessel classes as ..."* without retrieving STANAG 1241 → R3 downgrade to metadata-only pointer.
- *"Soldi et al. 2021 discusses label reconciliation ..."* when the paper has no such section → R2's verbatim-quote rule catches this.
- *"Kraus et al., PLOS ONE 19(8):e0308934"* when Crossref says first author is Kim → R6 forces author attribution from the API response only.
- A list of five hits with no Negative Findings → implies every search succeeded; almost never true. R4 makes this visible.

## Refusal cases

If the user says "just give me a quick pointer, no need to verify" or asks for fictional/illustrative references, **decline** and explain that this skill is for verifiable reviews only. For single-URL summarization, route to `url-reader` instead.
