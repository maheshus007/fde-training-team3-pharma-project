# Business Case

> Participant working artefact for Project AEGIS-PHARMA. Analysis cites challenge evidence under `case/` and `data/`; implementation remains under `submission/`.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Product / value lead |
| Version / date | 1.0 / 2026-08-10 |
| Reviewers | Domain/evidence lead; GxP/quality lead |
| Status | Reviewed |
| Related requirements / ADRs | INJ-001..006; REQ path via later `09_REQUIREMENTS_TRACEABILITY.md`; decisions D-001..D-005 |

## Purpose

Support a go / conditional-go recommendation to invest in a bounded AEGIS-PHARMA intervention that improves evidence reconciliation across batch-review readiness, PV intake and supply shortage planning without changing registered specifications or transferring Quality, Safety or allocation authority to AI (`data/board_requests.csv` BR-01; `data/ai_use_boundaries.csv`; `case/INTEGRATED_CASE.md` §§3–5).

Accountable owner: Product/value lead. Completion criteria: problem, baseline, no-AI alternative, metric tree, scope/exclusions, stop criteria and benefits plan are evidence-cited and independently reviewed.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-001 | `data/board_requests.csv` BR-01 | Board request; due 2026-11-30 | −14% release lead time; no specification or Quality-authority change | Single-row synthetic board metric; constraint is binding |
| E-002 | `case/INTEGRATED_CASE.md` §§2–4 | Case authority for capstone | Three mandatory workflows; fragmented brownfield estate | Narrative case; details in CSV injects |
| E-003 | `data/no_ai_baselines.csv` | Process-excellence estimates (INJ-003) | master_data_repair 38%/10w; rules_workflow 27%/6w; genai_assist 51%/14w | Estimates only; not measured NTG baselines |
| E-004 | `data/kpi_conflicts.csv` | Functional KPI targets (INJ-002) | Manufacturing 98% schedule; Quality 96% RFT; Safety 100% expedited; Clinical DB lock 2026-09-15 | Targets conflict under shared capacity |
| E-005 | `data/ai_use_boundaries.csv` | Executive prohibition (INJ-006) | Allowed reconcile/cite/flag/abstain vs prohibited release/PV final/allocate | Binding hard-gate input |
| E-006 | `data/portfolio_products.csv` NCX-101 | Portfolio record (INJ-004) | Patent exclusivity 19 months; label divergence risk | Synthetic portfolio |
| E-007 | `case/STAKEHOLDER_PACK.md` | Stakeholder mandates | QP/PV human-only final decisions; Quality independence | Deliberate conflicts listed |
| E-008 | `data/stakeholders.csv` ST-01..03 | Priority samples | QP evidence completeness vs Manufacturing supply continuity vs Safety timeliness | Partial stakeholder sample |

## 1. Problem statement and affected decisions

NovaCura’s evidence is split across LIMS, MES, eBR, QMS, safety databases, serialization, vendor portals and spreadsheets with inconsistent identifiers, timestamps and authorities (`case/INTEGRATED_CASE.md` §2). Board target BR-01 demands 14% end-to-end release lead-time reduction without specification change or weakened Quality authority (INJ-001; E-001). Concurrent inject pressure includes disputed biologics genealogy (INJ-021), PV duplicate/clock conflicts (INJ-037..038) and cold-chain/shortage planning (INJ-051, INJ-054, INJ-056).

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| What problem are we solving? | Evidence-reconciliation latency and contradiction opacity across Quality, Safety and Supply, not autonomous decisioning | Product/value (D-001) | This business case §1; charter WA-06 |
| Which decisions are affected? | Batch-review readiness gap lists; PV intake packaging for human assessors; supply option sets for human planners | Domain + Product | Workflow definitions in §5 and blueprint |
| Which decisions stay human? | Batch disposition; final PV judgements; allocate/ship/recall | GxP/quality (D-002) | `data/ai_use_boundaries.csv`; hard-gate tests (later) |
| Why now? | BR-01 due 2026-11-30; NCX-101 patent cliff in 19 months (INJ-004); inspection surge INJ-050 | Product/value | E-001, E-006 |

## 2. Baseline and evidence

Current state is deliberately defective: stale entitlement cache, model hash mismatch, unapproved unit mapping and untrusted knowledge are already visible via `starter/baseline_diagnostics.py` (INJ-067, INJ-070, INJ-024, INJ-065). KPI owners pull in incompatible directions (E-004; E-008).

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| What is the measured pain? | Board metric is release lead time (−14% target). Diagnostic findings prove authorization/unit/trust defects that inflate manual reconciliation | Evaluation + Domain | `submission/evidence/PREFLIGHT_REPORT.md`; E-001 |
| What evidence is authoritative for baseline claims? | Board CSV for target; case for workflow mandate; diagnostics for control defects; no_ai_baselines for alternative estimates | Domain/evidence | Evidence register above |
| How do we avoid false precision? | Treat E-003 percentages as process-excellence claims, not audited NTG actuals; abstain from claiming realized % until measured in POC | Product/value (A-002) | Assumptions log A-002 |

## 3. No-AI alternative

INJ-003 / E-003 present a credible non-generative path: master-data repair (38% estimated value, 10 weeks) and rules/workflow redesign (27%, 6 weeks) versus genai_assist (51%, 14 weeks). Team 3 does not dismiss the no-AI path.

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Can process redesign alone meet BR-01? | Possibly for parts of release lead time if master data and unit mappings are repaired; does not by itself solve multilingual PV clustering, untrusted-document handling or option generation under shortage ethics | Product + Domain (D-003) | Comparison table below |
| What must AI (if used) beat? | Deterministic rules + repaired masters on: contradiction surfacing speed, multilingual intake assist, option enumeration with citations — while matching or exceeding safety of abstention | Evaluation | Later scorecard vs no-AI baseline fixtures |
| Hybrid stance | Use deterministic reconciliation and contracts first; add bounded inference only where no-AI path fails measured tests | Architecture (D-004) | Blueprint §2; continuity INJ-082 |

| Option | Estimated value % | Duration weeks | Role in AEGIS |
|---|---:|---:|---|
| master_data_repair | 38 | 10 | Mandatory foundation (units, IDs, authority) |
| rules_workflow | 27 | 6 | Default execution path / AI-disabled mode |
| genai_assist | 51 | 14 | Optional assist behind budgets and human review |

## 4. Value hypothesis and metric tree

**Hypothesis:** If NTG deploys bounded reconciliation and option-support services that cite provenance, abstain on ambiguity and preserve human authority, then release-packet readiness time and PV intake cycle time improve toward BR-01 and Safety expedited readiness without violating Quality independence or AI-use boundaries.

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| North-star metric | Release lead time −14% with Quality authority unchanged (BR-01) | Product | E-001 |
| Leading indicators | % evidence gaps auto-flagged with citations; % unit/authority abstentions correct; PV duplicate-candidate precision for human review; option-set completeness under INJ-056 constraints | Evaluation | Future evaluation artefacts |
| Guardrail metrics | Zero autonomous prohibited actions; entitlement deny rate on stale cache; AI-disabled task completion; review time not excluded (INJ-077) | GxP + Security + Evaluation | Hard-gate tests |
| Conflicting KPIs | Manufacturing schedule adherence vs Quality RFT vs Safety on-time vs Clinical lock (E-004) — value case must not optimize one by suppressing another’s evidence | Product (D-005) | Stakeholder pack deliberate conflicts |

## 5. Scope and exclusions

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| In scope | Workflow A batch evidence reconciliation; Workflow B PV intake/signal support; Workflow C supply options/cold-chain recovery planning | Product | `case/INTEGRATED_CASE.md` §4 |
| In scope controls | Purpose limitation, least privilege, provenance, abstention, human review, idempotency, budgets, checkpoint/rollback, kill switch, AI-disabled continuity | Architecture | Case §5 |
| Out of scope | Autonomous disposition, final PV decisions, allocate/ship/recall, formulation/spec changes, clinical eligibility determination | GxP/Security | E-005; INJ-006 |
| Explicit exclusions | Changing registered specifications; weakening independent Quality authority (BR-01 constraint); relying on internet services for core path | Product | E-001; package mode |

## 6. Assumptions, stop/pivot criteria

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Key assumptions | Offline package sufficient; E-003 estimates usable for relative comparison; UnicodeDecodeError in verify_package is environmental not a reason to alter challenge tools | Product / Build | A-001..A-003 |
| Stop | Any design that requires autonomous regulated writes to meet BR-01 | GxP | Hard gates |
| Pivot | If deterministic rules+master-data meet BR-01 proxy metrics without inference, demote genai_assist to non-essential | Product + Evaluation | No-AI challenge INJ-003 |
| Pause | Authority/unit/time ambiguity unresolved for a demo claim | Domain | Working agreement WA-03 |

## 7. Benefits-realisation plan

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| 0–30 days | Instrument baselines for reconciliation cycle time on fixture batches; close unit-mapping and entitlement defects in design | Build + Domain | Fixtures/tests under `submission/` |
| 30–60 days | Demonstrate three workflows offline with human review touchpoints; measure review-minute inclusion (INJ-077) | Evaluation | Demo + scorecard |
| 60–90 days | Compare against no-AI baseline; board-ready BR-01 contribution estimate with residual risk | Product | Artefacts 22–29 later |
| Benefits owners | Quality (evidence completeness), PV (intake timeliness assist), Supply (option latency) — none own disposition/allocation via AEGIS | Per stakeholder pack | E-007 |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-001 | Risk | KPI conflict drives unsafe speed optimization (INJ-002) | Quality independence eroded | Product/GxP | Every scope change | Open |
| R-002 | Assumption | genai_assist 51% estimate overstates unique AI value vs master data | Wrong investment mix | Product | After first measured POC | Open |
| R-003 | Gap | Full package `--check` failed UnicodeDecodeError | Incomplete package integrity proof | Build | Documented in preflight; local hashes later | Open |
| R-004 | Risk | Hidden human-review cost (INJ-077) voids ROI | Benefits unrealized | Product | Cost model artefact | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| BR-01 without Quality authority change | Human-only disposition; advisory reconciliation | Prohibited-action tests | `data/board_requests.csv`; `data/ai_use_boundaries.csv` | Design accepted |
| No-AI path considered | Deterministic mode first | Baseline comparison plan | `data/no_ai_baselines.csv` | Design accepted |
| Three workflows only for POC | Blueprint scope | Workflow fixtures | `case/INTEGRATED_CASE.md` §4 | Design accepted |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Domain/evidence lead | Reviewer | Required explicit INJ-001..006 linkage | Added throughout | 2026-08-10 |
| GxP/quality lead | Reviewer | Confirm BR-01 constraint preserved | Confirmed in §5 | 2026-08-10 |
