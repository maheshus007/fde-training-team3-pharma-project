# Technical Spec — Public API Contracts

**Question this file answers:** Exactly which callable APIs stay stable?

| Field | Entry |
|---|---|
| Spec ID | MT2 |
| Version / date | 1.0 / 2026-08-12 |

## Workflow APIs

### `aegis.batch.reconcile_batch`

```
reconcile_batch(batch_id: str, request_id: str, user: str) -> dict
```

- `workflow` in response: `"batch_evidence"`
- `execution_status`: `"not_executed"`
- Must remain valid against package `batch_response.schema.json` when required fields present

### `aegis.pv.build_pv_response`

```
build_pv_response(case_ids: list[str], request_id: str, user: str) -> dict
```

- `workflow`: `"pv_intake"`

### `aegis.supply.build_supply_response`

```
build_supply_response(event_id: str, root_lot: str, request_id: str, user: str) -> dict
```

- `workflow`: `"supply_options"`
- `no_side_effects`: `true`

## Shared APIs (import path change only)

| Old | New |
|---|---|
| `from src.contracts import ...` | `from aegis.shared.contracts import ...` |
| `from src.policy_guard import ...` | `from aegis.shared.policy_guard import ...` |
| bare `import contracts` (graders with src on path) | `from aegis.shared.contracts import ...` |
| bare `import workflow_batch` | `from aegis.batch import reconcile_batch` or runtime helper |

## Runtime API (minimum)

```
select_runtime_mode(workflow: str) -> RuntimeSelection   # may re-export shared.reliability
run_batch_demo(user: str, batch_id: str) -> dict         # returns workflow core dict in this track
```

Agent envelope is **out of scope** for this track.
