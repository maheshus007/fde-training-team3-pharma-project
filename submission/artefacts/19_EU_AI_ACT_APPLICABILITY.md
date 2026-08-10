# EU AI Act Applicability

> Participant working artefact for Project AEGIS-PHARMA. Analysis is jurisdiction-scoped and assumption-bound; it is not legal advice and does not assert a notified-body conclusion.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — GxP / quality lead (applicability); Security/privacy lead (co-author) |
| Version / date | 1.1 / 2026-08-10 |
| Reviewers | Product/value lead; Architecture/integration lead |
| Status | Reviewed |
| Related requirements / ADRs | INJ-006; D-001, D-002, D-403; A-013, A-404..A-406; artefacts 16–18, 21 |

## Purpose

Record an evidence-based applicability analysis for AEGIS under the EU AI Act framing used in this synthetic programme: intended purpose, actor role, risk classification posture, obligations and change triggers — with residual legal uncertainty explicitly logged.

Accountable owner: GxP/quality lead. Completion criteria: advisory (non-autonomous) posture documented; high-risk autonomous decisioning excluded by design; assumptions and uncertainty recorded for defence.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-1901 | `case/INTEGRATED_CASE.md` §§4–5, §8 | Case authority | Human-retained Quality/Safety/allocation decisions; local legal accountability | Synthetic case |
| E-1902 | `data/ai_use_boundaries.csv` | Executive prohibition (INJ-006) | No release/PV final/allocate by AI | Binding programme boundary |
| E-1903 | `sources/LOCAL_REGULATORY_AND_STANDARDS_GUIDE.md` | Package guide | Intended/prohibited use, least privilege, fail-closed | Training guide, not counsel opinion |
| E-1904 | `submission/src/policy_guard.py` | Team control | Hard deny of prohibited actions | Code evidence |
| E-1905 | `PACKAGE_SCOPE_AND_ASSUMPTIONS.md` | Package scope | Offline synthetic package; participant freedom within hard gates | Workshop constraint |
| E-1906 | `submission/artefacts/03_STAKEHOLDER_DECISION_RIGHTS.md` | Team RAPID | Local QP/Safety Decide retained | Participant design |

## 1. Intended purpose and actor role

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Intended purpose | Assist NovaCura staff to reconcile evidence, package PV intake and generate supply options with citations and abstentions | Product (D-001) | Business case; blueprint |
| Explicit non-purpose | Autonomous batch disposition; final PV causality/seriousness/reportability; reserve/allocate/ship/recall | GxP (D-002) | E-1902, E-1904 |
| Actor role (assumption) | NovaCura (fictional) acts as deployer of an internal AI system; Team 3 builds a POC under workshop rules | Product + GxP | A-404 |
| Jurisdiction assumption | Primary analysis lens is EU deployer obligations for an EU-operated quality/safety support tool; other jurisdictions may add parallel duties | GxP | A-405; A-013 |

## 2. System and component boundary

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| In boundary | Orchestrator, retrieval, optional inference, policy_guard, UI review queues, audit export | Architecture | C4 / POC |
| Out of boundary | MES/LIMS/QMS systems of record write APIs for disposition; regulatory submission gateways; clinical eligibility engines | Architecture | D-001 scope |
| Human-in-the-loop | Required for all regulated outcomes; system outputs are advisory packets | GxP | E-1901, E-1906 |

## 3. Risk classification analysis

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Design posture | AEGIS is intentionally constrained to advisory support for regulated pharmaceutical workflows, not autonomous high-risk decisioning | GxP | E-1902 |
| Classification stance | Under the stated intended purpose and prohibitions, Team 3 treats the POC as requiring heightened governance and transparency, while asserting it does not perform autonomous decisions that determine batch release, PV reportability or allocation | GxP | D-403 |
| Residual uncertainty | Whether a future production expansion (e.g., scoring that effectively determines disposition without meaningful human review) would reclassify as high-risk remains unresolved without legal determination | GxP | R-1901 |
| Interpretation vs fact | Fact: programme forbids autonomous regulated actions. Interpretation: advisory + meaningful human review reduces high-risk autonomous-decision exposure. Assumption: meaningful human review remains real (not rubber-stamp) | GxP | Artefact 18 INJ-071 controls |

## 4. Prohibited/high-risk/transparency considerations

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Prohibited AI practices | No social scoring or biometric categorisation use cases in scope; not applicable to AEGIS workflows | Security | Scope D-001 |
| High-risk avoidance control | policy_guard denies release/PV final/allocate/ship/recall; no write tools for those effects | Security + GxP | E-1904; tests |
| Transparency | Users informed outputs are assistive; evidence citations and abstention reasons shown | Product | Blueprint |
| Automation bias risk | If humans stop reviewing, practical risk profile worsens even if legal labels unchanged | GxP | Artefact 18 |

## 5. Provider/deployer obligations

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Deployer-oriented duties (assumed) | Intended-use documentation; human oversight; logging; risk management; instruction for use; incident process | GxP + Security | E-1903; artefacts 16–21 |
| Provider duties | If NovaCura later places a general-purpose model into service as provider, additional obligations may apply — out of current POC claim | Architecture | A-406 |
| Evidence practice | Keep model/prompt/tool versions, evaluation results and audit trails (ISO-aligned artefact 20) | Evaluation | Change control |

## 6. Evidence and assumptions

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Binding programme evidence | E-1901, E-1902, E-1904 | GxP | This section |
| Assumptions that must remain true | Human Decide retained; no silent write path; emergency stop works; residency/consent gates hold | Multi-role | A-404..A-406 |
| What we do not claim | Certified EU AI Act conformity assessment; notified-body approval; production regulatory clearance | GxP | Explicit non-claim |

## 7. Change triggers

| Trigger | Effect on this analysis | Owner |
|---|---|---|
| Addition of write tool that can set disposition / allocate / finalize PV | Immediate invalidation; treat as potential high-risk expansion; stop claim | Security + GxP |
| Removal of forced human review / contestability | Invalidates meaningful-oversight assumption | Product + GxP |
| Deployment outside EU with different AI laws | Requires parallel jurisdiction analysis | Privacy + Legal (human) |
| Model substitution without change control | Suspend inference; re-run applicability + TEVV | Architecture |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-1901 | Gap | Formal legal opinion absent (synthetic workshop) | Classification residual uncertainty | GxP | Pre-production counsel | Open |
| R-1902 | Risk | Rubber-stamp review recreates high practical risk | Patient/quality harm + compliance exposure | GxP | INJ-071 monitoring | Open |
| R-1903 | Assumption | EU lens is sufficient for defence narrative in this package | Other regulators diverge | Privacy | Market expansion | Accepted |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Advisory not autonomous high-risk decisions | No write tools + policy_guard | `test_prohibited_actions.py` | E-1902, E-1904 | Pass |
| Human Decide retained | RAPID | Artefact 03 review | E-1906 | Design accepted |
| Uncertainty recorded | Assumptions A-013, A-404..A-406; R-1901 | Defence pack | This artefact §6–7 | Recorded |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Product/value lead | Reviewer | Avoid overclaiming conformity | Added explicit non-claim §6 | 2026-08-10 |
| Architecture/integration lead | Reviewer | Tie invalidation to write-tool introduction | Change triggers §7 | 2026-08-10 |
