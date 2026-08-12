# Feature — Agent Assist: PV Intake

**Question this file answers:** What should PV agent-assist do?

| Field | Entry |
|---|---|
| Feature ID | F2 |
| Workflow | `pv_intake` |
| Version / date | 1.0 / 2026-08-12 |

## Actor

PV intake specialist / safety physician reviewer.

## Preconditions

- Entitlement active for purpose `pv_intake_support`.
- Deterministic `build_pv_response` available.
- Agent only if `agent_mode=assist` and kill switch open.

## Allowed actions

extract, normalize, cluster, cite.

## Prohibited actions

final causality, seriousness, expectedness, reportability, signal confirmation, case auto-merge.

## Happy path

1. AuthZ re-check.
2. Deterministic PV response → `core` (source facts, duplicate candidates, clocks, terminology, listedness context).
3. Optional agent: read-only clustering/citation assist; trajectory recorded.
4. Annotations may highlight conflicts; must not resolve them into final judgments.
5. Envelope merge; `human_review.role` required (e.g. Safety Physician).

## Exceptions

| Case | Behaviour |
|---|---|
| AI-disabled / kill switch | Deterministic `core` only; PV manual continuity noted (INJ-082) |
| MedDRA version mismatch | Preserve versions; annotate conflict; no silent unify |
| Awareness date conflict | Preserve all clocks; no single “winning” date |
| Stale auth / bad tool | Fail closed on that path |

## Acceptance criteria

- [ ] No final PV decision fields in `core`
- [ ] Duplicate candidates only — no auto-merge
- [ ] Clock and terminology conflicts preserved
- [ ] `execution_status == not_executed`
