# Verification (R1, R2, R6)

Every citation must pass three structural checks before being emitted. If any check cannot be satisfied, the citation is dropped or downgraded per [paywall.md](paywall.md). No exceptions, no "best effort".

## R1. Two tool calls per citation

Both must happen, and both must leave a paper trail in the citation block.

### R1a. Metadata call

One of:

- **Crossref**: `WebFetch https://api.crossref.org/works/{DOI}` → JSON
- **arXiv**: `WebFetch http://export.arxiv.org/api/query?id_list={ARXIV_ID}` → Atom XML

Trim the response to the relevant fields and **paste it verbatim into the citation's verification block**:

- Crossref: `message.author`, `message.title`, `message.DOI`, `message.issued`, `message.URL`, `message.container-title`
- arXiv: `<entry><title>`, all `<entry><author><name>`, `<entry><published>`, `<entry><id>`

If neither Crossref nor arXiv has a record (e.g. an ISO standard, a corporate whitepaper), R1a fails → apply R3 metadata-only downgrade or drop.

### R1b. Full-text retrieval

One of:

- `WebFetch` of the paper PDF or HTML.
- Local file read of a PDF the user supplied.

Record the exact URL fetched or path read. A 403, redirect-to-login, or paywall splash page does **not** count as full-text retrieval — apply R3.

If R1a passed but R1b failed, the citation may exist as a metadata-only pointer per R3. It may not make any substantive claim about content.

There is no third path. You may not paraphrase a result you have not retrieved.

## R2. Verbatim quote per citation

Every citation must carry **at least one verbatim quoted passage of 25 words or more**, lifted from the retrieved full text, with a page or section locator (`p. 4`, `§ 3.2`, `Abstract`, `Conclusion para. 2`).

The quote is the evidence for the `claim_supported` line. The reader must be able to verify the claim by reading the quote alone. If no such quote exists in the paper, the source does not support the claim — remove the citation. Do not soften the claim, do not paraphrase, do not move on.

A 25-word quote is enough to constitute evidence and short enough that abstracts qualify. If you find yourself wanting to use a 5-word fragment, the source is probably being stretched.

## R6. Authors are taken from the API response

The author list in every citation must be copied **byte-for-byte from the Crossref or arXiv response** pasted in the verification block. The first author shown in the citation must match the first `author.family` (Crossref) or first `<author><name>` (arXiv) in that response, character for character.

Do not write authors from prior knowledge, search-snippet text, another paper's reference list, or the PDF's title page. All three of those have produced wrong attributions in practice. The API response is the only authoritative source.

This rule eliminates a specific failure mode: research subagents return wrong first authors that only metadata lookups catch — observed pattern is a paper attributed to a co-author or a similarly-named researcher when the authoritative API response (Crossref `author[0].family` or arXiv first `<author><name>`) records a different first author entirely.

## Failure modes this section blocks

- **Phantom citations**: R1b makes them impossible — no fetched URL, no citation.
- **Scope overreach**: R2 makes it impossible — no quote, no claim.
- **Author drift**: R6 makes it impossible — authors come from the pasted API response.
