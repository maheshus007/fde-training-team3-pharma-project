# T-001 — Modular monolith skeleton

**Question:** What code needs writing for package boundaries?

## Specs to load

- [`../architecture/agent-system.md`](../architecture/agent-system.md)

## Deliverable

Create `submission/src/aegis/{shared,batch,pv,supply,runtime}/` and move existing flat modules:

- workflows → `batch/workflow.py`, `pv/workflow.py`, `supply/workflow.py`
- gates/contracts → `shared/`
- public re-exports in package `__init__.py`
- delete old flat `submission/src/*.py` modules (no shims)
- update app/tests/scripts imports to `aegis.*`
- add `submission/tests/test_module_boundaries.py` (AST import rule)

## Done when

- [ ] `python submission/scripts/test.py` green
- [ ] Boundary test enforces no workflow↔workflow and no shared→workflow imports
