# Feature — Workflow Packages

**Question this file answers:** What should each workflow package expose?

| Field | Entry |
|---|---|
| Feature ID | MF3 |
| Version / date | 1.0 / 2026-08-12 |

## Actor

Runtime / app / tests calling workflow public APIs.

## Public APIs (signatures unchanged)

| Package | Export | Source today |
|---|---|---|
| `aegis.batch` | `reconcile_batch(batch_id, request_id, user) -> dict` | `workflow_batch.py` |
| `aegis.pv` | `build_pv_response(case_ids, request_id, user) -> dict` | `workflow_pv.py` |
| `aegis.supply` | `build_supply_response(event_id, root_lot, request_id, user) -> dict` | `workflow_supply.py` |

## Behaviour

- Move code into `workflow.py` per package; re-export from `__init__.py`.
- Do not change response shapes (package contract compatibility).
- Workflows may import `aegis.shared` only when needed; today they use stdlib only — keep that unless a shared helper is required.

## Exceptions

- Workflows must not import each other.
- Workflows must not import `aegis.runtime` or `app`.

## Acceptance criteria

- [ ] Public function names and signatures unchanged
- [ ] Old flat `workflow_*.py` files removed
- [ ] Contract / prohibited-action tests still pass after retarget
