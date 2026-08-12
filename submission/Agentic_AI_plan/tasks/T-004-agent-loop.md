# T-004 — Bounded agent loop

## Specs to load

- [`../features/budget-and-trajectory.md`](../features/budget-and-trajectory.md)
- [`../technical/state-transitions.md`](../technical/state-transitions.md)

## Deliverable

- `aegis/agents/loop.py` with max 25 steps
- Trajectory recording `{step, tool_id, action, side_effect:false, decision}`
- Stop + discard incomplete assist on bound/budget

## Done when

- [ ] Loop refuses to append step 26
- [ ] Prohibited action tokens denied
