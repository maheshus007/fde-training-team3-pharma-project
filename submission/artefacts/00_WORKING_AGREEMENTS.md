# Working Agreements — Team 3 / Project AEGIS-PHARMA

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Product/value lead (custodian) |
| Version / date | 1.0 / 2026-08-10 |
| Status | Binding for all Phase 0–8 work |
| Related | `WORKSHOP_DEPLOYMENT_PLAN.md`; `PACKAGE_SCOPE_AND_ASSUMPTIONS.md`; `submission/artefacts/00_TEAM_CHARTER.md` |

## WA-01 Facilitator independence

Teams must not depend on hidden answer keys, private credentials, later injects or undocumented oral instructions (`WORKSHOP_DEPLOYMENT_PLAN.md` facilitator-independent rule; `PACKAGE_SCOPE_AND_ASSUMPTIONS.md` “all 84 injects disclosed”). If an instruction is not in the local package or `submission/` artefacts, it has no force.

## WA-02 Assumptions must be logged

Any assumption required to proceed must be recorded in `submission/artefacts/ASSUMPTIONS_AND_DECISION_LOG.md` with owner, evidence path, status and invalidation trigger before the dependent work continues. Silent assumptions are treated as defects.

## WA-03 Preserve contradictions; govern resolution

The case intentionally contains conflicting identifiers, versions, timestamps, authorities, quality states, terminology and priorities (`PACKAGE_SCOPE_AND_ASSUMPTIONS.md` deliberate ambiguity; INJ-002; INJ-023; INJ-038). Do not “clean” contradictions without preserving source evidence and recording a governed resolution (decision ID, authority, effective time). Records marked `referenced_missing`, `untrusted`, `draft`, `superseded` or `unknown` are challenge conditions, not packaging defects.

## WA-04 Immutable challenge evidence

Never modify `case/`, `data/`, `knowledge/`, `source_documents/`, `evaluation/`, `requirements/`, `starter/` or `templates/`. All participant work stays under `submission/`. Never fabricate, overwrite or silently normalize regulated evidence fields (source, authority, effective date, version, time precision, unit, verbatim value, uncertainty).

## WA-05 Deny-by-default authorization

At execution time, check current user, purpose, object, role and tool authorization. Stale entitlement caches (INJ-067), unsigned/poisoned tools (INJ-066), hash-mismatched models (INJ-070) and untrusted documents containing instructions (INJ-065) are denied or treated as untrusted data, not executable policy.

## WA-06 No prohibited autonomous decisions

Automation may reconcile, cite, flag, abstain, extract, normalize, cluster and generate options. Automation must never release/reject/reprocess/recall a batch; make final PV seriousness/causality/expectedness/reportability/signal confirmation; or reserve/allocate/ship/initiate recall (`data/ai_use_boundaries.csv`; INJ-006; scoring hard gates).

## WA-07 AI-disabled continuity required

Each mandatory workflow must retain a safe manual/deterministic path for model unavailability (INJ-082; `data/continuity_requirements.csv`: batch_review and supply_planning 14-day AI outage tolerance; pv_intake manual runbook required with zero-hour AI outage tolerance for expedited paths). Evaluation lead blocks demos that lack this path.

## WA-08 Offline deterministic mode first

Prefer contracts, fixtures and tests that run without network, cloud keys or live model inference (`PACKAGE_SCOPE_AND_ASSUMPTIONS.md`). Model inference, if used later, is additive behind budgets, checkpoints, rollback and kill switch — never the only path to a correct result.

## WA-09 Tests before inference; evidence after changes

Create deterministic tests before enabling model inference for a capability. Every material requirement must trace to a test and an evidence artefact under `submission/`. Structure-checker forbidden tokens (empty guidance stubs) are banned from submission prose.

## WA-10 Independent review before defence claims

Claims about safety, quality, privacy or scoring readiness require a reviewer who did not author the claim. Product may not override GxP/security vetoes on hard-gate issues.

## WA-11 Communication and escalation

- Raise blockers within one working session of discovery.
- Escalate role conflicts using the charter matrix (Manufacturing vs Quality; Privacy vs retention; Procurement vs architecture substitutability per `case/STAKEHOLDER_PACK.md`).
- Document overrides with actor, reason, time and rollback condition.

## WA-12 Definition of done for agreements

Agreements are met when another qualified team can reproduce the environment, execute public tests, inspect evidence, operate the manual fallback and defend a go / conditional-go / pivot / pause / stop recommendation without oral knowledge from the builders (`case/INTEGRATED_CASE.md` §9).
