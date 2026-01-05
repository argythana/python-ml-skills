# MCP Example Schema (Column Analysis)

This is a compact JSON schema that an MCP server could return for a "analyze_column" request.
Use compact fields to reduce token usage when sending responses back to a language model.

Example request (from agent):

```json
{
  "method": "analyze_column",
  "params": {
    "source": "/data/users.csv",
    "column": "status",
    "limit": 50
  }
}
```

Example response (MCP server):

```json
{
  "status": "ok",
  "result": {
    "summary": {
      "total": 1234567,
      "nulls": 123,
      "non_null": 1234444,
      "unique": 5,
      "cardinality": "Low"
    },
    "top": [
      {"v": "completed", "c": 987654, "p": 80.0},
      {"v": "pending",   "c": 123456, "p": 10.0}
    ],
    "notes": ["Low cardinality", "Minimal missing data"]
  }
}
```

Notes:

- Use short keys (`v`, `c`, `p`) to minimize token size when returning many rows.
- `top` contains the top N values (controlled by `limit`).
- Keep `notes` short and focused for quick human-readable hints.

Security & Versioning

- Include an authentication header or token in the MCP transport layer (not shown in schema).
- Add a `protocol_version` field at the top-level response if you expect schema changes.

Caching & Pagination

- For very high-cardinality columns, return `cursor` or `next` to page through results instead of returning everything.
