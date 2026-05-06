# Paywall and no-full-text downgrade (R3)

When R1b (full-text retrieval) fails, the citation does not disappear — but it is downgraded to **metadata-only** with strict limits on how it can be used.

## When R3 applies

- Paywalled journal article — Crossref returns metadata, but the publisher gates the PDF behind a login.
- ISO/IEC standards, FAO/WHO guidelines, government technical reports — public catalog page exists, full document does not.
- Proprietary taxonomies (commercial geospatial datasets, clinical coding systems) — vendor confirms the artifact exists but does not publish full content.
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

> "An ISO standard exists in this area (ISO 19144-2 LCML [C7], metadata-only — content not verified)."

> "Proprietary land-cover taxonomies are documented in industry sources [C8], not surveyed here."

Unacceptable phrasings:

> ~~"ISO 19144-2 LCML defines five land-cover meta-classes..."~~ — this is a content claim. Forbidden under R3.

> ~~"Industry taxonomies use 12 high-level land-cover classes..."~~ — same problem.

If you find yourself wanting to make a content claim, the citation is failing R3. Either retrieve the full text and re-promote it to a normal citation, or remove the claim from the prose and replace it with `[unsupported]`.

## Why this is structural, not advisory

The `claim_supported = "NONE — content not verified"` field forces the writer to confront, every single time, that the source has no content backing in this review. R5's self-audit table re-checks this field; any metadata-only citation whose `claim_supported` is anything other than `NONE` fails the audit.

## Standards bodies and proprietary taxonomies — default treatment

Treat as R3 by default unless full text was actually retrieved:

- ISO, IEC documents (e.g. ISO 19144-2 LCML)
- FAO documents (e.g. LCCS — Land Cover Classification System)
- WHO guidelines and clinical coding systems (e.g. SNOMED-CT under restricted licence)
- ITU recommendations (sometimes free; check)
- Commercial geospatial taxonomies and proprietary remote-sensing product specifications

Some of these are actually free (e.g. several ITU-T recommendations, Copernicus product user manuals). Verify by fetching. If the fetch returns the actual specification text, R1b is satisfied and R3 does not apply.
