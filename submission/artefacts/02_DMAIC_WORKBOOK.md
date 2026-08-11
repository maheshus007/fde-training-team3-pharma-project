# DMAIC Workbook

> Participant working artefact. DMAIC frames the three mandatory AEGIS-PHARMA workflows against NovaCura evidence and injects INJ-001..006 as Phase 1 drivers, with later injects informing failure modes.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Product / value lead with Domain/evidence lead |
| Version / date | 1.0 / 2026-08-10 |
| Reviewers | Evaluation/reliability lead; GxP/quality lead |
| Status | Reviewed |
| Related requirements / ADRs | INJ-001..006; business case D-001..D-005; continuity INJ-082 |

## Purpose

Define, measure, analyse, improve and control the evidence-reconciliation problem so that Team 3 can compare AI-assisted and no-AI paths, select bounded improvements, and prevent regression into prohibited autonomous decisions.

Accountable owner: Product/value lead. Completion criteria: each DMAIC phase has evidence-cited answers, owners and acceptance evidence; failure modes cover diagnostics findings and AI-use boundaries.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-101 | `case/INTEGRATED_CASE.md` §4 | Case mandate | Workflows A–C definitions and prohibitions | Narrative |
| E-102 | `data/board_requests.csv` BR-01 | Board | −14% release lead time constraint | Synthetic |
| E-103 | `data/no_ai_baselines.csv` | Process excellence (INJ-003) | Relative value/duration of repair vs rules vs genai | Estimates |
| E-104 | `data/kpi_conflicts.csv` | Functional KPIs (INJ-002) | Conflicting targets | Incomplete incentive model |
| E-105 | `data/ai_use_boundaries.csv` | Executive boundary (INJ-006) | Allowed vs prohibited actions | Binding |
| E-106 | `starter/baseline_diagnostics.py` output | Preflight 2026-08-10 | Stale cache; hash mismatch; unit mapping; untrusted knowledge | Obvious findings only |
| E-107 | `data/continuity_requirements.csv` | Continuity (INJ-082) | 14-day AI outage for batch/supply; PV manual required | Synthetic |
| E-108 | `case/STAKEHOLDER_PACK.md` | Stakeholder pack | Human-only QP/PV finals; deliberate conflicts | Qualitative |

## 1. Define

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| VOC / CTQ | Board wants faster release evidence assembly without weakening Quality (E-102). QP wants complete reliable release evidence (E-108). PV wants timely complete case handling without AI final decisions. Supply wants options under quality and ethics constraints | Product | Business case §1 |
| Process scope | Start: request for batch-review readiness, ICSR intake package, or shortage/cold-chain planning case. End: human-ready evidence pack / option set with abstentions — not disposition | Domain | E-101 |
| Out of process | Release/reject/reprocess/recall; final causality/seriousness/reportability; reserve/allocate/ship | GxP | E-105 |
| Problem statement | Evidence reconciliation across brownfield systems is slow and error-prone under inject stress (genealogy breaks, unit defects, duplicate ICSRs, cold-chain disputes), threatening BR-01 and inspection readiness while KPI owners conflict | Product | E-101, E-104, E-106 |
| Goal statement | Deliver offline demonstrators for Workflows A–C that reduce time-to-complete-evidence-pack and raise contradiction detection with zero hard-gate violations | Evaluation | Charter scoring section |

## 2. Measure

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Y metrics | Release-packet readiness cycle time (proxy for BR-01); PV intake packaging time; shortage option-set latency; abstention correctness; prohibited-action count (must be 0) | Evaluation | Scorecard later |
| X factors | Authority resolution time; unit-mapping approval state; entitlement freshness; document trust class; MedDRA/version alignment; genealogy completeness | Domain | Inject catalogue D04–D08 |
| Baseline signals already measured | Diagnostics: stale entitlement cache; model hash mismatch; unapproved unit mapping; untrusted knowledge present (E-106) | Security + Domain | `submission/evidence/PREFLIGHT_REPORT.md` |
| No-AI baseline measures | Use E-103 durations/value estimates as comparison anchors until fixture timers exist | Product | INJ-003 |
| Data quality note | Challenge data contains deliberate defects; measurement must count contradictions found, not “cleaned” rows | Domain | Package deliberate ambiguity |

## 3. Analyse

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Root causes (evidence-backed) | Fragmented systems and identity collisions (case §2; INJ-005, INJ-045); unapproved unit assumptions (INJ-024); authority/version conflicts (INJ-031, INJ-039, INJ-040); incentive conflict prioritizing speed over completeness (INJ-002); trust failures in tools/knowledge/models (INJ-065..070) | Domain | Inject map |
| Why AI is not the first root fix | Master-data and rules paths already claim 38% and 27% estimated value (E-103); many defects are contractual/authorization, not language tasks | Architecture | D-004 hybrid |
| Failure chain example | Unapproved unit mapping + genealogy break + automation bias (INJ-024, INJ-021, INJ-071) → false “ready for release” summary if disposition were automated — hence prohibition | GxP | E-105 |
| KPI conflict analysis | Optimizing Manufacturing 98% schedule alone increases Quality deviation risk; AEGIS metrics must include guardrails for RFT and Safety on-time (E-104) | Product | Business case D-005 |

## 4. Improve

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Improve-1 | Deterministic evidence graph/contracts: cite source, authority, effective time; refuse silent unit conversion | Architecture + Domain | Future data contracts |
| Improve-2 | Entitlement check at execution; ignore stale cache; deny poisoned tools and hash-mismatched models | Security | INJ-067, INJ-066, INJ-070 |
| Improve-3 | Human review queues with forced viewing of omitted critical deviations (counter INJ-071) | GxP + Product | Blueprint human touchpoints |
| Improve-4 | Optional bounded genai_assist for extraction/clustering/option narrative only after Improve-1..3 tests pass | Build + Evaluation | E-103 sequencing |
| Improve-5 | AI-disabled runbooks meeting E-107 continuity windows | Evaluation + Build | INJ-082 |

## 5. Control

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Process controls | Versioned structured outputs; additional-properties denial; idempotency keys; bounded steps; budgets; checkpoints; rollback; kill switch | Architecture | Case §5 |
| Quality controls | Independent Quality risk acceptance; no AEGIS write to disposition fields | GxP | E-105, E-108 |
| Monitoring | Prohibited-action attempts, abstention rate, entitlement denials, token/cost spikes (INJ-076), outage failover success | Evaluation + Security | Later observability artefact |
| Response | On model outage or hash mismatch, switch to deterministic/manual path without degraded safety | Build | E-107 |
| Documentation | Assumptions/decisions log kept current; contradictions preserved | Domain | WA-02, WA-03 |

## 6. Failure modes and verification

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| FM-1 Silent unit conversion | Interface assumes µg/mL vs mg/L (INJ-024) | Domain | Reject unapproved mapping; test required |
| FM-2 Stale entitlement allows write | Cache after IAM revoke (INJ-067) | Security | Execution-time authz test |
| FM-3 Untrusted PDF instructs ignore holds | INJ-065 | Security | Treat as data; never as policy |
| FM-4 Automation bias omits deviation | INJ-071 | GxP | Reviewer checklist + forced evidence list |
| FM-5 Agent duplicates reservations | INJ-080 | Architecture | Idempotency; no reserve tools in scope |
| FM-6 AI unavailable 14 days | INJ-082 | Evaluation | Manual runbook drill |
| Verification approach | Deterministic tests before inference; adversarial fixtures for injects; hard-gate suite blocks defence if any prohibited action succeeds | Evaluation | Scoring hard gates |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-101 | Gap | Quantitative NTG cycle-time baseline not in package | BR-01 % attribution uncertain | Product | Use fixture timers as proxy | Open |
| R-102 | Risk | Improve-4 genai added before Improve-1..3 | Hard-gate failure | Evaluation | Gate on test suite | Open |
| R-103 | Assumption | Diagnostics four findings are representative starters | Missed inject interactions | Domain | Full inject mapping Phase 2+ | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Define three workflows with prohibitions | Scope control | Contract tests | E-101, E-105 | Accepted |
| Measure using board + diagnostics | Metrics plan | Preflight report | E-102, E-106 | Accepted |
| Improve hybrid no-AI-first | Deterministic mode | Baseline comparison | E-103 | Accepted |
| Control AI-disabled path | Continuity runbooks | Outage drill | E-107 | Planned |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Evaluation/reliability lead | Reviewer | Required continuity metrics in Control | Added E-107 controls | 2026-08-10 |
| GxP/quality lead | Reviewer | Required automation-bias failure mode | Added FM-4 | 2026-08-10 |

## Prompt 08 thin Improve notes (2026-08-11)

1. **Token/retrieval caps:** max 3 inference calls, 2048 tokens, T=0, CQ-id allowlist, purpose filters on graph.  
2. **No blind model retry:** invalid JSON discarded; rules continue; no retry loop without diagnosis.  
3. **Control metrics:** NFR-01..16 (latency, budgets, schema 100%, prohibited=0, tests without Azure keys).  
4. **Open ambiguities that would waste build:** Azure deployment name (cloud demo only); CAPA auto-link blocked; INJ-044 out of scope.

## Prompt 10 thin Improve sequencing (2026-08-11)

1. **Must-fix / Measure-first:** T-001 enum; T-002 health envelope; T-003 stubs; T-004 authz+purpose; T-005..T-008 graph/CQ/ontology **green on GraphPort/ontology modules** before engines (do not wait for T-013).  
2. **Deferred Overproduction / Model waste:** live Azure/Cosmos (T-014/T-015 live); CAPA auto-link; INJ-044; WCAG AA; inspection export FR-X-05; legal-hold delete API.  
3. **Assumption tests:** CQ-1/2/3/6 on assessment GraphPort; CQ-5 IDMP non-merge; CQ-8/9 via existing tool_trust + authz tests — reduce “KG/auth works” Unknown before cloud.  
4. **Waiting:** T-014/T-015 live wait on credentials — not on evidence pack. INJ-070 hash pin is assessment-testable without live Azure (mismatch → stub).

Full Prompt 09 DOWNTIME register is still pending; this lens is sequencing only. Structural reopen = **cleared** (artefacts 10/11).
