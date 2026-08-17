# Privacy and Ethics

> Participant working artefact for Project AEGIS-PHARMA. Cites challenge injects; does not invent regulatory approvals.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Security / privacy lead |
| Version / date | 1.2 / 2026-08-16 |
| Reviewers | GxP/quality lead; Domain/evidence lead; Product/value lead |
| Status | Reviewed |
| Related requirements / ADRs | INJ-041, INJ-059, INJ-060, INJ-061, INJ-062, INJ-064; D-401; A-401..A-403 |

## Purpose

Establish privacy-by-design and ethics constraints for AEGIS so that advisory workflows can process safety, batch and supply evidence without unlawful secondary use, uncontrolled re-identification, residency breach, or automated erasure of GxP-held records.

Accountable owner: Security/privacy lead. Completion criteria: consent/secondary use, genomic re-id, deletion vs GxP, residency and sensitive segments each have control, owner and acceptance evidence.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-1701 | `case/INTEGRATED_CASE.md` INJ-041, INJ-059..062, INJ-064 | Case inject catalogue | Privacy conflict narratives | Narrative |
| E-1702 | `data/consents.csv`; `data/data_exports.csv` | INJ-060 | EU trial data proposed for global model training outside original consent purpose | Synthetic |
| E-1703 | `data/genomic_data.csv`; `data/privacy_risk.csv` | INJ-059 | Nominally pseudonymised rare-disease data with high re-id risk | Synthetic |
| E-1704 | `data/deletion_requests.csv`; `data/retention_rules.csv` | INJ-061 | Data-subject deletion vs trial/GxP retention | Synthetic conflict |
| E-1705 | `data/data_residency.csv`; `data/backup_inventory.csv` | INJ-064 | Backup replica in unapproved region | Synthetic |
| E-1706 | `data/icsr_cases.csv`; `data/sensitive_segments.csv` | INJ-041 | Pregnancy and paediatric content in general queue | Synthetic |
| E-1707 | `submission/artefacts/00_TEAM_CHARTER.md` | Team binding | Deletion never automated against GxP holds | Participant rule |
| E-1708 | `data/ai_use_boundaries.csv` | INJ-006 | AI must not finalize PV judgements that depend on sensitive narrative interpretation alone | Binding |
| E-1709 | `data/patient_support_cases.csv` | INJ-062 | PSP-17 free text exceeds copay-support purpose (diagnosis, job loss, family, bank hardship) | Synthetic; minimise, do not route to general context |

## 1. Purpose and data map

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Primary purposes | Batch evidence reconciliation; PV intake packaging; supply option generation — advisory only | Product (D-001) | Business case §5 |
| Data classes | Batch/quality records; ICSR narratives; consent metadata; genomic research subsets; residency tags; backup inventory | Domain | E-1701..E-1706 |
| Out of purpose | Global model training on EU trial data without matching consent (INJ-060); affiliate-wide identifiable dump (INJ-068) | Privacy | Deny export/train tools in agent path |
| Decision | Purpose code required on every retrieval and inference request; mismatch → deny | Privacy | A-401 |

## 2. Permission/consent assumptions

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Fact (INJ-060) | Challenge proposes secondary use not explicit in original consent | Case | E-1702 |
| Assumption | Workshop POC does not perform live model training on EU trial personal data; training proposals remain blocked design paths | Privacy | A-402 |
| Control | Secondary-use flag check against consent purpose; abstain/escalate to Privacy + Legal (human) | Privacy | Decision log |
| Acceptance | No AEGIS tool may initiate `data_exports` for model training under mismatched purpose | Security | Policy / contract denial |

## 3. Minimisation and pseudonymisation

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Default | Display/process minimum fields needed for the workflow step; full narrative only for authorized PV roles | Privacy + Domain | Blueprint sensitive data |
| Patient support (INJ-062) | Copay-support free text is not a general PV/batch/supply context; `privacy_gates.check_patient_support_minimise` denies reuse | Privacy | E-1709; TEST-INJ-062 |
| Genomic (INJ-059) | Treat rare-disease combinations as high re-id risk despite nominal pseudonymisation | Privacy | E-1703 |
| Control | No genomic raw fields in general agent context; aggregate or access-gated views; re-id risk score gates export | Privacy | Privacy risk CSV driven |
| Residual | Expert attackers may still re-identify from quasi-identifiers | Privacy | Residual accepted with no bulk export |

## 4. Secondary use and re-identification

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Secondary use | Blocked when consent purpose ≠ requested purpose (INJ-060) | Privacy | E-1702 |
| Re-identification | Genomic + rare disease quasi-identifiers require elevated approval; AEGIS abstains from join patterns that recreate identity | Privacy | E-1703 |
| Ethics stance | Benefit of model accuracy does not override consent boundaries in this programme | Product + Privacy | Charter |

## 5. Residency and cross-border controls

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Fact (INJ-064) | Backup replica places regulated personal data in unapproved region | Case | E-1705 |
| Control | Residency tag check before replicate/export; deny restore/inference from unapproved region copies; alert Privacy | Architecture + Privacy | Backup inventory gate |
| Assumption | POC offline fixtures simulate residency labels; no real cross-border transfer in workshop | Architecture | A-403 |
| Acceptance | Any detected unapproved-region replica is a blocker for go-live claims | Privacy | Defence gate |

## 6. Rights, retention and legal hold

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Conflict (INJ-061) | Participant deletion request vs GxP/trial retention obligation | Case | E-1704 |
| Decision | AEGIS never auto-deletes GxP-relevant records; route to human Privacy + Quality/Legal hold assessment | Privacy + GxP | E-1707; D-401 |
| Control | Deletion request creates workflow ticket; system may suppress processing/display where lawful, not destroy held records | Privacy | Retention rules |
| Acceptance | Automated erase of held trial/PV records is a hard fail | Evaluation | Negative deletion test in later suite |

## 7. Ethical trade-offs and oversight

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Sensitive segments (INJ-041) | Pregnancy/paediatric content requires elevated role; general case queue must not expose by default. `sensitive_segments.csv` keys PV-1020, which is absent from `icsr_cases.csv` — cite the join gap; do not invent ICSR PV-1020 (A-502) | Privacy + PV | E-1706 |
| Patient-support leakage (INJ-062) | Purpose limitation: deny general-context use of PSP-17 free text | Privacy | E-1709 |
| Trade-off | Safety timeliness vs minimization — expedited paths get role-gated full narrative, not open agent dump | Safety + Privacy | Stakeholder RAPID |
| Oversight | Privacy lead veto on secondary use and residency; GxP consulted on retention | Charter | Artefact 03 |
| AI ethics | No final PV seriousness/causality/reportability by model on sensitive narratives | GxP | E-1708; prohibited tests |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-1701 | Risk | Role mis-assignment exposes INJ-041 segments | Privacy harm | Security | Entitlement review | Open |
| R-1702 | Gap | Full consent-purpose engine not yet coded beyond policy design | Secondary-use bypass in future code | Privacy | Phase 5 | Open |
| R-1703 | Assumption | Synthetic consent rows are sufficient to demonstrate deny logic | Real consent schemas differ | Privacy | Production mapping | Accepted |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| No secondary use without consent match (INJ-060) | Purpose binding; no train-export tools | Design + later contract tests | E-1702 | Design accepted |
| Genomic re-id caution (INJ-059) | Access gate; no raw genomic in general context | Privacy review | E-1703 | Design accepted |
| Deletion vs GxP (INJ-061) | Human ticket; no auto-erase | Negative deletion test (later) | E-1704, E-1707 | Decision D-401 |
| Residency (INJ-064) | Region deny on replica use | Residency fixture tests (later) | E-1705 | Design accepted |
| Sensitive segments (INJ-041) | Elevated role gate; join-gap recorded | TEST-INJ-041 | E-1706 | Accepted |
| Patient-support minimise (INJ-062) | Purpose deny in privacy_gates | TEST-INJ-062 | E-1709 | Accepted |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| GxP/quality lead | Reviewer | Stress no auto-delete under hold | D-401 recorded | 2026-08-10 |
| Domain/evidence lead | Reviewer | Align sensitive segment fields with ICSR fixtures | Cited E-1706 | 2026-08-10 |
| Product/value lead | Reviewer | Confirm secondary-use block does not break BR-01 advisory path | Training export out of scope | 2026-08-10 |
