# Stakeholder and Decision Rights

> Participant working artefact mapping NovaCura stakeholders to AEGIS-PHARMA decision rights, conflicts and segregation of duties.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Product / value lead with GxP/quality lead |
| Version / date | 1.0 / 2026-08-10 |
| Reviewers | Security/privacy lead; Domain/evidence lead |
| Status | Reviewed |
| Related requirements / ADRs | `case/STAKEHOLDER_PACK.md`; `data/stakeholders.csv`; INJ-002, INJ-006, INJ-074; Team Charter |

## Purpose

Establish who may demand, design, approve, veto or escalate AEGIS capabilities so that local legal accountability for Quality, Safety, Clinical and Regulatory decisions remains human (`case/INTEGRATED_CASE.md` §8; INJ-074).

Accountable owner: Product/value lead. Completion criteria: stakeholder map, RACI/RAPID, incentive conflicts, independent review, escalation and training needs are evidence-cited.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-201 | `case/STAKEHOLDER_PACK.md` | Stakeholder evidence pack | Mandates, incentives, concerns, decision authority | Qualitative pack |
| E-202 | `data/stakeholders.csv` ST-01..03 | Sample priorities | QP evidence completeness; Manufacturing supply continuity; Safety reporting timeliness | Partial list |
| E-203 | `data/kpi_conflicts.csv` | Functional KPIs (INJ-002) | Conflicting targets | No weighting |
| E-204 | `data/ai_use_boundaries.csv` | Executive boundary (INJ-006) | Prohibited autonomous actions | Binding |
| E-205 | `data/board_requests.csv` BR-01 | Board | Lead-time target with Quality constraint | Synthetic |
| E-206 | `data/decision_rights.csv` (referenced by INJ-074) | Case inject pointer | Role conflict global vs local accountability | Use with stakeholder pack |

## 1. Stakeholder map

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Primary users | EU QP / batch reviewers; PV case handlers; supply planners under quality constraints | Product | E-201 |
| Primary authorities | Chief Quality Officer (quality-system policy); EU QP (certification human-only); Global Head of PV (final safety human-only); CISO (security); DPO (privacy) | GxP + Security | E-201 |
| Economic sponsors | Board (BR-01); Manufacturing VP; Supply Chain VP | Product | E-205, E-202 |
| Challengers / constraints | Patient Safety Representative (advisory veto via safety governance); Works Council (consultation); Biostatistics (prespecified transforms); Site Investigator Council (local facts) | Product | E-201 |
| Capstone team mapping | Team roles proxy sponsor concerns during build; they do not replace NTG accountable roles in operating model | Charter | `00_TEAM_CHARTER.md` |

| Stakeholder | AEGIS interest | Must never lose |
|---|---|---|
| EU Qualified Person (ST-01) | Complete cited release evidence | Human certification |
| Manufacturing VP (ST-02) | Faster readiness, fewer opaque holds | Cannot gain release authority via AI |
| Global Safety Head (ST-03) | Faster intake/clustering assist | Final PV decisions |
| Chief Quality Officer | Inspection-ready provenance | Independent Quality authority (BR-01) |
| Supply Chain VP | Traceable options under shortage | Allocate/ship without approvals |
| CISO / DPO | Deny poisoned tools; lawful processing | Security/privacy veto |

## 2. RACI/RAPID decision matrix

RAPID used for regulated decisions; RACI for delivery work.

| Decision | Recommend | Agree | Perform | Input | Decide |
|---|---|---|---|---|---|
| Scope AEGIS to Workflows A–C | Product | GxP, Security | Build | Domain, Evaluation | Product (D-001) |
| Treat source as authoritative for a context | Domain | GxP (if GxP-relevant) | Build | Architecture | Domain; GxP veto if release/safety |
| Enable model inference for a step | Architecture | Evaluation, Security | Build | Product | Evaluation release gate |
| Accept residual quality risk in demo | GxP | Product | Evaluation | Domain | GxP |
| Override abstention to force automation | Not allowed for prohibited actions | — | — | — | Denied by E-204 |
| Privacy secondary use of trial data | DPO (NTG) / Security lead (team) | GxP | Build | Product | DPO/Security — default deny |

| Delivery activity | R | A | C | I |
|---|---|---|---|---|
| Artefacts 01–04 | Product | Product | Domain, GxP | All |
| Prohibited-action tests | Evaluation | Security | GxP, Build | Product |
| AI-disabled runbooks | Build | Evaluation | Domain | All |

## 3. Incentive conflicts

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Speed vs completeness | Manufacturing schedule adherence 98% vs Quality right-first-time 96% (E-203); stakeholder pack: Quality and Manufacturing disagree on binding constraint | Product documents; GxP decides evidence completeness bar | E-201, E-203 |
| Global standardization vs local accountability | INJ-074 / E-201: global process owner vs local QP/safety officers | Architecture supports jurisdiction variation; GxP/PV retain local decide | Charter segregation |
| Privacy minimization vs GxP preservation | Stakeholder pack deliberate conflict; INJ-035/061 | Security + GxP co-resolve; no silent delete | Later privacy artefact |
| Procurement concentration vs substitutability | Bundled vendor vs CISO/architecture exit needs (INJ-078, INJ-083) | Security + Architecture | Vendor exit artefact later |
| Clinical automation vs biostatistics | Prespecified explainable transforms required | Domain keeps clinical eligibility out of AEGIS scope | E-204 |

AEGIS success metrics include guardrails so BR-01 progress cannot be claimed by suppressing Quality or Safety evidence.

## 4. Independent review and segregation of duties

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Author ≠ approver | Artefact authors cannot sole-approve hard-gate claims | Evaluation / GxP | Charter §4 |
| Build ≠ security accept | Write-capable tools require Security agree | Security | INJ-066 |
| Manufacturing ≠ release | Manufacturing VP never independent batch release (E-201) | GxP / QP | E-201 |
| PV assist ≠ PV decide | Intake tools stop at cluster/cite | Global Safety Head | E-204 |
| Team SoD | Same person may hold multiple workshop roles only if review of their own hard-gate content is delegated | Charter | `00_TEAM_CHARTER.md` |

## 5. Escalation and override

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Escalation path | Builder → role lead → Product documents trade-off → GxP/Security veto window → pause/stop recorded in decision log | Product custodian | WA-11 |
| Override of abstention | Allowed only for human accountable roles outside the system using their existing NTG authorities — never by the model or agent | GxP | E-204 |
| Emergency change | Vendor hotfixes without retrospective approval are challenge defects (INJ-034); AEGIS must flag missing approval, not bypass | Domain | Inject catalogue |
| Board pressure | BR-01 cannot override Quality-authority constraint (E-205) | GxP | Hard gate |

## 6. Training and adoption

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Required competencies | Evidence citation, abstention meaning, entitlement hygiene, multilingual PV caution (INJ-072), accessibility (INJ-073), automation-bias awareness (INJ-071) | Product + Evaluation | Blueprint §6 |
| Adoption risk | Reviewers accepting AI summaries that omit critical deviations (INJ-071) | GxP | Forced evidence checklist |
| Site burden | Site Investigator Council concern that central automation ignores local facts (E-201) | Domain | Local confirmation steps in Workflow B/C where applicable |
| Works Council | Performance surveillance via AI telemetry needs consultation in applicable regions | Security/Product | Privacy/ethics artefact later |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-201 | Risk | Global process owner pushes uniform automation past local QP | Legal accountability break | GxP | INJ-074 reviews | Open |
| R-202 | Gap | Full `decision_rights.csv` detail not yet exhaustively tabulated in this artefact | Residual role ambiguity | Domain | Phase 2 evidence model | Open |
| R-203 | Assumption | Team role proxies are sufficient for capstone defence of SoD | Examiner challenges oral vs written | Product | Keep written RAPID current | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Human-only QP/PV finals | No disposition/final-PV tools | Prohibited-action tests | E-201, E-204 | Design accepted |
| KPI conflicts acknowledged | Guardrail metrics | Scorecard design | E-203 | Design accepted |
| Independent review | Charter SoD | Review records on artefacts | Charter §4 | Met for Phase 1 |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Security/privacy lead | Reviewer | Add privacy secondary-use default deny | Added in RAPID | 2026-08-10 |
| Domain/evidence lead | Reviewer | Bind ST-01..03 sample to pack | Added map table | 2026-08-10 |
