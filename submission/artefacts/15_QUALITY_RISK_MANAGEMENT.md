# Quality Risk Management

> Participant working artefact for Project AEGIS-PHARMA. ICH Q9-style critical thinking applied to the three advisory workflows; hazards include automation bias (INJ-071), omitted evidence and unit conversion (INJ-024).

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — GxP / quality lead |
| Version / date | 1.0 / 2026-08-10 |
| Reviewers | Domain/evidence lead; Product/value lead; Security/privacy lead |
| Status | Reviewed |
| Related requirements / ADRs | Artefacts 13–14; ADR-003, ADR-004, ADR-006, ADR-009; INJ-006, INJ-024, INJ-071 |

## Purpose

Perform quality risk management for Workflows A–C so that automation reduces reconciliation friction without increasing the likelihood that humans accept incomplete, unit-corrupted or decision-shaped outputs.

Accountable owner: GxP / quality lead. Completion criteria: risk question, hazard analysis, failure chains, controls, residual risk, acceptance and review triggers are documented for the three workflows.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-451 | `case/INTEGRATED_CASE.md` INJ-071; `data/candidate_outputs.csv` | Case / human-factors inject | Reviewers may accept AI summaries that omit critical deviations | Narrative + synthetic feedback |
| E-452 | Diagnostics / `data/interface_mappings.csv` INJ-024 | Unit mapping defect | Unapproved µg/mL vs mg/L style conversions | Baseline diagnostics confirm defect class |
| E-453 | `data/ai_use_boundaries.csv` | INJ-006 | Prohibited autonomous decisions | Binding |
| E-454 | `data/kpi_conflicts.csv` | INJ-002 | Speed incentives vs quality completeness | Conflicting KPIs |
| E-455 | `knowledge/AI_GXP_BOUNDARY.md` (K-003) | Effective 2026-05-01 | Decisions reserved to authorized roles | Synthetic policy |
| E-456 | DMAIC FM-1..FM-4 | `02_DMAIC_WORKBOOK.md` | Prior failure modes including automation bias and units | Team artefact |

## 1. Risk question and scope

**Risk question:** What is the risk to product quality, patient safety, trial integrity and regulated record trustworthiness if AEGIS-PHARMA produces or presents advisory outputs for batch evidence, PV intake and supply options?

**In scope:** Advisory software behaviour, human-review interaction, evidence integrity, units/identity/time, continuity under AI-disabled mode.

**Out of scope for this QRM:** Changing registered specifications; validating brownfield LIMS/MES/QMS themselves; autonomous execution paths (architecturally excluded, monitored as hazard if they reappear).

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Risk to be managed | Incorrect or incomplete advice that a pressurized reviewer accepts | GxP | §§2–4 |
| Risk not transferred to AI | Final disposition/PV/supply execution | GxP (E-453, E-455) | Contract tests |

## 2. Hazard analysis

| Hazard ID | Workflow | Hazard | Harm |
|---|---|---|---|
| H-01 | A batch | Omitted critical deviation in summary (INJ-071) | Inappropriate release decision by human |
| H-02 | A batch | Silent or unapproved unit conversion (INJ-024) | Wrong potency/impurity interpretation |
| H-03 | A batch | Genealogy/identity contradiction suppressed | False readiness |
| H-04 | B PV | Final causality/reportability emitted by system | Unlawful/unqualified safety conclusion |
| H-05 | B PV | Clock/timezone coercion without provenance | Missed expedited reporting window |
| H-06 | B PV | Duplicate cases merged incorrectly | Undercounting / overcounting |
| H-07 | C supply | Side-effectful reservation/allocation | Stock moved without governance |
| H-08 | C supply | Option set omits quality hold / ethical constraint | Patient access or quality harm |
| H-09 | All | Stale entitlement allow | Privacy / GxP access breach |
| H-10 | All | Automation bias under KPI speed pressure (INJ-002 + INJ-071) | Systematic under-review |
| H-11 | All | Untrusted document treated as policy | Incorrect controlled procedure application |
| H-12 | All | AI-only path during outage | Continuity failure or unsafe improvisation |

## 3. Failure chains

**FC-A (batch readiness):** Unapproved unit map (H-02) + genealogy break (H-03) + AI summary omits deviation (H-01) + reviewer under schedule pressure (H-10) → human releases on incomplete pack. **Breaks:** unit abstention; contradiction engine; forced evidence view; disposition field impossible in contract.

**FC-B (PV):** Multilingual narrative + duplicate ambiguity (H-06) + system emits `final_reportability` or `causality_assessment` (H-04) → premature regulatory posture. **Breaks:** schema denial of final PV fields; required_reviews list; human Safety physician decision.

**FC-C (supply):** Shortage urgency + draft option with hidden quality hold (H-08) + `reservation_id` accepted (H-07) → stock reserved without Quality. **Breaks:** `no_side_effects: true`; additionalProperties denial; approvals_required surfacing.

## 4. Risk controls

| Hazard | Preventive control | Detective control | Corrective / governance |
|---|---|---|---|
| H-01 / H-10 | Forced critical-deviation list before acknowledgement | Unscripted bias drills; audit of acknowledgements | GxP veto on “ready” UX that hides gaps |
| H-02 | Approved mapping only; else abstain | Contract/unit tests | Change-controlled mapping update |
| H-03 | Contradiction preservation (WA-03) | Readiness ≠ ready when conflicted | Human resolves under QMS |
| H-04 | Schema + prohibited field reject | Negative PV fixtures (reportability + causality) | Defect = critical |
| H-05 | Clock evidence array; no silent TZ coerce | PV clock fixtures | PV assessor confirms |
| H-06 | Duplicate candidates, not merges | Precision review metrics | Human merge decision |
| H-07 | `no_side_effects` const; no write tools | Negative supply fixtures | Security tool deny |
| H-08 | Constraints + quality_holds required arrays | Shortage constraint fixtures | Supply governance board |
| H-09 | Execution-time authZ re-check | Stale cache tests | Deny-by-default |
| H-11 | Authority-checked retrieval | Untrusted knowledge tests | Abstain/escalate |
| H-12 | Kill switch + AI-disabled runbooks | Continuity drill | Evaluation gate |

## 5. Residual risk and uncertainty

| Residual risk | Why remains | Uncertainty |
|---|---|---|
| Reviewer still skims forced list | Human factor cannot be engineered to zero | Medium — depends on training and UI |
| Fixture gaps miss a real contradiction class | POC evidence incomplete vs live brownfield | Medium — R-401 |
| Inference phrasing nudges judgement | Even without prohibited fields | Medium — mitigated by dual-path and budgets |
| KPI pressure reopens bias | Organizational (E-454) | High organizational; medium technical |

No residual risk acceptance authorizes prohibited automated actions.

## 6. Risk acceptance

| Statement | Decision | Owner | Date |
|---|---|---|---|
| Residual human skimming risk accepted for POC with forced evidence control and training note | Conditionally accepted | GxP | 2026-08-10 |
| Residual fixture-vs-live adapter gap accepted for offline defence | Conditionally accepted | Architecture + GxP | 2026-08-10 |
| Any acceptance of prohibited-field pass or silent unit convert | Not acceptable | GxP | 2026-08-10 |

## 7. Review triggers

| Trigger | Action |
|---|---|
| INJ-071 demonstration failure | Reopen H-01/H-10; strengthen UX/tests |
| New unit mapping source | Revalidate H-02 controls |
| Schema change | Re-run fail-closed suite; update this QRM |
| Continuity drill fail | Reopen H-12 |
| KPI policy change removing Quality independence pressure | Reassess H-10 likelihood |
| Evidence-model change | Refresh identity/authority hazards |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-451 | Assumption | Workshop unscripted drills sufficiently evidence INJ-071 control for scoring | Human-factor score risk | Evaluation | Defence | Open |
| R-452 | Gap | Quantitative severity/probability scores not mandated by package; qualitative QRM used | Comparability | GxP | Examiner preference | Accepted |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| QRM covers three workflows | §§2–4 | Review | This artefact | Accepted |
| Automation bias (INJ-071) controlled | Forced evidence; FC-A break | Unscripted + payload tests | E-451 | Design accepted |
| Unit conversion (INJ-024) controlled | Abstain without approved map | Deterministic tests | E-452 | Design accepted |
| Omitted evidence hazard controlled | Contradiction + gaps arrays; readiness rules | Contract + scenario tests | FC-A | Design accepted |
| Prohibited actions fail closed | Schema denial | `test_workflow_contracts.py` | E-453 | Tests green |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Domain/evidence lead | Reviewer | Add genealogy contradiction hazard | H-03 | 2026-08-10 |
| Product/value lead | Reviewer | Link KPI pressure to automation bias | H-10 / E-454 | 2026-08-10 |
| Security/privacy lead | Reviewer | Include entitlement and untrusted doc hazards | H-09, H-11 | 2026-08-10 |
