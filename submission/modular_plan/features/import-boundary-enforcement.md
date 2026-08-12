# Feature — Import Boundary Enforcement

**Question this file answers:** How do we prove the app is modular, not just re-foldered?

| Field | Entry |
|---|---|
| Feature ID | MF5 |
| Version / date | 1.0 / 2026-08-12 |

## Actor

CI / `submission/scripts/test.py` / developers.

## Preconditions

- `aegis` package tree exists.

## Rules under test

1. No module under `aegis.batch|pv|supply` imports another of those packages.
2. No module under `aegis.shared` imports `aegis.batch|pv|supply|runtime`.
3. (Optional stretch) `aegis.batch|pv|supply` must not import `aegis.runtime`.

## Mechanism

- Deterministic unittest: `submission/tests/test_module_boundaries.py`
- Static scan via `ast` parse of `.py` files under `submission/src/aegis/`
- No new third-party dependency (no import-linter package required)

## Exceptions

- None. Violations fail the test suite.

## Acceptance criteria

- [ ] Boundary test present and collected by `scripts/test.py`
- [ ] Intentional violation in a scratch check would fail (documented in test docstring)
- [ ] Suite green on the compliant tree
