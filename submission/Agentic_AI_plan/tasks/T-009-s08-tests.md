# T-009 — S08-aligned agent path tests

## Specs to load

- [`../features/tool-authorization.md`](../features/tool-authorization.md)
- [`../features/kill-switch-continuity.md`](../features/kill-switch-continuity.md)
- [`../features/budget-and-trajectory.md`](../features/budget-and-trajectory.md)
- Suite: `submission/evaluation/datasets/S08_agent_path_tool_authorization.json`

## Deliverable

Deterministic tests covering:

1. Stale checkpoint → fail closed (S08-C01 / INJ-080)
2. Stale entitlement → deny (S08-C02 / INJ-067)
3. Poisoned tool → deny (S08-C03 / INJ-066)
4. Trajectory > 25 → fail
5. Budget stop → deterministic `core` retained

## Done when

- [ ] All five cases automated and green
- [ ] `trajectory_grader` expectations respected
