# M-009 — Verify tests and AI-disabled demo

## Specs to load

- [`../plan/MODULAR_PLAN.md`](../plan/MODULAR_PLAN.md) success criteria
- [`../product/prd.md`](../product/prd.md) metrics

## Deliverable

Run:

```
python submission/scripts/test.py
python submission/app/demo.py --ai-disabled
```

Confirm evidence JSON update under `submission/evidence/` from the test script.
Confirm no `aegis/agents/` directory exists yet.

## Done when

- [ ] All submission tests green
- [ ] Demo works on AI-disabled path
- [ ] Grep migration checklist clean for code paths
- [ ] Ready to start `submission/specs/tasks/` agentic track
