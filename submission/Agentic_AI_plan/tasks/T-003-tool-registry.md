# T-003 — Tool registry and gateway wiring

## Specs to load

- [`../features/tool-authorization.md`](../features/tool-authorization.md)
- [`../technical/tool-gateway.md`](../technical/tool-gateway.md)

## Deliverable

- `aegis/shared/tool_registry.py` with approved hash set for assessed mode
- Gateway function calling existing `check_tool_manifest` / authZ helpers
- Purpose allowlists per T2
- Unit tests for allow `batch_status_read` path and deny poisoned fixture

## Done when

- [ ] Poisoned manifest denied
- [ ] Approved signed read manifest allowed
- [ ] Idempotency key behaviour covered by a test
