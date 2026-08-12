# M-005 — Retarget unit tests

## Specs to load

- [`../technical/file-migration-map.md`](../technical/file-migration-map.md)
- [`../technical/public-api-contracts.md`](../technical/public-api-contracts.md)

## Deliverable

Update imports in:

- `submission/tests/test_workflow_contracts.py`
- `submission/tests/test_prohibited_actions.py`
- `submission/tests/test_authorization_freshness.py`
- `submission/tests/test_tool_trust.py`

Change `from src.X` → `from aegis.shared.X` (with `submission/src` on path).

## Done when

- [ ] No `from src.` under `submission/tests/`
- [ ] Tests collect under unittest discovery
