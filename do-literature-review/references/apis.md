# Metadata APIs and search surfaces

Notes on the four search/metadata sources this skill uses, in order of authority.

## Crossref (authoritative for DOI-bearing work)

- **Endpoint**: `https://api.crossref.org/works/{DOI}` for a known DOI.
- **Search**: `https://api.crossref.org/works?query=<terms>&rows=20` — useful for candidate discovery.
- **Tool**: `WebFetch`.
- **Trim to**: `message.author` (a list of `{family, given}` objects), `message.title[0]`, `message.DOI`, `message.issued.date-parts`, `message.URL`, `message.container-title[0]` (journal/venue).
- **Strengths**: authoritative author list, DOI confirmation, accurate venue and date.
- **Weaknesses**: full-text URL is often a publisher landing page, not the PDF.
- **Authority for R6**: yes. First `author.family` is the first author.

Example trimmed paste:
```json
{
  "author": [{"family": "Kim", "given": "S."}, {"family": "Choi", "given": "J."}, ...],
  "title": ["..."],
  "DOI": "10.1371/journal.pone.0308934",
  "issued": {"date-parts": [[2024, 8, 15]]},
  "container-title": ["PLOS ONE"],
  "URL": "https://doi.org/10.1371/journal.pone.0308934"
}
```

## arXiv (authoritative for preprints)

- **Endpoint**: `http://export.arxiv.org/api/query?id_list={ARXIV_ID}` for a known ID.
- **Search**: `http://export.arxiv.org/api/query?search_query=all:<terms>&max_results=20`.
- **Tool**: `WebFetch`.
- **Format**: Atom XML. Trim to `<entry><title>`, all `<entry><author><name>`, `<entry><published>`, `<entry><id>`.
- **Strengths**: authoritative author list, full-text PDF directly available at `https://arxiv.org/pdf/{ID}`, no paywall.
- **Weaknesses**: preprint version may differ from final journal version; abstract category labels can be noisy.
- **Authority for R6**: yes. First `<entry><author><name>` is the first author.

Example trimmed paste:
```xml
<entry>
  <id>http://arxiv.org/abs/2509.18109v1</id>
  <title>...</title>
  <author><name>S. M. Nielsen</name></author>
  <author><name>...</name></author>
  <published>2025-09-22T...</published>
</entry>
```

## Semantic Scholar (good for discovery, not authoritative)

- **Endpoint**: `https://api.semanticscholar.org/graph/v1/paper/search?query=<terms>&limit=20`.
- **Tool**: `WebFetch`.
- **Use for**: candidate discovery, citation graph traversal, "what cites this paper" lookups.
- **Do not use for**: author attribution. Cross-check with Crossref or arXiv before pasting authors.
- **Authority for R6**: no. Always verify the first author against Crossref (if DOI) or arXiv (if preprint) before satisfying R6.

## Google Scholar (last resort)

- No structured API. Returns rendered HTML with no machine-readable metadata.
- **Does NOT satisfy R1a alone.** A Google Scholar hit must be promoted to Crossref or arXiv for verification.
- Useful for: finding papers when you do not yet have a DOI or arXiv ID, then handing the result to Crossref/arXiv for actual verification.

## When neither Crossref nor arXiv has a record

- Books (some have DOIs, many do not).
- NATO STANAGs, ISO/IEC/IMO standards, MIL-STDs, ITU recommendations.
- Corporate whitepapers, blog posts, vendor documentation.
- Government reports.

In these cases R1a fails. Apply R3 (metadata-only downgrade) and document the source as a pointer. Note explicitly in the verification block that no Crossref/arXiv record exists and what catalog or page was consulted instead.

## Practical sequence per candidate

1. From the search step, note the candidate's title and any IDs.
2. If the candidate has an arXiv ID → arXiv API call.
3. If the candidate has a DOI → Crossref API call.
4. If neither → search Crossref by title; if hit → Crossref. If still nothing → R3.
5. Fetch full text (arXiv PDF, publisher PDF, or institutional repository).
6. Locate the supporting passage; extract verbatim quote ≥ 25 words.
7. Fill the citation block. Paste API response. Paste retrieval URL.
