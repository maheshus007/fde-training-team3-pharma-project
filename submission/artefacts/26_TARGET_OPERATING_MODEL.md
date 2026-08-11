# Target Operating Model

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — AEGIS-PHARMA capstone (individual names/roles pending; see A-001 in `01_BUSINESS_CASE.md`) |
| Version / date | v0.1 draft — 2026-08-07 |
| Reviewers | Pending team review |
| Status | Draft |
| Related requirements / ADRs | `03_STAKEHOLDER_DECISION_RIGHTS.md`; artefacts 18, 20, 24, 25 |

## Purpose

Defines how NovaCura would run the three bounded AI-support capabilities day-to-day: ownership, forums, run/change/control split, service management, governance of models/data/tools, competency and KPIs — without transferring regulated accountability to the model. Accountable owner: CQO / COO (role-played). Completion criteria: every capability has a named accountable human forum.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-2601 | `03_STAKEHOLDER_DECISION_RIGHTS.md` | Prior artefact | RACI for QP, PV, Supply Board, CISO, DPO | Carried forward |
| E-2602 | `data/ai_use_boundaries.csv` | Boundary register | Allowed/prohibited actions | Hard TOM constraint |
| E-2603 | `data/staff_rates.csv` + `data/cost_model.csv` | Cost evidence | Human review currently $0 in cost model despite real rates | TOM must fund review |
| E-2604 | `18_RESPONSIBLE_AI_HUMAN_FACTORS.md` | Prior artefact | Automation bias, a11y, competency gaps | Operating controls needed |
| E-2605 | `20_ISO42001_GOVERNANCE.md` | Prior artefact | AIMS-style control map | Governance spine |

## 1. Capabilities and ownership

| Capability | Accountable owner | Supporting |
|---|---|---|
| Workflow A — batch evidence support | EU QP (decision); Quality Ops (run) | Platform / AI engineering |
| Workflow B — PV intake support | PV / safety physician | Case intake ops |
| Workflow C — supply/recall-scope options | Supply Governance Board | Supply planning |
| Model gateway & gates | Platform owner; CISO for authz gates | Security engineering |
| Privacy rights / residency | DPO | Data stewards |
| Validation / CSA | Validation / CQO | Capstone→BAU transition |

## 2. Decision forums

| Forum | Decides | Cadence |
|---|---|---|
| Supply Governance Board | Allocation/recall-scope option approval | As needed / shortage |
| Quality release meeting | Whether AI packet is used in QP pack | Per batch |
| PV medical review | Final PV determinations (AI never) | Per case/signal |
| AI Change Board (proposed) | Model/tool/prompt/schema changes, integrity exceptions | Weekly / emergency |
| Incident command | Kill switch / resumption | Event-driven |

## 3. Run/change/control roles

| Lane | Who | Notes |
|---|---|---|
| Run | Site quality reviewers, PV intake, supply planners | Use drafts; escalate gaps |
| Change | Platform + Validation | Schema/model/tool changes via AI Change Board |
| Control | CQO, CISO, DPO, QP/PV/Board | Boundaries, audits, kill switch |
| Segregation | Builders do not self-approve validation; reviewers do not change model routing | Addresses INJ-074 pressure |

## 4. Service management

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Service classes | (1) Deterministic support — always on; (2) AI inference — disabled until CSA green; (3) Manual runbooks — mandatory per continuity_requirements | Platform / CQO | Artefact 24 |
| Support model | L1 site ops → L2 platform → L3 vendor (with concentration risk) | Platform | Artefact 27 |
| Funding | Human review must be budgeted (E-2603) | FinOps | E-2603 |

## 5. Model/data/prompt/tool governance

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Model | Integrity + validated scope before select; registry is SoR | Platform / Validation | ADR-006/007 |
| Data | Purpose, residency, consent live-check, ALCOA+ | DPO / Data | Artefacts 06/17 |
| Prompt/tool | Versioned; approved tools only; poisoned manifests rejected | Platform / CISO | Artefact 16 |
| Prompt logs | 90-day minimise unless hold | DPO | retention_rules |

## 6. Competency and training

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Required | AI-assisted review pitfalls (19s accept), abstention meaning, when to escalate, a11y obligations | CQO | E-2604 |
| Gap | No training records in challenge evidence — TOM requires creating them before pilot | CQO | Gap R-2601 |

## 7. KPIs and continuous improvement

| KPI | Direction | Anti-pattern |
|---|---|---|
| Evidence gaps surfaced before QP | Up | Hiding contradictions |
| Unsafe-accept rate / time-to-accept | Down / not minimised blindly | Racing the clock |
| Gate deny appropriateness | Monitor FPs/FNs | Disabling gates for throughput |
| Fixture regression | Zero new fails | Fake passes |
| AI outage continuity drills passed | Up | Paper runbooks only |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-2601 | Gap | Competency programme not instantiated | Medium | CQO | 0–30 day roadmap | Open |
| R-2602 | Assumption | AI Change Board can be stood up without new legal entity | Low | Capstone team | Handover | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Regulated decisions stay human | RACI + boundaries | Contract negatives | E-2601, E-2602 | PASS (design) |
| Review funded in TOM | Cost model correction | FinOps | E-2603 | Open (process) |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Pending | CQO / COO | — | — | — |
