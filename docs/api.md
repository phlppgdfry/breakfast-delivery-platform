# Local API contract

Base URL: `http://127.0.0.1:8115`. JSON is UTF-8. All records are synthetic.

| Method and route | Behaviour |
| --- | --- |
| `GET /api/health` | HTTP 200 with `status=ok`, `mode=local-demo` |
| `GET /api/snapshot` | Configuration, presented records, metrics, analysis and latest 12 audit events |
| `GET /api/export.csv` | Current presented records; union of keys preserves optional notes |
| `POST /api/action` | Validate and commit one domain use case; return updated snapshot |

Only explicitly allowed public assets are served. Database files, source files and directory traversal paths are not exposed. The CSV exporter prefixes formula-leading values for spreadsheet safety.

Example action body:

```json
{
  "action": "create",
  "customer": "Taylor Demo",
  "box": "Classic",
  "quantity": 1,
  "postal": "9000",
  "slot": "06:00–07:00",
  "allergens_ack": true
}
```

Updates require `id` and integer `version` from the most recent snapshot. The next committed version increments by one. Creates (only in Morning Table) receive a server-generated identifier and version 1. Authoritative totals, state transitions, risk scores and metrics are calculated on the server.

Send `Content-Type: application/json`; the body must be 1–16384 bytes. An Origin header, when present, must match the server’s local origin. CLI clients may omit Origin, but still need the local Host.

| Status | Meaning |
| --- | --- |
| 200 | Read or mutation succeeded |
| 400 | Malformed JSON, invalid field or rejected business rule |
| 403 | Invalid Host or cross-origin browser write |
| 404 | Unknown route or non-public file |
| 409 | Stale record version; refresh before retrying |
| 413 | Empty or oversized mutation body |
| 415 | Mutation is not sent as JSON |
| 500 | Unexpected failure; the mutation transaction rolls back |

Errors have the shape `{"error":"human-readable explanation"}`. The browser preserves form input after validation errors and refreshes state after a conflict. There is no public API authentication contract because the service is local-only.
