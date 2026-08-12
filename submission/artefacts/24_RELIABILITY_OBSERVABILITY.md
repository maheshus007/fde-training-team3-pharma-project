# Reliability and Observability

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — AEGIS-PHARMA capstone (individual names/roles pending; see A-001 in `01_BUSINESS_CASE.md`) |
| Version / date | v0.1 draft — 2026-08-07 |
| Reviewers | Pending team review |
| Status | Draft |
| Related requirements / ADRs | INJ-069, INJ-079, INJ-081, INJ-082; continuity_requirements.csv |

## Purpose

Defines critical journeys, SLIs/SLOs, lineage and fallback behaviour given an **open** AI regional outage and a prior ransomware containment event. Accountable owner: platform SRE / CQO. Completion criteria: AI-disabled continuity is mandatory, not optional; unsafe model fallback is forbidden.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-2401 | `data/downtime_events.csv` | Incident log | DT-1 ransomware containment MES/QMS/historian 16h; DT-2 AI primary region outage start 2026-08-01T01:00Z, end=**open** | INJ-069, INJ-079 |
| E-2402 | `data/model_endpoints.csv` | Endpoint register | primary_large down; fallback_small available | Unsafe-fallback temptation |
| E-2403 | `data/continuity_requirements.csv` | Continuity policy data | batch_review max_ai_outage_days=14, manual_runbook=required; pv_intake max_ai_outage_hours=**0**, manual_runbook=required; supply_planning 14 days | PV has zero AI outage tolerance for AI-dependent path → must have non-AI path always |
| E-2404 | `data/cost_model.csv` | Cost model | observability $31,000/month | Budget exists; capability quality unknown |
| E-2405 | PUB-10 evaluation | evaluate.py | reliability fixture recorded `not_implemented` for endpoint failover code | Honest gap |
| E-2406 | `submission/evaluation/datasets/S12_model_substitution_outage_rollback.json`; `runbooks/AI_DISABLED.md` | Participant TEVV / ops | Outage/rollback/manual-mode suite + AI-disabled runbook filed | Drill evidence still open (R-2501) |

## 1. Critical user journeys

| Journey | Reliability need | Evidence |
|---|---|---|
| Batch evidence pack for QP | Must work with AI down within 14 days via manual runbook | E-2403 |
| PV intake | AI outage budget **0 hours** if path is AI-dependent → deterministic/manual path must be default-capable | E-2403 |
| Supply options | 14-day AI outage tolerance with manual runbook | E-2403 |
| Gate decisions (auth/purpose/tokens) | Must not fail open during partial outage | Artefact 16 |

## 2. SLI/SLO and error budgets

| SLI | Proposed SLO (POC) | Notes |
|---|---|---|
| Deterministic workflow success (schema-valid response or controlled abstention) | ≥ 99% of assessed runs | Measured by test/evaluate |
| Gate fail-closed rate on known abuse fixtures | 100% | SEC/checkpoint/privacy |
| Unsafe model selection rate | 0% | Gateway |
| AI inference availability | N/A while inference disabled | DT-2 open (E-2401) |
| Error budget | Any unsafe selection or side effect = immediate budget burn to zero | — |

## 3. Logs, metrics and traces

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Minimum log fields | request_id, user, purpose, affiliate, model_id or `none`, gate outcomes, input_hash, contract_version, abstention reason | Capstone team | evaluate.py record shape |
| Metrics | deny rates by gate; tokens/request; checkpoint age rejects; fixture pass/`not_implemented` counts | Capstone team | E-2404 budget implies metrics exist at vendor — export gap in artefact 27 |
| Gap | No distributed tracing implementation in POC. | Capstone team | Gap R-2401 |

## 4. Data/model/prompt/tool lineage

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Model lineage | registry_hash vs deployed_hash + signature (artefact 10/16) | Capstone team | model_artifacts.csv |
| Tool lineage | approved flag + manifest hash required before call (R-1604 open) | Capstone team | tool_catalog |
| Data lineage | cite sources in workflow outputs; preserve verbatim conflicts | Capstone team | workflow_* |

## 5. Capacity and backpressure

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Backpressure | Token cap; bounded agent steps (policy); refuse oversized loops | Capstone team | security_gates |
| MES timeout pattern | 7 retries without idempotency (artefact 12) — backpressure without idempotency is dangerous | Capstone team | interface_events |

## 6. Outage, fallback and recovery

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Current state | AI primary region outage open (E-2401); primary endpoint down (E-2402). | Platform | E-2401, E-2402 |
| Allowed fallback | Deterministic offline workflows + manual runbooks (E-2403). | Capstone team | E-2403 |
| Forbidden fallback | Auto-switch to any model failing integrity / out of validated scope — even if endpoint “available.” | Capstone team | ADR-006/007; E-2405 |
| OT ransomware | Separate continuity for MES/QMS (E-2401 DT-1); AI cannot compensate for OT loss. | CISO / Ops | E-2401 |

## 7. Alerting and evidence retention

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Alert on | endpoint down, integrity mismatch, gate bypass (should be impossible), budget exceed, open downtime > SLO | Platform | E-2401–E-2403 |
| Retain | gate/decision evidence per retention_rules; AI prompt logs 90d unless hold | DPO / CQO | artefact 17 |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-2401 | Gap | No tracing/metrics backend in submission | Medium | Capstone team | Before production claim | Open |
| R-2402 | Gap | PUB-10 failover selector not coded | Medium | Capstone team | Code backlog | Open |
| R-2403 | Risk | Operators may enable fallback_small without scope/integrity checks during DT-2 | High | Platform | While DT-2 open | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| AI-disabled path exists | deterministic workflows | run.py / tests | E-2403 | PASS (POC) |
| Safe endpoint failover | endpoint selector | PUB-10 | E-2405 | not_implemented |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Pending | Platform SRE | — | — | — |
