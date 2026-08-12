# T-010 — Demo and Taipy wiring

## Specs to load

- [`../architecture/agent-system.md`](../architecture/agent-system.md)
- [`../features/kill-switch-continuity.md`](../features/kill-switch-continuity.md)

## Deliverable

- `demo.py`: default AI-disabled; optional `--agent assist`
- Taipy: call `runtime.run`; do not embed policy logic in UI
- Print/show envelope summary without implying regulated execution

## Done when

- [ ] `python submission/app/demo.py --ai-disabled` → `agent.engaged=false`
- [ ] Assist flag does not break AI-disabled default
