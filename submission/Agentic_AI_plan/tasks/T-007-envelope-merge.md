# T-007 — Envelope merge

## Specs to load

- [`../technical/agent-request-response.md`](../technical/agent-request-response.md)
- [`../plan/VALIDATION.md`](../plan/VALIDATION.md) (V-FIX-01)

## Deliverable

- `aegis/agents/merge.py` + `aegis/runtime` runner producing envelope
- `core` left package-schema valid
- Annotations only under `agent.annotations` with `authoritative:false`
- Reject / test failure if agent fields appear inside `core`

## Done when

- [ ] Package schema validation of `core` passes with assist engaged
- [ ] Test covers `AGENT_FIELD_IN_CORE` detection
