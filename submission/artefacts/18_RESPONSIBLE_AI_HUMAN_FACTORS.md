# Responsible AI and Human Factors

> Participant working artefact for Project AEGIS-PHARMA. Complements RAPID rights in artefact 03 and blueprint human touchpoints.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Product / value lead (custodian); GxP/quality lead (human-factors controls) |
| Version / date | 1.1 / 2026-08-10 |
| Reviewers | Security/privacy lead; Evaluation/reliability lead |
| Status | Reviewed |
| Related requirements / ADRs | INJ-071..074; WA-06; D-402; blueprint forced evidence view |

## Purpose

Design human accountability, anti-automation-bias controls, language equity, accessibility, role-conflict handling, contestability and emergency stop so AEGIS remains assistive under BR-01 schedule pressure.

Accountable owners: Product (UX accountability) and GxP (regulated review behaviour). Completion criteria: each listed inject has a control and acceptance path; emergency stop and contestability are operable without model inference.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-1801 | `case/INTEGRATED_CASE.md` INJ-071..074 | Case inject catalogue | Human-factor failure modes | Narrative |
| E-1802 | `data/candidate_outputs.csv`; `data/reviewer_feedback.csv` | INJ-071 | Reviewers accept AI summary omitting critical deviation | Synthetic |
| E-1803 | `data/model_performance.csv`; `data/icsr_cases.csv` | INJ-072 | Arabic/Hindi extraction quality below EN/DE | Synthetic metrics |
| E-1804 | `data/usability_findings.csv` | INJ-073 | Keyboard incomplete; colour-only warnings | Challenge condition |
| E-1805 | `data/stakeholders.csv`; `data/decision_rights.csv` | INJ-074 | Global process owner vs local QP/safety legal accountability | Synthetic |
| E-1806 | `submission/artefacts/04_PRODUCT_SERVICE_BLUEPRINT.md` | Team artefact | Forced evidence view; accessibility requirements | Participant design |
| E-1807 | `submission/src/policy_guard.py` | Team control | Hard deny of prohibited autonomous actions | Code |

## 1. Human accountability

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Who decides? | Local QP / Safety officer / Supply planner retain Decide for regulated outcomes; AEGIS Recommend/Input only | GxP (D-002) | Artefact 03 |
| System accountability | Architecture and Security accountable for deny-by-default and audit completeness | Security | Artefact 16 |
| Non-delegable | Batch disposition; final PV judgements; allocate/ship/recall | GxP | E-1807; prohibited tests |

## 2. Automation bias and contestability

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Threat (INJ-071) | Reviewers accept AI summary that omits critical deviation | Fact | E-1802 |
| Control | Forced evidence view: critical deviations and contradictions must be acknowledged before readiness acknowledgement | GxP + Product | E-1806 |
| Contestability | Any user with role may contest an AEGIS finding; contest opens human queue with immutable prior output preserved | Product | UX requirement |
| Acceptance | Candidate-output fixture with omitted deviation cannot be acknowledged without viewing deviation list | Evaluation | Later UI/acceptance test |

## 3. Uncertainty and abstention UX

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Principle | Abstention is a first-class outcome, not a failure message | Product | WA-08 |
| UX | Show reason codes (authority gap, unit conflict, stale auth, untrusted doc, language low confidence) | Product + Domain | Blueprint |
| Anti-pattern | Softening abstention into implied approval under BR-01 pressure | GxP veto | Charter |

## 4. Language/subgroup performance

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Fact (INJ-072) | Arabic and Hindi narratives show lower extraction quality than English/German | Case metrics | E-1803 |
| Control | Language-aware confidence thresholds; low-confidence → human-only path; never auto-finalize PV fields | Evaluation + PV | Subgroup gates later |
| Equity stance | Do not claim parity until subgroup metrics pass; schedule must not silence language risk | Product | Defence honesty |

## 5. Accessibility

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Fact (INJ-073) | Proposed interface fails full keyboard operation and uses colour-only warnings | Usability finding | E-1804 |
| Requirement | Full keyboard path; text+icon (not colour-only) status; contrast meeting agreed WCAG target for internal apps | Product + Build | E-1806 |
| Acceptance | Usability retest must clear keyboard and non-colour status before UI go claim | Evaluation | Later usability pack |

## 6. Training and competency

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Required competencies | Citation reading, abstention meaning, entitlement hygiene, multilingual caution, accessibility, automation-bias awareness | Product + Evaluation | Artefact 03 |
| Role conflict (INJ-074) | Global standardization may not override local legal Decide rights | GxP | E-1805; RAPID |
| Control | Jurisdiction-specific configuration; local QP/Safety veto preserved | Architecture + GxP | Artefact 03 |

## 7. Monitoring and feedback

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Monitoring | Automation-bias acknowledgements skipped; contest rate; language abstention rate; accessibility defects; emergency-stop activations | Evaluation | Observability later |
| Emergency stop | Kill switch disables inference and write-capable tool registration; deterministic/manual path remains | Architecture | WA-07; D-402 |
| Feedback loop | Reviewer disagreement on omitted deviations feeds regression fixtures | Evaluation | E-1802 pattern |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-1801 | Risk | Forced-view checklist becomes click-through habit | Bias returns | GxP | Defence rehearsal | Open |
| R-1802 | Gap | `submission/app` advisory UI exists; keyboard/a11y + forced-evidence study not yet evidenced | INJ-073 residual | Build | Before pilot | Open |
| R-1803 | Assumption | Synthetic language metrics directionally correct for gating design | Real languages differ | Evaluation | Measured eval | Accepted |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Counter automation bias (INJ-071) | Forced evidence acknowledgement | Candidate-output acceptance test (later) | E-1802, E-1806 | Design accepted |
| Language inequity (INJ-072) | Confidence routing / abstain | Subgroup metrics gate | E-1803 | Design accepted |
| Accessibility (INJ-073) | Keyboard + non-colour status | Usability retest | E-1804 | Requirements accepted |
| Role conflict (INJ-074) | Local Decide preserved | RAPID matrix | E-1805 | Design accepted |
| Contestability + e-stop | Contest queue + kill switch | Continuity / stop drills | D-402 | Decision recorded |
| No prohibited autonomy | policy_guard | `test_prohibited_actions.py` | E-1807 | Pass |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Security/privacy lead | Reviewer | Emergency stop must also drop poisoned tool path | Kill switch clears unapproved tools | 2026-08-10 |
| Evaluation/reliability lead | Reviewer | Language gates must be measurable | Pointed to model_performance.csv | 2026-08-10 |
