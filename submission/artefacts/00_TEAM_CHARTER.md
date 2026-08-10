# Team Charter — Team 3 / Project AEGIS-PHARMA

| Field | Entry |
|---|---|
| Organisation context | NovaCura Therapeutics Group (NTG) — fictional sponsor (`case/INTEGRATED_CASE.md`) |
| Capstone product | Project AEGIS-PHARMA three mandatory workflows |
| Version / date | 1.0 / 2026-08-10 |
| Status | Approved for Phase 0–1 work |
| Related evidence | `WORKSHOP_DEPLOYMENT_PLAN.md`; `requirements/SCORING_MODEL.md`; `case/STAKEHOLDER_PACK.md` |

## 1. Purpose

Team 3 designs, builds and defends an offline-capable AI Forward Deployed Engineering intervention that reduces evidence-reconciliation friction across Quality, Pharmacovigilance and Supply without transferring regulated human accountability to automation (`case/INTEGRATED_CASE.md` §§3–5; INJ-006; `data/ai_use_boundaries.csv`).

Completion criteria for this charter: every role has named decision rights, independent review paths are visible, working agreements are enforceable without a facilitator, and scoring hard gates are understood by all members.

## 2. Roles (workshop plan alignment)

Roles match `WORKSHOP_DEPLOYMENT_PLAN.md` recommended team roles. One person may hold multiple roles; decision rights and independent review remain distinct.

| Role | Primary accountability | Decision rights | Independent of |
|---|---|---|---|
| Product / value lead | Problem framing, no-AI comparison, value hypothesis, benefits realisation | Scope inclusions/exclusions for the three workflows; stop/pivot recommendation drafting | Build implementation choices |
| Domain / evidence lead | Source authority, inject mapping, evidence registers, contradiction preservation | Which evidence is cited vs abstained; lineage completeness criteria | Product marketing claims |
| Architecture / integration lead | C4, contracts, bounded contexts, offline deterministic mode | Interface contracts, idempotency keys, tool boundaries | Final GxP risk acceptance |
| GxP / quality lead | Validation state, CSA/GxP relevance, quality risk, release-packet integrity | Risk acceptance for quality-system controls; veto on disposition automation | Manufacturing throughput pressure (INJ-002) |
| Security / privacy lead | Threat model, entitlements, tool trust, privacy/ethics, residency | Deny-by-default on stale entitlements, untrusted docs, poisoned tools | Convenience or vendor concentration preferences |
| Evaluation / reliability lead | TEVV, scorecards, FinOps measures, outage/continuity evidence | Release gates for demo/defence; AI-disabled continuity acceptance | Feature completeness pressure |
| Build lead | Implementation under `submission/`, fixtures, tests, runbooks, evidence export | Engineering sequencing within approved contracts | Regulatory conclusions reserved to domain/GxP owners |

## 3. Decision rights and segregation

| Decision class | Accountable | Must consult | Independent review / veto |
|---|---|---|---|
| Expand scope beyond Workflows A–C | Product/value | All leads | GxP/quality + Security/privacy |
| Treat a record as authoritative | Domain/evidence | Architecture, GxP | GxP/quality when release/safety-relevant |
| Allow write-capable tool or status change | Architecture + Security | GxP, Build | Security/privacy (hard deny if write enables prohibited action) |
| Accept residual quality/PV/supply risk for defence | GxP/quality | Product, Evaluation | Matches `case/STAKEHOLDER_PACK.md` Quality / QP / PV mandates |
| Ship demo with AI enabled | Evaluation/reliability | Build, Security | Evaluation may block if tests or continuity path fail |
| Log assumption vs pause work | Any role may raise | Product/value | Facilitator-independent: assumption must be written before proceeding |

Hard rule from INJ-006 / `data/ai_use_boundaries.csv`: no role may authorize autonomous formulation change, specification change, clinical eligibility determination, safety case disposition, batch release/reject/reprocess/recall, or stock reserve/allocate/ship.

## 4. Independent review

- Every material artefact in `submission/artefacts/` requires at least one reviewer who did not draft the primary content for that section.
- Prohibited-action and entitlement tests are designed by Evaluation/security and cannot be waived by Build alone.
- Conflicts between Manufacturing throughput (INJ-002; ST-02) and Quality evidence completeness (ST-01) escalate to GxP/quality lead with Product documenting the trade-off; automation never resolves the conflict silently.
- Privacy vs retention conflicts (INJ-035, INJ-061) escalate to Security/privacy with GxP consulted; deletion is never automated against GxP holds.

## 5. Working agreements (summary)

Full text: `submission/artefacts/00_WORKING_AGREEMENTS.md`.

1. Facilitator-independent: no reliance on hidden keys, private credentials, later injects or undocumented oral instructions (`WORKSHOP_DEPLOYMENT_PLAN.md`).
2. Assumptions must be logged before they unblock work.
3. Contradictions in challenge data are preserved; cleaning requires governed resolution.
4. AI-disabled continuity path is mandatory for all three workflows (INJ-082).
5. Challenge evidence outside `submission/` is immutable.

## 6. Scoring understanding

From `requirements/SCORING_MODEL.md`:

- 180-point model across discovery, product, DMAIC, architecture, data integrity, three-workflow quality, GxP, security, privacy, evaluation, FinOps, reliability, operating model and defence.
- Phase 0–1 primarily loads Discovery (10), Product proposition (10) and DMAIC/value (10).
- Unconditional pass is impossible if hard gates are breached (autonomous regulated decisions; lost provenance; silent unit conversion; revoked entitlements/untrusted instructions; missing manual outage path; non-reproducible package; omitted material subgroup/privacy/GxP risks).

Team 3 optimizes for hard-gate survival first, then evidence-backed scoring areas.

## 7. Checkpoints adopted

Aligned to workshop hours:

| Checkpoint | Focus | Owners |
|---|---|---|
| Hour 7 | Problem and no-AI qualification | Product, Domain |
| Hour 12 | Authority, identity, time, unit, lineage | Domain, Architecture, GxP |
| Hour 18 | Architecture and prohibited-action contracts | Architecture, Security, Evaluation |
| Hour 26 | Three-workflow demonstration | Build, Evaluation |
| Hour 34 | Red-team, outage, cost gates | Security, Evaluation |
| Hour 38 | Clean-room handover rehearsal | All |

## 8. Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Domain/evidence lead | Independent of Product draft | Confirm INJ-001..006 cited as Phase 1 drivers | Accepted | 2026-08-10 |
| GxP/quality lead | Independent of Build | Confirm no disposition authority granted to any role via automation | Accepted | 2026-08-10 |
