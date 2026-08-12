# Feature — Composition Root (`aegis.runtime`)

**Question this file answers:** How should the app compose modules?

| Field | Entry |
|---|---|
| Feature ID | MF4 |
| Version / date | 1.0 / 2026-08-12 |
| Correction | V-FIX-01 |

## Actor

CLI demo and Taipy UI (thin shells).

## Preconditions

- Workflow packages and shared kernel exist.

## Happy path

1. App puts `submission/src` on `sys.path` once.
2. App calls `aegis.runtime` helpers (e.g. select AI-disabled mode + run one workflow).
3. Runtime imports the target workflow + shared reliability/finops as needed.
4. UI does not embed policy or contract logic.

## Allowed temporary path

During migration tasks only, app may `from aegis.batch import reconcile_batch` directly. Final preferred state: go through `runtime`.

## Acceptance criteria

- [ ] `aegis.runtime` provides at least mode selection + one-workflow dispatch helper
- [ ] `demo.py` no longer uses bare `import workflow_batch`
- [ ] Taipy imports updated similarly
