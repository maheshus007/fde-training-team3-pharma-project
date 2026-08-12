# T-012 — Verify tests and evidence

## Specs to load

- [`../plan/AGENTIC_PLAN.md`](../plan/AGENTIC_PLAN.md) success criteria
- [`../product/prd.md`](../product/prd.md) metrics

## Deliverable

Run and record:

```
python submission/scripts/test.py
python submission/app/demo.py --ai-disabled
```

Confirm `submission/evidence/test_results.json` updated by the test script.
Optionally run evaluate path if agent fixtures are hooked.

## Done when

- [ ] All submission tests green
- [ ] AI-disabled demo works
- [ ] No edits outside `submission/`
