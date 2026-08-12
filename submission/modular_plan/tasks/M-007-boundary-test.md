# M-007 — Import boundary test

## Specs to load

- [`../features/import-boundary-enforcement.md`](../features/import-boundary-enforcement.md)
- [`../technical/dependency-rules.md`](../technical/dependency-rules.md)

## Deliverable

Add `submission/tests/test_module_boundaries.py`:

- AST-scan `submission/src/aegis/**/*.py`
- Fail on illegal imports per MT3 matrix
- Stdlib only

## Done when

- [ ] Test fails if a workflow imports another workflow (manual sanity once)
- [ ] Test passes on the compliant tree via `scripts/test.py`
