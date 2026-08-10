# ISO/IEC 42001-Aligned Governance

> Participant working artefact for Project AEGIS-PHARMA. Aligns AIMS-style controls to workshop evidence; cites `knowledge/AI_MODEL_CHANGE_CONTROL.md` as synthetic NovaCura policy input (applicability must still be verified at use).

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Architecture / integration lead (AIMS controls); GxP/quality lead (validation intersection) |
| Version / date | 1.1 / 2026-08-10 |
| Reviewers | Security/privacy lead; Evaluation/reliability lead |
| Status | Reviewed |
| Related requirements / ADRs | `knowledge/AI_MODEL_CHANGE_CONTROL.md` (K-005); artefacts 16–19, 21; D-004, D-014 |

## Purpose

Define AI management system (AIMS)–aligned controls for model, prompt, retrieval, tool and evaluator change so AEGIS can evolve without silent risk creep or unapproved inference.

Accountable owner: Architecture/integration lead. Completion criteria: policy objectives, inventory, risk assessment, lifecycle controls, supplier/data governance, monitoring and evidence mapping are populated and linked to change-control authority K-005.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-2001 | `knowledge/AI_MODEL_CHANGE_CONTROL.md` | Synthetic NovaCura Global Policy; effective 2026-05-12; status approved; Doc ID K-005 | Version model/prompt/retrieval/schema/tool/evaluator; classify by risk; regression + approval before release | Training document; consumer must verify applicability |
| E-2002 | `data/model_registry.csv`; `data/model_artifacts.csv` | INJ-070 | Hash mismatch demonstrates need for registry pin | Synthetic |
| E-2003 | `data/tool_catalog.csv`; poisoned/approved manifests | INJ-066 | Tool changes are controlled configuration | Synthetic |
| E-2004 | `sources/LOCAL_REGULATORY_AND_STANDARDS_GUIDE.md` | Package guide | Intended use, supplier management, change control themes | Guide |
| E-2005 | `submission/src/policy_guard.py` | Team control | Runtime enforcement of prohibited actions / tool trust / auth freshness / model hash | Code |
| E-2006 | `submission/artefacts/ASSUMPTIONS_AND_DECISION_LOG.md` | Team log | Change decisions and invalidation triggers | Living |

## 1. AI policy and objectives

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Policy objective | Assist evidence reconciliation without transferring regulated Decide authority to AI | Product + GxP | D-001, D-002 |
| Operating mode | Deterministic/offline first; inference optional, budgeted, kill-switchable | Architecture (D-004) | WA-08 |
| Binding change rule | Per K-005: version artifacts; classify risk; require regression evidence and approval before controlled release | Architecture | E-2001 |
| Non-use | Do not treat K-005 as authority outside status/jurisdiction/scope/effective period (document’s own prohibition) | Domain | E-2001 § Prohibited use |

## 2. Use-case inventory and ownership

| Use case | Owner | Risk tier (programme) | AI role |
|---|---|---|---|
| Workflow A — batch evidence reconciliation | Domain + GxP | High operational impact; advisory only | Reconcile/cite/flag/abstain |
| Workflow B — PV intake / signal support | Safety + Domain | High privacy/safety impact; advisory only | Extract/normalize/cluster/cite |
| Workflow C — supply options / cold-chain recovery | Supply + Quality | High continuity impact; options only | Generate options |
| Shared — tool/model gateway | Security + Architecture | Control plane | Deny-by-default |

## 3. Risk and impact assessment

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Method | Inject-driven threat/privacy/human-factor assessment (artefacts 16–18) plus quality risk intersection | Security + GxP | Artefacts 16–18 |
| Top risks | Poisoned tools; stale auth; injection; hash-mismatched models; automation bias; secondary use | Security | Artefact 16–17 |
| Residual acceptance | Recorded in artefact 21; not silently closed | Evaluation | Assurance case |

## 4. Lifecycle controls

Aligned to K-005 mandatory controls (E-2001):

| Change class | Examples | Required evidence before release | Approvers |
|---|---|---|---|
| Model | New weights, vendor model swap | Registry hash pin (`check_model_artifact`); eval regression; subgroup language check; AI-disabled path still green | Architecture + Evaluation + GxP |
| Prompt | System/tool prompts | Prompt version ID; golden fixture diff; prohibited-action suite | Architecture + Security |
| Retrieval corpus | Knowledge additions | Authority/effective-date tags; untrusted flag; supersession check | Domain + Security |
| Schema / contract | Response JSON | Contract tests; negative prohibited samples | Architecture + Evaluation |
| Tool | New manifest | Signature + approved hash; catalog approval; `test_tool_trust.py`; no disposition write | Security + Architecture |
| Evaluator / grader | Threshold changes | Documented rationale; no silent weakening of hard gates | Evaluation + GxP |

Runtime: `policy_guard` remains on the execution path for workflow payloads, authz freshness, tool trust and model hash (E-2005).

## 5. Supplier and data governance

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Model suppliers | Substitutable; hash and eval gates; exit path required before production claim | Architecture | FinOps/exit later |
| Data suppliers | Documents/tools treated as untrusted until verified (D-008) | Security | INJ-065/066 |
| Personal data | Consent purpose, residency, retention holds (artefact 17) | Privacy | INJ-060/061/064 |
| K-005 evidence expected | Source identity, version, effective date, owner, retrieval time; transformations; conflicts; reviewer actions; audit events | Domain | E-2001 |

## 6. Monitoring, incidents and improvement

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Monitor | Prohibited-action attempts; stale-auth denials; tool rejects; hash mismatches; token spend (INJ-076); contest/e-stop | Security + Evaluation | Artefact 16 §7 |
| Incident | Fail closed; disable inference; preserve audit; human continuity | Ops + Security | WA-07 |
| Improvement | Failed gates create fixtures; change class re-entry via §4 table | Evaluation | TEVV later |

## 7. Evidence mapping

| AIMS-oriented control | Submission evidence | Challenge authority cited |
|---|---|---|
| AI policy / objectives | Charter; WA-05/06; this artefact §1 | E-2001; E-2004 |
| Risk assessment | Artefacts 16–18 | Inject catalogue |
| Lifecycle / change | §4 table citing K-005 | K-005 E-2001 |
| Runtime enforcement | `policy_guard.py` + tests | INJ-006/066/067/070 |
| Model integrity | Registry pin vs INJ-070 | E-2002 |
| Tool integrity | Catalog + manifests | E-2003 |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-2001 | Assumption | K-005 remains applicable synthetic policy for workshop change control | Wrong authority if superseded | Domain | Catalog supersession | Accepted |
| R-2002 | Gap | Full CMS/ticket workflow for changes not implemented in POC | Manual discipline risk | Architecture | Phase 7 ops | Open |
| R-2003 | Risk | Prompt tweak skips regression under schedule pressure | Silent quality drop | Evaluation | Hard gate in CI | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Versioned change before controlled release | §4 lifecycle table citing K-005 | Change checklist + regression suite | E-2001 | Design accepted |
| Tool change cannot admit disposition write | policy_guard + catalog | `test_tool_trust.py` | E-2003, E-2005 | Pass |
| Model hash mismatch blocks load | Registry pin | `check_model_artifact` tests | E-2002 | Pass |
| Prohibited actions remain denied across changes | Hard-gate suite in release criteria | `test_prohibited_actions.py` | E-2005 | Pass |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Security/privacy lead | Reviewer | Tool class must require signature and hash | Added to §4 | 2026-08-10 |
| Evaluation/reliability lead | Reviewer | Hard gates must not be weakenable by evaluator change alone | GxP co-approval on grader changes | 2026-08-10 |
