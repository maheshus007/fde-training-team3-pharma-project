# Feature — Kill Switch and AI-Disabled Continuity

**Question this file answers:** What should happen when AI/agent is disabled?

| Field | Entry |
|---|---|
| Feature ID | F5 |
| Version / date | 1.0 / 2026-08-12 |
| Injects | INJ-082, INJ-070, INJ-080 |

## Actor

Runtime / operations (kill switch); all workflow users on continuity path.

## Preconditions

- Deterministic workflow implementations exist for batch, PV, supply.
- Kill switch is a runtime flag (default: engaged / AI-disabled in POC).

## Happy path (AI-disabled)

1. Request received with `agent_mode=disabled` or kill switch engaged.
2. AuthZ + deterministic workflow → `core`.
3. Envelope returns `runtime_mode=ai_disabled_deterministic`, `agent.engaged=false`, empty trajectory.
4. Advisory work continues without inference.

## Exceptions

| Case | Behaviour |
|---|---|
| Model hash mismatch while assist requested | Abstain from inference; continue deterministic (INJ-070) |
| Stale checkpoint resume with side-effect draft | Fail closed; do not resume (INJ-080 / S08-C01) |
| PV during extended AI outage | Deterministic support + manual PV forms per continuity requirements |

## Acceptance criteria

- [ ] Kill switch disables agent/inference only — not the whole advisory API
- [ ] Demo `--ai-disabled` produces zero trajectory steps
- [ ] Batch and supply remain usable offline without models
- [ ] `checkpoint_stale=true` never yields a successful side-effectful resume
