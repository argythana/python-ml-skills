# Paywall and no-full-text downgrade (R3)

When R1b (full-text retrieval) fails, the citation does not disappear — but it is downgraded to **metadata-only** with strict limits on how it can be used.

## When R3 applies

- Paywalled journal article — Crossref returns metadata, but the publisher gates the PDF behind a login.
- NATO STANAGs, ISO/IEC/IMO standards, military doctrine — public catalog page exists, full document does not.
- Proprietary taxonomies (Statcode, Lloyd's, IHS Markit) — vendor confirms the artifact exists but does not publish full content.
- WebFetch returns a 403, a redirect-to-login, an interstitial, or an abstract-only page.
- Preprint listed on arXiv but the link is dead.

## What "metadata-only" means

The citation block is still emitted, with these constraints:

- `retrieval_status` = `metadata_only`.
- `verbatim_quote` = `N/A — full text not retrieved`.
- `quote_locator` = `N/A`.
- `claim_supported` = `NONE — content not verified`.
- A `WARNING: unverified content — metadata-only per R3` line in the Warnings section of the citation block.

## How a metadata-only citation may be used in prose

Only as a **pointer**. Acceptable phrasings:

> "A NATO standard exists in this area (STANAG 1241 [C7], metadata-only — content not verified)."

> "Proprietary vessel-classification taxonomies are documented in industry sources [C8], not surveyed here."

Unacceptable phrasings:

> ~~"STANAG 1241 defines five identity categories..."~~ — this is a content claim. Forbidden under R3.

> ~~"Industry taxonomies use 12 high-level vessel classes..."~~ — same problem.

If you find yourself wanting to make a content claim, the citation is failing R3. Either retrieve the full text and re-promote it to a normal citation, or remove the claim from the prose and replace it with `[unsupported]`.

## Why this is structural, not advisory

The `claim_supported = "NONE — content not verified"` field forces the writer to confront, every single time, that the source has no content backing in this review. R5's self-audit table re-checks this field; any metadata-only citation whose `claim_supported` is anything other than `NONE` fails the audit.

## Standards bodies and proprietary taxonomies — default treatment

Treat as R3 by default unless full text was actually retrieved:

- NATO STANAG (1241, 4154, ...)
- ISO, IEC, IMO documents
- ITU recommendations (sometimes free; check)
- MIL-STD documents (sometimes free; check)
- Lloyd's Register, IHS, Clarksons, S&P Global proprietary taxonomies
- Statcode / Statcode 5

Some of these are actually free (ITU-R M.1371, MIL-STD-2525). Verify by fetching. If the fetch returns the actual specification text, R1b is satisfied and R3 does not apply.
