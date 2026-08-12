# T-006 — OfflineExtractAdapter + kill switch wiring

## Specs to load

- [`../technical/model-adapter.md`](../technical/model-adapter.md)
- [`../features/kill-switch-continuity.md`](../features/kill-switch-continuity.md)
- [`../prompts/`](../prompts/)

## Deliverable

- `aegis/agents/adapters/offline_extract.py`
- Runtime selection: default AI-disabled; assist only when flag + kill switch open
- Hash pin via `check_model_artifact` / `select_model`

## Done when

- [ ] Hash mismatch → abstain, deterministic continues
- [ ] Kill switch → adapter not invoked
