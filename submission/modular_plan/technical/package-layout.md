# Technical Spec — Package Layout

**Question this file answers:** Exactly what directories and files must exist?

| Field | Entry |
|---|---|
| Spec ID | MT1 |
| Version / date | 1.0 / 2026-08-12 |

## Target tree

```
submission/src/aegis/
  __init__.py
  shared/
    __init__.py
    contracts.py
    policy_guard.py
    security_gates.py
    privacy_gates.py
    reliability.py
    finops.py
    model_gateway.py
    clinical_protocol.py
  batch/
    __init__.py          # exports reconcile_batch
    workflow.py
  pv/
    __init__.py          # exports build_pv_response
    workflow.py
  supply/
    __init__.py          # exports build_supply_response
    workflow.py
  runtime/
    __init__.py
    compose.py           # mode select + dispatch helpers
```

## Must not exist after this track

- `submission/src/workflow_batch.py`
- `submission/src/workflow_pv.py`
- `submission/src/workflow_supply.py`
- `submission/src/contracts.py` (and other flat modules listed in migration map)
- `submission/src/aegis/agents/` (deferred)

## Path setup

Call sites insert `submission/src` on `sys.path` so `import aegis` works.
Do not keep inserting paths that expect bare `workflow_batch`.
