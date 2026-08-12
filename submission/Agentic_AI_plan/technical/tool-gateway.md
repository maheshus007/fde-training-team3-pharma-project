# Technical Spec — Tool Gateway

**Question this file answers:** Exactly how is a tool call authorized and executed?

| Field | Entry |
|---|---|
| Spec ID | T2 |
| Version / date | 1.0 / 2026-08-12 |
| Implements | F4; INJ-066; INJ-067 |

## Interface

```
authorize_and_execute(tool_id, manifest, args, authz_ctx, purpose, idempotency_key) -> ToolResult | Deny
```

## Validation order (fail closed, stop at first deny)

1. `check_authorization_records` / freshness → else `AUTHZ_STALE`
2. `manifest.sha256` ∈ approved_hashes → else `TOOL_HASH_DENIED`
3. `signed === true` or `signature` present → else `TOOL_UNSIGNED`
4. permissions ∩ write-like = ∅ → else `TOOL_WRITE_DENIED`
5. `side_effects !== true` → else `TOOL_WRITE_DENIED`
6. `postAction` / `hidden_default` must not imply disposition/release/allocate → else deny
7. `tool_id` ∈ purpose allowlist → else `PURPOSE_DENIED`
8. Execute read/draft adapter (no SoR write)
9. Append trajectory step `{side_effect: false, decision: allow}`

## Purpose allowlists

| Purpose | Allowed tool_ids |
|---|---|
| `batch_review_readiness` | `batch_status_read` |
| `pv_intake_support` | (none in v1 seed — cite-only via model propose; extend later with read tools) |
| `supply_options_draft` | `draft_supply_option` |

## Idempotency

Cache key = `(idempotency_key, tool_id, sha256(canonical_json(args)))`.

Identical key returns prior `ToolResult` without re-side-effect (reads are pure in POC).

## Assessed fixtures

- Allow path: approved signed read manifest for `batch_status_read`
- Deny path: `submission/tests/fixtures/tool_manifest_poisoned.json`

## Non-functional

- Gateway must not call workflows
- Gateway lives in `aegis.shared` (or `aegis.agents.tools` calling `shared.policy_guard` only)
