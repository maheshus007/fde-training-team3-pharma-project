# SCQA Narrative — Prompt 02

| Field | Entry |
|---|---|
| Narrative class | **decision-ready** |
| Evidence boundary | Challenge pack + Team 3 Phase 0–4 artefacts + Discovery register |
| Date | 2026-08-10 (revised after validation) |
| Prompt | `submission/prompts/02_scqa_minto.md` |

## Evidence boundary

May claim: case facts, CSV inject conditions, contract schemas, diagnostics findings, prior Team 3 decisions.  
Must not claim: measured −14% already achieved; production GxP validation complete; locked vendor/graph product.

## Situation

NovaCura Therapeutics Group runs fragmented GxP, PV and supply systems (LIMS, MES/eBR, QMS, safety DB, RIM, serialization, portals). Evidence for batch-review readiness, PV intake/signal-support and supply-shortage/cold-chain planning is split across inconsistent identifiers, clocks, units and authorities (`case/INTEGRATED_CASE.md` §2; `SOURCE_SYSTEM_FACT_PACK.md`). Project AEGIS-PHARMA must reduce reconciliation time while humans retain regulated accountability (case §§3–5).

## Complication

Board BR-01 demands −14% release lead time without changing specifications or weakening Quality authority (`board_requests.csv`). Concurrent inject pressure includes genealogy breaks (INJ-021), unit defects (INJ-024), PV duplicate/clock/listedness conflicts (INJ-037–040), cold-chain association disputes (INJ-051), and trust failures (stale auth, poisoned tools, untrusted docs — INJ-065–067, 070). KPI owners pull in incompatible directions (INJ-002). A no-AI path is a credible competitor (INJ-003). Autonomous optimization of disposition, final PV, allocation, formulation/specification or eligibility is prohibited (INJ-006) and is a scoring hard gate.

## Question

What bounded **capability** should Team 3 deliver so authorized reviewers can reconcile and cite conflicting evidence faster across Workflows A/B/C — with governed meaning (identity, unit, terminology, time, authority) and explainable multi-hop evidence — without transferring QP, PV or supply execution authority to automation?

## Answer (capability-level — not architecture lock-in)

Deliver a **bounded advisory evidence-reconciliation capability** for Workflows A/B/C that:

1. Assembles provenanced evidence packs with contradictions, gaps and abstentions;  
2. Enforces **semantic/domain rules** so identity, units, MedDRA/IDMP and clocks are not silently collapsed;  
3. Makes multi-hop relationships **citeable and reviewable** for humans;  
4. Supports optional assisted analysis only behind budgets, current authorization, fail-closed contracts and **mandatory HITL**;  
5. Preserves a **deterministic / AI-disabled** path that meets the same safety invariants.

**Architecture options** (offline evidence KG vs RER-only; agent orchestrator shape; inference adapter) are **deferred to DDD/C4/ADR** and remain provisional until validated — they are not part of this Answer’s lock.

### Desired outcomes / “good”

- Conflicts and gaps surfaced with citations, not silently resolved  
- Abstention when identity/unit/time/authority unresolved  
- Zero successful prohibited actions  
- Same core detections available with inference off  
- No-AI/rules baseline remains a first-class competitor (INJ-003)

### Audience / horizon / authority

- Audience: QP/QA, PV assessors, supply planners, examiners  
- Horizon: Phase 5–8 POC to defence (not production go)  
- Authority: humans Decide; system Reconciles / Advises only  

### Exclusions

Clinical eligibility automation; autonomous formulation/specification change; enterprise master-data cleanup as primary deliverable; cloud-only or secret-dependent runtime; autonomous disposition / final PV / allocate-ship-recall.

### Metrics (known vs Unknown)

| Metric | Status |
|---|---|
| Zero prohibited actions | Known gate |
| Contract schema compliance | Known |
| Correct abstention / conflict recall on golden injects | Fixture-based |
| BR-01 −14% contribution | **Unknown** until measured |
| Reviewer time saved | **Unknown** |
