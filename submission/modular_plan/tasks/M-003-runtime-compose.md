# M-003 — Runtime composition helpers

## Specs to load

- [`../features/composition-root.md`](../features/composition-root.md)
- [`../technical/public-api-contracts.md`](../technical/public-api-contracts.md)
- [`../architecture/modular-system.md`](../architecture/modular-system.md)

## Deliverable

- `aegis/runtime/compose.py` (or equivalent) with:
  - AI-disabled / mode selection via `shared.reliability`
  - Helper to run batch demo path (and optionally pv/supply dispatch)
- Re-export from `aegis.runtime`

## Done when

- [ ] Runtime imports workflows + shared only
- [ ] No policy logic duplicated in app beyond calling runtime
