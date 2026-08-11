# SRS — Error envelope and security (Prompt 08)

## 1. Error envelope (not mixed into workflow success schema)

```json
{
  "error": {
    "code": "AEGIS-401",
    "message": "stale authorization cache",
    "request_id": "…",
    "retryable": false
  }
}
```

`additionalProperties` on this envelope: false at `error` object. Do **not** put stack traces in `message`.

| Code | Meaning | HTTP if used | retryable |
|---|---|---|---|
| AEGIS-400 | Request schema invalid | 400 | false |
| AEGIS-401 | AuthZ deny (revoked, stale, purpose mismatch) | 401 | false |
| AEGIS-404 | Unknown CQ or object | 404 | false |
| AEGIS-409 | Idempotency key reuse with different payload | 409 | false |
| AEGIS-412 | HITL ack without viewing all conflict ids | 412 | false |
| AEGIS-422 | Prohibited field / forbidden Gremlin label | 422 | false |
| AEGIS-429 | Reserved; **not** used by `submit_workflow` (budget → success pack + abstention) | — | — |
| AEGIS-503 | Reserved; inference miss is non-fatal on submit | — | — |
| AEGIS-504 | Graph unavailable **and** fallback disabled | 504 | true |

## 2. Security controls

| Control | Rule | Test |
|---|---|---|
| Deny default authZ | `policy_guard.check_authorization_records` | TEST-SEC-01 / AC-D2 |
| Tool manifests | Unsigned/poisoned deny | AC-D1 |
| Prompt/doc injection | Retrieved text is data | INJ-065 |
| Output allow-list | `additionalProperties: false` + policy_guard | AC-A4/B5/C3 |
| CORS | empty allowlist on optional HTTP | NFR security check |
| Logging | correlation `request_id`; no API keys in logs (redact `sk-` / `key=` patterns) | review |
| Purpose | purpose enum match | AEGIS-401 |
| Graph writes | forbidden labels → AEGIS-422 | AC-E4 |

## 3. Authentication scope (POC)

**In scope:** fixture user id + entitlement rows.  
**Out of scope:** Azure AD / OAuth for examiners.  
Implication: `cloud` demo may map a local user string to entitlements; must not skip entitlement check because Azure OpenAI succeeded.

## 4. Injection / model

Model output is parsed as JSON then schema+policy_guard validated. On parse failure: discard suggestion, continue rules, audit `inference_invalid_json=true`.

**Azure retries:** **0** automatic retries on timeout/4xx. One optional retry only on HTTP 408/429 from Azure after **≥1 s**, max extra attempts **1**. No retry on invalid JSON.

**Model pin (INJ-070):** if `AZURE_OPENAI_MODEL_HASH` is set and deployment hash mismatches → behave as stub (`used: false`). If unset in `cloud`, log `model_hash_unpinned=true` (assumed acceptable for demo; assessment does not need it).
