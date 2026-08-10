# Assurance Case

> Participant working artefact for Project AEGIS-PHARMA. Claims–arguments–evidence structure for later go / conditional-go / pivot / pause / stop defence.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Evaluation / reliability lead (custodian); GxP/quality lead (regulated claims) |
| Version / date | 1.1 / 2026-08-10 |
| Reviewers | Security/privacy lead; Product/value lead; Architecture/integration lead |
| Status | Reviewed |
| Related requirements / ADRs | Artefacts 16–20; WA-05/06/07; D-001..D-015; D-401..D-405 |

## Purpose

State the top assurance claim for Phase 4 secure AI/agent design, support it with arguments and evidence, list defeaters, residual risk and invalidation conditions, and frame a **conditional-go** recommendation into POC build (Phase 5) rather than an unconditional production go.

Accountable owner: Evaluation/reliability lead. Completion criteria: CAE chain complete; prohibited-action and trust tests green; residual risks and invalidation triggers explicit.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-2101 | `data/ai_use_boundaries.csv` | INJ-006 | Allowed vs prohibited actions | Binding |
| E-2102 | `submission/src/policy_guard.py` | Team 3 | Deny-by-default enforcement module | Code |
| E-2103 | `submission/tests/test_prohibited_actions.py` | Team 3 | Batch/PV/supply prohibited actions rejected | Test |
| E-2104 | `submission/tests/test_authorization_freshness.py` | Team 3 | Stale cache denied (INJ-067) | Test |
| E-2105 | `submission/tests/test_tool_trust.py` | Team 3 | Poisoned/unsigned tools and hash mismatch denied | Test |
| E-2106 | `submission/artefacts/16_THREAT_ABUSE_MODEL.md` | Team 3 | Threat→control map | Artefact |
| E-2107 | `submission/artefacts/17_PRIVACY_ETHICS.md` | Team 3 | Consent/re-id/deletion/residency/sensitive | Artefact |
| E-2108 | `submission/artefacts/18_RESPONSIBLE_AI_HUMAN_FACTORS.md` | Team 3 | Bias, language, a11y, contest, e-stop | Artefact |
| E-2109 | `submission/artefacts/19_EU_AI_ACT_APPLICABILITY.md` | Team 3 | Advisory posture; uncertainty logged | Artefact |
| E-2110 | `submission/artefacts/20_ISO42001_GOVERNANCE.md` | Team 3 | Change control citing K-005 | Artefact |
| E-2111 | `knowledge/AI_MODEL_CHANGE_CONTROL.md` | K-005; effective 2026-05-12 | Model/prompt/tool change rules | Synthetic policy |
| E-2112 | `submission/evidence/PREFLIGHT_REPORT.md` | Team 3 | Baseline diagnostics findings | Preflight |
| E-2113 | `submission/tests/test_workflow_contracts.py` | Team 3 | Contract negative samples reject prohibited fields | Test |

## 1. Top claim

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| C0 Top claim | For the Phase 4 design envelope, AEGIS-PHARMA’s agent/tool path is bounded such that prohibited regulated actions are denied by default, stale entitlements and poisoned tools fail closed, and residual risks are explicit enough to justify a **conditional-go** into offline POC implementation | Evaluation + GxP | This assurance case |
| Not claimed | Production readiness; EU AI Act conformity certification; measured BR-01 −14% achievement; complete UI accessibility clearance | Product + GxP | Explicit scope limit |

## 2. Context and assumptions

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Context | Synthetic offline workshop; three advisory workflows; human Decide retained | Product | D-001, D-002 |
| Assumptions in force | A-005 boundaries binding; A-008 diagnostics real; A-013/A-401..A-406 Phase 4 assumptions | Multi-role | Assumptions log |
| Operating property | Inference optional; AI-disabled continuity required | Architecture | WA-07, D-004 |

## 3. Subclaims and arguments

| ID | Subclaim | Argument | Depends on |
|---|---|---|---|
| C1 | Prohibited regulated actions cannot succeed via policy_guard | `check_workflow_payload` denies batch disposition/release/reject/recall, PV finals, supply reserve/allocate/ship/quality-status/recall | E-2101, E-2102, E-2103 |
| C2 | Stale entitlement cache cannot authorize | Revoked IAM or stale cache ⇒ deny | E-2104; INJ-067 |
| C3 | Poisoned/unsigned tools cannot execute | Approved hash + signature required; disposition write/postAction denied | E-2105; INJ-066 |
| C4 | Abuse surface is analysed with mapped controls | Threat model covers injection, exfil, ransomware, supply chain, DoW, excessive agency, replay | E-2106 |
| C5 | Privacy/ethics conflicts are governed, not ignored | Secondary use, genomic re-id, deletion vs GxP, residency, sensitive segments have owners/controls | E-2107 |
| C6 | Human factors reduce automation-bias and role-conflict failures | Forced evidence, contestability, e-stop, language/a11y requirements | E-2108 |
| C7 | Legal applicability is advisory-scoped with uncertainty recorded | No autonomous high-risk decision claim; change triggers defined | E-2109 |
| C8 | Change is AIMS/K-005 aligned | Model/prompt/tool changes need version, regression, approval | E-2110, E-2111 |

## 4. Evidence references

| Subclaim | Primary evidence | Result at Phase 4 exit |
|---|---|---|---|
| C1 | `python -m unittest` prohibited suite | Pass |
| C2 | Authorization freshness suite (incl. fixtures) | Pass |
| C3 | Tool trust suite | Pass |
| C1 support | Workflow contract negative samples | Pass (E-2113) |
| C4–C8 | Artefacts 16–20 reviewed | Reviewed status |
| Baseline defects known | Preflight diagnostics | E-2112 informs design |

## 5. Defeaters and counterevidence

| Defeater | Why it matters | Current handling |
|---|---|---|---|
| D1 Rubber-stamp human review (INJ-071) | Makes advisory system behave like autonomous in practice | Forced evidence + monitoring; residual open |
| D2 Permission synonym bypass on tools | Could admit write tool | Fragment denylist + catalog; maintain on change |
| D3 UI accessibility still failing (INJ-073) | Blocks inclusive operation claim | Requirements accepted; implementation gap Phase 5 |
| D4 Unicode package check failure on host | Environment noise vs package integrity | A-001; not used to claim package-perfect |
| D5 Future write-tool “exception” under BR-01 pressure | Would invalidate C0/C1/C7 | Security/GxP hard veto; change trigger in artefact 19 |

## 6. Residual risk

| ID | Residual risk | Severity | Tolerated for conditional-go? | Owner |
|---|---|---|---|---|
| RR-1 | Automation bias persists despite checklist | High | Yes for POC build; must retest before defence go | GxP |
| RR-2 | Language inequity in PV extraction | Medium | Yes with abstain routing design | Evaluation |
| RR-3 | Accessibility not yet coded | Medium | Yes for Phase 5 entry; no UI go claim | Build |
| RR-4 | Exfil/residency engines not fully coded | Medium | Yes with design controls; implement in POC | Privacy |
| RR-5 | EU AI Act formal opinion absent | Medium | Yes for workshop defence with uncertainty stated | GxP |

## 7. Invalidation and reapproval conditions

| Condition | Effect | Reapproval needed from |
|---|---|---|---|
| Any prohibited action test fails | Immediate stop on defence claims | Evaluation + GxP + Security |
| Write-capable disposition/allocate/PV-final tool approved | Invalidate C0/C1/C7; pause | Security + GxP |
| Inference becomes sole path (AI-disabled broken) | Invalidate continuity claim | Architecture + Evaluation |
| Consent/residency gate bypassed in code | Invalidate C5 | Privacy |
| K-005 superseded without adopting successor | Re-map change control | Domain + Architecture |

## Recommendation framing (for later defence)

| Option | When to choose | Phase 4 position |
|---|---|---|---|
| Go (production) | All residual risks closed; measured benefits; full TEVV/ops | Not justified now |
| Conditional-go (continue POC) | Hard gates green; residuals owned with dates | **Selected** — proceed Phase 5 offline POC under D-001/D-002 |
| Pivot | No-AI path dominates on measured value | Revisit after POC metrics (D-003) |
| Pause | Critical gate red or authority conflict unresolved | If C1–C3 fail |
| Stop | Boundaries cannot be met | If write-tools mandated against E-2101 |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-2101 | Risk | Conditional-go misread as production go | Overclaim in defence | Product | Defence script review | Open |
| R-2102 | Gap | End-to-end workflow POC not yet built | Benefits unproven | Build | Phase 5 | Open |
| R-2103 | Assumption | policy_guard remains on every execution path in POC | Bypass nullifies C1–C3 | Architecture | Code review gate | Accepted |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| C0 conditional-go for Phase 5 | Artefacts 16–20 + policy_guard | Unittest suite under `submission/tests` | E-2102..E-2113 | Conditional-go |
| Hard-gate prohibited actions | `check_workflow_payload` | `test_prohibited_actions.py` | E-2103 | Pass |
| INJ-067 | `check_authorization_records` | `test_authorization_freshness.py` | E-2104 | Pass |
| INJ-066 / INJ-070 | `check_tool_manifest` / `check_model_artifact` | `test_tool_trust.py` | E-2105 | Pass |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Security/privacy lead | Reviewer | Require C2/C3 as equal peers to C1 | Added subclaims | 2026-08-10 |
| Product/value lead | Reviewer | Label recommendation conditional-go not go | §7 table | 2026-08-10 |
| Architecture/integration lead | Reviewer | Invalidation if policy_guard bypassed | R-2103 | 2026-08-10 |
