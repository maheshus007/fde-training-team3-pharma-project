# Data Governance and Integrity

> Participant working artefact for Project AEGIS-PHARMA. ALCOA+, lineage, authority, retention and identity/time/unit integrity cite challenge evidence. Implementation remains under `submission/`.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Domain / evidence lead with GxP/quality lead |
| Version / date | 1.1 / 2026-08-10 |
| Reviewers | Security/privacy lead; Architecture/integration lead |
| Status | Reviewed |
| Related requirements / ADRs | INJ-018, INJ-024, INJ-029..036, INJ-035; `knowledge/GXP_DATA_INTEGRITY_STANDARD.md`; D-008, D-010, D-204 |

## Purpose

Establish how AEGIS inventories datasets, assigns source authority by object/context/time, preserves ALCOA+ attributes, controls lineage/transformations, and handles retention/legal-hold/privacy conflicts without fabricating, overwriting or silently normalizing regulated evidence.

Accountable owner: Domain/evidence lead. Completion criteria: ALCOA+ assessment for Workflow A–C critical objects; explicit resolution policy for INJ-035; identity/time/unit controls tied to inject evidence.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-601 | `knowledge/GXP_DATA_INTEGRITY_STANDARD.md` (K-014; 2026-02-15) | NovaCura Global Policy (synthetic) | ALCOA+ mandatory controls | Training extract |
| E-602 | `data/inject_evidence_map.csv` INJ-029..036 | Inject map | Quality/data-integrity inject evidence files | Catalogue |
| E-603 | `data/audit_trails.csv`; `data/privileged_sessions.csv` | System audit | Audit capture disabled during master-data repair | INJ-029 |
| E-604 | `data/access_logs.csv`; `data/staff_rosters.csv` | Access | Shared laboratory account on night shift | INJ-030 |
| E-605 | `data/system_inventory.csv`; `data/validation_inventory.csv` | Inventories | Validated vs conditionally released vs research-only conflict | INJ-031 |
| E-606 | `data/spreadsheet_inventory.csv` | Inventory | Unapproved macro spreadsheet for dissolution | INJ-032 |
| E-607 | `data/deviations.csv`; `data/capa_records.csv` | QMS | CAPA closed; deviation reappears under different taxonomy | INJ-033 |
| E-608 | `data/change_controls.csv`; `data/vendor_releases.csv` | Change control | Emergency hotfix without retrospective approval | INJ-034 |
| E-609 | `data/retention_rules.csv`; `data/legal_holds.csv`; `data/deletion_requests.csv` | Retention / Legal / Privacy | Retain clinical/ICSR vs delete AI logs vs DSR-17 open vs LH-44 active on NCB204-301 and NCB204-B24071 | INJ-035 |
| E-610 | `data/certificates_analysis.csv`; `data/document_lineage.csv` | CoA lineage | Transcribed PDF; original signed source not locatable | INJ-036 |
| E-611 | `data/lab_results.csv`; `data/interface_mappings.csv` | LIMS / interface | LR-88 mg/L vs spec µg/mL; mapping `approved=no` | INJ-024 |
| E-612 | `data/wearable_readings.csv`; `data/timezone_rules.csv` | Clinical devices | local_unknown vs UTC; DST transition DE-008 2026-03-29 | INJ-018 |
| E-613 | `data/document_catalog.csv`; `source_documents/*` | Document authorities | Approved CCDS; referenced_missing eCTD file; EMA letter due-date ambiguity | Mixed integrity |
| E-614 | `data/DATASET_PROFILE.csv` | Package profile | Row/column hashes for fixtures | Integrity baseline for offline mode |

## 1. Dataset inventory and classification

| Class | Examples | GxP / privacy relevance | AEGIS use |
|---|---|---|---|
| GxP critical manufacturing/lab | `batches.csv`, `material_genealogy.csv`, `lab_results.csv`, `ebr_steps.csv`, `release_packets.csv` | High | Workflow A cite-only |
| Quality system | `deviations.csv`, `capa_records.csv`, `change_controls.csv`, `validation_inventory.csv` | High | Gap/effectiveness flags |
| Safety / PV | `icsr_cases.csv`, `adverse_events.csv`, `safety_receipts.csv`, `sensitive_segments.csv` | High + sensitive | Workflow B; purpose-bound |
| Regulatory / IDMP | `medicinal_products.csv`, `idmp_mappings.csv`, `market_authorisations.csv`, `ectd_sequences.csv` | High | Identity and MA constraints |
| Supply / cold-chain | `shipments.csv`, `temperature_loggers.csv`, `inventory.csv`, `allocation_constraints.csv` | Medium–high | Workflow C options |
| Identity / access | `users_entitlements.csv`, `access_cache.csv`, `organisations.csv` | Security | Execution-time authz |
| AI platform / advisory | `model_registry.csv`, `candidate_outputs.csv`, `agent_runs.csv` | Conditional | Inference optional; not SoR |
| Untrusted / defective | `knowledge/MALICIOUS_SUPPLIER_DEVIATION.md`, `tool_manifest_poisoned.json`, transcribed CoA | Contaminated | Display as data; never execute |

Classification decision: AEGIS treats all retrieved content as untrusted until status, authority, signature/hash and applicability are verified (D-008).

## 2. Source authority by object/context/time

| Business object | Authoritative source (context) | Not automatically authoritative | Effective-time rule |
|---|---|---|---|
| Batch genealogy edge | MES/eBR for process consumption; warehouse for issue/receipt — both retained when they conflict | Later warehouse timestamp alone | Cite both MES `missing_branch` and WM-90 for SUA-88 |
| Lab concentration | Signed LIMS result as received (unit verbatim) | Interface default conversion | Conversion only with approved mapping + provenance |
| System validation state | Controlled validation inventory after reconciliation | Any single inventory label | Flag INJ-031 triple conflict; abstain on “validated enough” claims |
| Product strength/form | Jurisdictional MA / RIM for regulatory questions; ERP for logistics description — both cited | Alias collapse | INJ-045 |
| ICSR awareness clock | Each receipt channel kept; PV defines clock per procedure | Earliest/latest auto-pick without policy | INJ-038 |
| Listedness | Source-specific (IB / CCDS / local label) at stated version/date | Global “expected” flag | INJ-040; `source_documents/CCDS_NCB204_v4.md` effective 2026-03-18 |
| Legal hold vs deletion | Legal hold LH-44 and GxP retain rules override privacy delete until co-resolved | Privacy-only delete automation | INJ-035; D-204 |
| Policy SOP | `document_catalog` / knowledge_catalog status=approved and applicable | Superseded / untrusted / old policy | Compare `BATCH_RELEASE_EVIDENCE_POLICY.md` vs `BATCH_RELEASE_POLICY_OLD.md` |

Fact: `SOURCE_SYSTEM_FACT_PACK.md` states no system is universally authoritative.

## 3. Identity and master-data conflicts

| Conflict | Evidence | Governance response |
|---|---|---|
| Acquisition BIOX vs NTG identifiers | `organisations.csv`; `system_inventory.csv` BIOX-ELN; INJ-005 | Namespace by org; no cross-tenant join without stewardship map |
| Compound local code collision | `compounds.csv`; `substance_master.csv`; INJ-008 | Keep structure_hash/salt_form; abstain on merge |
| Product IDMP ambiguity | `medicinal_products.csv` RIM vs ERP; `idmp_mappings.csv` ambiguous_strength_presentation; INJ-045 | Dual citation; steward decision outside AEGIS auto-path (D-201) |
| Alias fan-out | `product_master_aliases.csv` | Aliases are retrieval aids, not identity resolution |
| Shared lab account | INJ-030 | Attributability break: mark results non-attributable until investigation |

## 4. Quality and ALCOA+ assessment

Per E-601 (Attributable, Legible, Contemporaneous, Original, Accurate, Complete, Consistent, Enduring, Available):

| ALCOA+ element | Workflow A finding | Workflow B finding | Workflow C finding |
|---|---|---|---|
| Attributable | Shared instrument account (INJ-030); audit gap (INJ-029) | Affiliate vs vendor receipt actors differ (INJ-038) | Logger/pallet association disputed (INJ-051) |
| Legible | Spreadsheet without verified history (INJ-032) | Multilingual narratives; MedDRA version labels required (INJ-039, INJ-072) | Trade doc vs licence text mismatch (INJ-057) |
| Contemporaneous | eBR back-entry after downtime (INJ-025) | Awareness dates disagree across channels (INJ-038) | Logger timestamps mixed local_unknown/UTC |
| Original | Transcribed CoA; signed source missing (INJ-036) | Social post without identifiable reporter (INJ-042) | Aggregation missing after line restart (INJ-052) |
| Accurate | Unapproved unit map 1:1 mg/L→µg/mL (INJ-024); OOS/OOT/invalid triad (INJ-023) | PT shift across MedDRA 27.1 vs 28.0 (INJ-039) | Temp readings tied to conflicting pallets P-88/P-89 |
| Complete | QP packet missing CMO audit commitment (INJ-028); genealogy branch missing | Duplicate cluster incomplete without human merge | Recall genealogy incomplete (INJ-058) |
| Consistent | CAPA taxonomy drift (INJ-033); validation labels disagree (INJ-031) | Listedness IB/CCDS vs IN local label (INJ-040) | Demand vs inventory vs ethics constraints (INJ-056) |
| Enduring | Retention conflict may delete AI logs while GxP needs hold (INJ-035) | ICSR retain rule vs DSR | Retirement evidence preservation (INJ-084) |
| Available | referenced_missing eCTD document (DOC-ECTD-1) | Restricted case stub exception in RELATIONSHIP_MODEL | OT isolation degraded MES/QMS (INJ-069) |

Decision: AEGIS readiness/output grades records with ALCOA+ defect tags; never “repairs” by overwriting originals.

## 5. Lineage and transformation controls

| Control | Requirement | Evidence link |
|---|---|---|
| Preserve originals | Store verbatim source values alongside any derived view | E-601; INJ-036 |
| Document transformations | Every unit convert, code map, clock normalize records rule id, approver, effective time | INJ-024; `interface_mappings.csv` |
| Deny silent normalize | Unapproved mapping → abstain | D-010 |
| Lineage register | `document_lineage.csv` pattern: derived_from, transcribed_by, verified_by | E-610 |
| Contract versions | LIMS v1 vs v2 field rename tracked in `api_contract_versions.csv` and `source_documents/LIMS_result_contract_*.md` | E-512 path via artefact 05 |
| Audit continuity | If audit_trails show disabled window, mark master-data changes in that window as integrity-suspect | INJ-029 |
| Candidate AI outputs | `candidate_outputs.csv` must retain omitted_fact visibility (INJ-071) | Human factors |

## 6. Retention, residency and legal hold

| Obligation | Record example | Directed action | Conflict |
|---|---|---|---|
| GxP / clinical retain | `clinical_trial_source` — 25 years EU minimum scenario | retain | vs DSR-17 delete-all biomarker/AI data |
| PV retain | `ICSR` — PV lifecycle retention | retain | vs privacy minimisation |
| Privacy minimise | `AI prompt logs` — delete after 90 days unless evidence hold | delete | vs inspection/AI evidence needs (INJ-050, INJ-084) |
| Legal hold | LH-44 active on NCB204-301 and NCB204-B24071 | preserve | Blocks deletion for scoped records |
| Residency | `data_residency.csv`; `backup_inventory.csv` | Stay in approved regions | INJ-064 unapproved backup region |

Resolution policy for INJ-035 (decision D-204; aligned with D-401):

1. Legal hold and explicit GxP retain rules suppress automated deletion.
2. Privacy DSR remains open and visible; fulfillment is a human Legal + Privacy + GxP co-decision.
3. AEGIS may recommend hold/retain/delete options with citations; it never executes deletion against active holds.
4. AI logs under hold are retained with purpose limitation and access control.

## 7. Stewardship and issue remediation

| Issue type | Steward | Remediation path | AEGIS role |
|---|---|---|---|
| Unit mapping approval | QC / Data standards | Change-controlled mapping update | Abstain until approved |
| IDMP ambiguity | Regulatory MDM | Stewardship per `IDMP_MASTER_DATA_GOVERNANCE.md` | Dual-cite |
| Audit-trail gap | IT Quality / CSV | Investigate privileged session; assess impacted records | Flag suspect window |
| Shared account | Lab management | Unique credentials; retrospective attribution where possible | Mark attributable=false |
| Unapproved spreadsheet | Quality systems | Retire or validate under CSV | Exclude from authoritative calc |
| CAPA recurrence | Quality | Reopen effectiveness; align taxonomy | Similarity link only |
| Vendor hotfix | Change control + vendor mgmt | Retrospective approval or rollback | Surface bypass |
| Missing original CoA | Supplier quality | Obtain signed source or document gap for QP | Cite lineage break |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|
| R-601 | Risk | Pressure to meet BR-01 tempts silent unit conversion | Hard-gate failure | GxP | INJ-024 tests | Open |
| R-602 | Assumption | Fixture-scale lineage is representative for POC defence | Production volumes need stronger stores | Architecture | Phase 5 | Accepted for POC |
| R-603 | Gap | Full personal-data ROPA deferred to privacy artefact Phase 4 | Residual privacy design debt | Security/privacy | Artefact 17 | Open |
| R-604 | Risk | Deleting AI logs at day 90 destroys inspection evidence if hold missed | INJ-050 / INJ-084 failure | GxP + Privacy | Retention job design | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| ALCOA+ defects visible, not overwritten | §4 tags + immutable originals | Integrity tests on LR-88, CoA lineage | E-610, E-611 | Design accepted |
| Retention conflict handled without auto-delete | D-204 / §6 | Hold vs DSR scenario test | E-609 | Design accepted |
| Unit/time integrity | Mapping approval + timezone rules | INJ-024, INJ-018 fixtures | E-611, E-612 | Design accepted |
| Authority contextual | §2 matrix | Authority selection review | Case fact pack | Design accepted |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| GxP/quality lead | GxP | Require explicit INJ-035 policy | Captured as D-204 / §6 | 2026-08-10 |
| Security/privacy lead | Privacy | No automated DSR fulfillment | Confirmed §6 step 3 | 2026-08-10 |
| Domain/evidence lead | Domain | ALCOA+ table covers A–C | Confirmed §4 | 2026-08-10 |
