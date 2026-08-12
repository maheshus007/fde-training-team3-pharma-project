# PRD — Agentic Assist for AEGIS-PHARMA

**Question this file answers:** What problem are we solving?

| Field | Entry |
|---|---|
| Version / date | 1.0 / 2026-08-12 |
| Audience | Product, stakeholders, GxP/Security leads |
| Status | Draft for implementation |
| Related | `submission/artefacts/04_PRODUCT_SERVICE_BLUEPRINT.md`; `data/ai_use_boundaries.csv` |

## Problem

NovaCura reviewers assemble conflicting evidence across LIMS, MES/eBR, QMS, safety DB and IRT under time pressure. Manual reconciliation is slow; unconstrained AI risks silent invention and prohibited regulated actions.

## Users

| Persona | Job | Outcome (not decision) |
|---|---|---|
| Batch evidence reviewer / QP support | Assemble cited release-packet evidence | Readiness assessment with gaps |
| PV intake specialist | Intake, cluster, clock/terminology flags | Human-ready case file |
| Supply planner | Draft shortage / cold-chain options | Ranked draft options |
| Control reviewer | Verify abstentions, denials, tool trust | Gate evidence |

## Goals

1. Faster assembly of cited review packs.
2. Explicit contradictions, gaps and abstentions (never silently normalized).
3. Audited assist trail when agent mode is engaged.
4. Continuity when AI is disabled.

## Non-goals

- Batch release / reject / reprocess / recall
- Final PV causality / seriousness / expectedness / reportability / signal confirmation
- Reserve / allocate / ship / quality-status change / recall initiation
- Clinical eligibility determination
- Replacing human accountability

## Success metrics

| Metric | Target |
|---|---|
| Package contract validation of `core` | Pass |
| Prohibited-action tests | Pass (fail-closed) |
| Trajectory length | ≤ 25 steps |
| `execution_status` | Always `not_executed` |
| Default demo path | AI-disabled, agent not engaged |
| S08 security/trajectory expectations | Covered by automated tests |

## Binding evidence

- `data/ai_use_boundaries.csv` (INJ-006)
- INJ-066 tool poison; INJ-067 stale auth; INJ-070 model hash; INJ-080 trajectory; INJ-082 continuity

## Deliberately omitted here

Workflows detail, APIs, schemas, package layout, prompts — see feature, technical and architecture specs.
