# Vendor Exit and Retirement

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — AEGIS-PHARMA capstone (individual names/roles pending; see A-001 in `01_BUSINESS_CASE.md`) |
| Version / date | v0.1 draft — 2026-08-07 |
| Reviewers | Pending team review |
| Status | Draft |
| Related requirements / ADRs | INJ-078, INJ-083, INJ-084; artefacts 23–24 |

## Purpose

Inventories critical vendor concentration, contract/portability gaps, substitution and exit rehearsal needs, and retirement/retention rules for AI evidence — so AIVENDOR-X exit or capability retirement does not erase GxP decision evidence. Accountable owner: Procurement / Platform. Completion criteria: concentration risk has an explicit substitution strategy; export gaps are named.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-2701 | `data/vendor_dependencies.csv` | Dependency map | model hosting, vector store, evaluation, observability → **all AIVENDOR-X** | INJ-078 total concentration |
| E-2702 | `data/vendor_contracts.csv` | Contracts | AIVENDOR-X exit_days=**120**, data_export=**prompts only**; CMO-IE fill_finish exit_days=180, export PDF/CSV partial | INJ-083 |
| E-2703 | `data/vendor_exit_assets.csv` | Exit asset status | prompt_export=available; embedding_export=**not_supported**; evaluation_history=**PDF_only**; tool_audit=**partial** | Portability gaps |
| E-2704 | `data/retirement_assets.csv` | Retirement policy data | model cards required; prompt versions required; decision evidence risk_based_GxP; raw sensitive prompts minimise/controlled | INJ-084 |
| E-2705 | `data/model_endpoints.csv` | Endpoints | OnPrem-DE LOCAL-SLM available as partial substitute path | Limited alternative |
| E-2706 | `data/retention_rules.csv` | Retention | AI prompt logs 90d unless hold; ICSR/clinical long retain | Conflict management with privacy |

## 1. Dependency inventory

| Capability | Vendor | Exit criticality |
|---|---|---|
| Model hosting | AIVENDOR-X | Critical |
| Vector store | AIVENDOR-X | Critical if RAG enabled |
| Evaluation | AIVENDOR-X | High |
| Observability | AIVENDOR-X | High |
| Fill/finish (non-AI but brownfield) | CMO-IE | Critical for supply — 180d exit |

## 2. Contract and portability gaps

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| AI export rights | Prompts only (E-2702); embeddings not supported; eval history PDF-only; tool audit partial (E-2703). | Procurement | E-2702, E-2703 |
| Decision | Do not store sole copy of GxP decision evidence in vendor-only stores; keep `submission/evidence`-style hashes/results and cited source IDs in NTG-controlled retention. | Platform / CQO | E-2703, E-2704 |
| Exit clock | 120 days for AIVENDOR-X — rehearsal must fit inside that window. | Procurement | E-2702 |

## 3. Substitution strategy

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Near-term | Deterministic offline mode already removes inference dependency for assessed workflows. | Capstone team | artefacts 21/24 |
| Inference substitute | LOCAL-SLM on OnPrem-DE (E-2705) only if integrity + validated scope pass — not automatic. | Platform | E-2705; ADR-006 |
| Eval/observability | Bring evaluation runners in-house (`scripts/evaluate.py` pattern); dual-export metrics before exit. | Platform | E-2703 |
| Vector | Prefer not to introduce non-portable embeddings until export supported — or maintain rebuildable index from controlled sources. | Platform | E-2703 |

## 4. Exit rehearsal

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Rehearsal items | Export prompts; rebuild eval history from local JSON; cut over gateway to deny AIVENDOR-X; run continuity drill with AI disabled; verify decision evidence still retrievable. | Platform | E-2702–E-2704 |
| Status | Not yet executed as a timed drill. | Capstone team | Gap R-2701 |

## 5. Evidence and data export

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Must export / retain | Model cards, prompt versions, decision evidence (E-2704); local test/eval JSON; schema versions. | CQO | E-2704 |
| Cannot rely on vendor for | Embeddings, full eval history, complete tool audit (E-2703). | Platform | E-2703 |

## 6. Retention/destruction

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Destroy | Raw sensitive prompts under minimise — unless legal hold (E-2706). | DPO | E-2704, E-2706 |
| Retain | Decision evidence risk-based GxP; ICSR/clinical per rules. | CQO / PV | E-2706 |
| Retirement approval | CQO + DPO + Platform sign-off that export/retain/destroy complete before vendor off. | Procurement | E-2704 |

## 7. Retirement approval and residual risk

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Residual risk | PDF-only eval history and partial tool audit may leave investigative blind spots after exit. | CQO / CISO | E-2703 |
| Accept only if | Local mirrors exist for all defence-critical claims. | Capstone team | artefact 21 |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-2701 | Gap | 120-day exit rehearsal not run | High | Platform / Procurement | Before reliance on vendor | Open |
| R-2702 | Risk | Embedding non-export traps future RAG designs | Medium | Platform | Before RAG enablement | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Concentration identified | vendor_dependencies | Review | E-2701 | PASS |
| Exit rehearsal complete | Drill | — | E-2702 | Open |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Pending | Procurement / Platform | — | — | — |
