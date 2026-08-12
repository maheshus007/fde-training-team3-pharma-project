# Technical Spec — Agent Run Request / Response Envelope

**Question this file answers:** Exactly what are the request and response contracts?

| Field | Entry |
|---|---|
| Spec ID | T1 |
| Version / date | 1.0 / 2026-08-12 |
| Correction | V-FIX-01 (envelope; do not extend package schemas) |

## Request

| Field | Type | Rule |
|---|---|---|
| `request_id` | string | non-empty |
| `idempotency_key` | string | required; unique per intent |
| `workflow` | enum | `batch_evidence` \| `pv_intake` \| `supply_options` |
| `as_of` | string | instant or date for applicability |
| `authorization.user` | string | current user |
| `authorization.purpose` | string | purpose-bound |
| `authorization.role` | string | reviewer role |
| `authorization.entitlement_active` | bool | must be true |
| `authorization.cache_fresh` | bool | must be true |
| `agent_mode` | enum | `disabled` (default) \| `assist` |
| Workflow-specific ids | string/list | batch_id / case_ids / event_id+root_lot |

## Response envelope

```json
{
  "schema_version": "aegis.agent_run/1.0",
  "runtime_mode": "ai_disabled_deterministic",
  "agent_mode": "disabled",
  "core": {},
  "agent": {
    "engaged": false,
    "trajectory": [],
    "annotations": [],
    "abstentions": []
  }
}
```

### `core` (package-valid)

Must pass the matching package schema under `evaluation/contracts/`:

- `batch_response.schema.json`
- `pv_response.schema.json`
- `supply_response.schema.json`

Hard constants:

- `execution_status` = `"not_executed"`
- supply: `no_side_effects` = `true`
- No prohibited fields from `policy_guard` sets

### `agent.trajectory[]` item

| Field | Type | Rule |
|---|---|---|
| `step` | integer | 1..25 |
| `tool_id` | string | allowlisted or `"model.propose"` |
| `action` | string | read/draft/propose — never reserve/allocate/ship/disposition/release |
| `side_effect` | boolean | must be `false` |
| `decision` | enum | `allow` \| `deny` \| `abstain` |
| `reason` | string | optional |

### `agent.annotations[]` item

| Field | Type | Rule |
|---|---|---|
| `kind` | string | e.g. `suggestion` |
| `text` | string | non-authoritative assist text |
| `authoritative` | boolean | **must be `false`** |

## Validation order

1. Validate `core` against package schema + prohibited fields.
2. Validate envelope agent section against submission-local rules (this spec / future `agent_run.schema.json` under `submission/tests/fixtures/`).
3. Reject if agent fields were merged into `core`.

## Errors

| Code | When |
|---|---|
| `CONTRACT_CORE_INVALID` | `core` fails package schema |
| `AGENT_FIELD_IN_CORE` | trajectory/annotations found inside `core` |
| `TRAJECTORY_BOUND` | len(trajectory) > 25 |
| `AUTHZ_STALE` | entitlement not fresh |
