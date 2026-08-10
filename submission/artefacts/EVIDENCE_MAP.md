# Evidence Map — Project AEGIS-PHARMA (Phase 2)

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Domain / evidence lead |
| Version / date | 1.0 / 2026-08-10 |
| Status | Reviewed |
| Related | `data/inject_evidence_map.csv`; `data/injects.json`; `case/INTEGRATED_CASE.md` §7; artefacts 05–09 |

## Purpose

Map challenge injects to data files, knowledge documents, source documents and case packs with authority, effective-time notes, conflicts and gaps. Provide a complete summary register for INJ-001..084 (D01–D13) and deep dives for Workflows A/B/C plus cross-cutting authority, identity, time and unit integrity.

Participant status in package CSV remains `UNASSESSED`; Team 3 assessment column below records Phase 2 disposition for POC scope.

Assessment values: In-scope POC | Supporting | Deferred (out of A–C write path) | Hard-gate control.

---

## 1. How to read this map

| Column | Meaning |
|---|---|
| Evidence paths | Paths relative to package root under `data/`, `knowledge/`, `source_documents/`, `case/` |
| Authority | Declared or inferred steward; “contextual” means per `case/SOURCE_SYSTEM_FACT_PACK.md` |
| Effective time | Known dates from fixtures/docs, or precision limitation |
| Conflicts / gaps | Deliberate challenge conditions to preserve, not silently repair |

Primary indexes already shipped by the package: `data/inject_evidence_map.csv`, `data/injects.json`, `data/document_catalog.csv`, `data/knowledge_catalog.csv`, `data/RELATIONSHIP_MODEL.csv`, `data/DATASET_PROFILE.csv`.

---

## 2. Complete inject register (INJ-001..084)

Paths abbreviated: files live under `data/` unless prefixed `knowledge/` or `source_documents/` or `case/`.

| Inject | Dim | Title | Evidence paths | Authority / time notes | Conflicts / gaps | Team 3 assessment |
|---|---|---|---|---|---|---|
| INJ-001 | D01 | Board compression target | `board_requests.csv`; `portfolio_products.csv`; `case/INTEGRATED_CASE.md` | Board request BR-01 due 2026-11-30 | Speed vs Quality independence | In-scope POC (value) |
| INJ-002 | D01 | Conflicting success metrics | `kpi_conflicts.csv`; `stakeholders.csv`; `case/STAKEHOLDER_PACK.md` | KPI owners concurrent | Incompatible targets | Supporting |
| INJ-003 | D01 | No-AI challenge | `no_ai_baselines.csv` | Process-excellence estimates | Relative % not audited history | In-scope POC |
| INJ-004 | D01 | Patent-cliff urgency | `portfolio_products.csv`; `commercial_forecast.csv` | Portfolio 19-month horizon | Schedule pressure ≠ waiver | Supporting |
| INJ-005 | D01 | Acquisition integration | `organisations.csv`; `system_inventory.csv`; case §2 | NTG / BIOX / CMO-IE | Incompatible ids/tenancy | In-scope POC (identity) |
| INJ-006 | D01 | Prohibited optimization | `ai_use_boundaries.csv` | Executive boundary | Hard prohibitions | Hard-gate control |
| INJ-007 | D02 | Assay drift | `assay_results.csv`; `instruments.csv`; `reagent_lots.csv` | QC / research assays | Comparability disputed | Deferred |
| INJ-008 | D02 | Compound genealogy collision | `compounds.csv`; `substance_master.csv` | Research registry | Shared local code, different structure | Supporting (identity) |
| INJ-009 | D02 | Omics cohort bias | `omics_cohorts.csv`; `model_performance.csv` | Translational models | Ancestry performance gap | Deferred |
| INJ-010 | D02 | Preclinical image manipulation | `preclinical_studies.csv`; `image_forensics.csv` | CRO report metadata | Duplication concern | Deferred |
| INJ-011 | D02 | Unqualified research model | `model_registry.csv` | Model governance | No intended use / locked set | Supporting (model trust) |
| INJ-012 | D02 | Target-evidence conflict | `target_evidence.csv`; `data_licenses.csv` | Internal vs licensed | Disagreement + licence limits | Deferred |
| INJ-013 | D03 | Protocol-version divergence | `clinical_trials.csv`; `protocol_versions.csv`; `site_approvals.csv`; `source_documents/Protocol_NCB204_301_v4_1.md`; `v5_0.md` | Clinical / country approval | Sites on mixed versions | Supporting (temporal) |
| INJ-014 | D03 | Eligibility ambiguity | `subjects.csv`; `eligibility_evidence.csv` | Central vs local lab | AI must not determine eligibility | Hard-gate control |
| INJ-015 | D03 | Randomization outage | `randomization_events.csv`; `downtime_events.csv` | IRT / manual log | Emergency assignment | Deferred |
| INJ-016 | D03 | Potential unblinding | `support_tickets.csv`; `access_logs.csv` | Site support | Treatment-arm hints | Deferred |
| INJ-017 | D03 | eConsent withdrawal mismatch | `consents.csv`; `specimens.csv`; `processing_events.csv` | eConsent vs lab | Processing after withdrawal | Supporting (privacy) |
| INJ-018 | D03 | Device clock skew | `wearable_readings.csv`; `timezone_rules.csv` | Device / site TZ; DST 2026-03-29 | local_unknown vs UTC | In-scope POC (time) |
| INJ-019 | D03 | Endpoint adjudication backlog | `endpoint_packets.csv`; `imaging_reviews.csv` | Imaging core | Missing docs; conflicting reviews | Deferred |
| INJ-020 | D03 | Site inspection risk | `site_metrics.csv`; `access_logs.csv` | Clinical quality | Credential sharing pattern | Deferred |
| INJ-021 | D04 | Biologics genealogy break | `batches.csv`; `material_genealogy.csv`; `warehouse_movements.csv` | MES vs warehouse; batch 2026-07-10 | SUA-88 missing_branch vs issued | In-scope POC (A) |
| INJ-022 | D04 | Sterility excursion | `environmental_monitoring.csv`; `microbiology_results.csv`; `knowledge/STERILE_MANUFACTURING_ESCALATION.md` | EM / micro | Organism id corrected later | In-scope POC (A) |
| INJ-023 | D04 | OOS/OOT disagreement | `lab_results.csv`; `oos_investigations.csv`; `knowledge/OOS_OOT_INVESTIGATION.md` | LIMS vs stats vs notebook | Triple status conflict | In-scope POC (A) |
| INJ-024 | D04 | Unit conversion defect | `lab_results.csv`; `interface_mappings.csv`; `source_documents/LIMS_result_contract_v1.md`; `v2.md` | CRO→LIMS interface; approved=no | mg/L vs µg/mL | In-scope POC (unit) |
| INJ-025 | D04 | eBR exception | `ebr_steps.csv`; `downtime_events.csv` | eBR | Back-entry after degradation | In-scope POC (A) |
| INJ-026 | D04 | Cleaning validation boundary | `cleaning_validation.csv`; `production_schedule.csv` | Validation / scheduling | Campaign sequence change | Supporting (A) |
| INJ-027 | D04 | PAT drift | `pat_models.csv`; `recipes.csv` | PAT vs recipe | Version desync | Supporting (A) |
| INJ-028 | D04 | QP evidence gap | `release_packets.csv`; `supplier_audits.csv`; `source_documents/CMO_audit_commitment_2025_14.md` | QP / supplier quality | Missing commitment confirmation | In-scope POC (A) |
| INJ-029 | D05 | Audit-trail disabled | `audit_trails.csv`; `privileged_sessions.csv` | System audit | 47-minute gap | In-scope POC (integrity) |
| INJ-030 | D05 | Shared laboratory account | `access_logs.csv`; `staff_rosters.csv` | Lab access | Attributability break | In-scope POC (integrity) |
| INJ-031 | D05 | Validation-state ambiguity | `system_inventory.csv`; `validation_inventory.csv` | CSV inventories | Triple label conflict | In-scope POC (authority) |
| INJ-032 | D05 | Unapproved spreadsheet | `spreadsheet_inventory.csv` | QC calc | No verified history | Supporting |
| INJ-033 | D05 | CAPA effectiveness failure | `deviations.csv`; `capa_records.csv` | QMS | Taxonomy drift recurrence | Supporting (A) |
| INJ-034 | D05 | Change-control bypass | `change_controls.csv`; `vendor_releases.csv` | Change control | Hotfix lacking retrospective approval | Supporting |
| INJ-035 | D05 | Record-retention conflict | `retention_rules.csv`; `legal_holds.csv`; `deletion_requests.csv` | Legal LH-44 active; DSR-17 open | Retain vs delete | In-scope POC (retention) |
| INJ-036 | D05 | ALCOA+ provenance break | `certificates_analysis.csv`; `document_lineage.csv`; `knowledge/GXP_DATA_INTEGRITY_STANDARD.md` | CoA lineage | Transcribed; original missing | In-scope POC (A) |
| INJ-037 | D06 | ICSR duplicate cluster | `icsr_cases.csv`; `duplicate_candidates.csv`; `product_master_aliases.csv`; `knowledge/PV_DUPLICATE_MANAGEMENT.md` | Safety DB / vendors | Same event, different names | In-scope POC (B) |
| INJ-038 | D06 | Reporting-clock conflict | `icsr_cases.csv`; `safety_receipts.csv`; `knowledge/PV_REPORTING_CLOCKS.md` | Multi-channel receipt | Awareness dates disagree | In-scope POC (B) |
| INJ-039 | D06 | MedDRA version mismatch | `adverse_events.csv`; `terminology_versions.csv` | MedDRA 27.1 vs 28.0 | PT/signal grouping shift | In-scope POC (B) |
| INJ-040 | D06 | Expectedness source conflict | `listedness_sources.csv`; `product_labels.csv`; `source_documents/CCDS_NCB204_v4.md` (eff. 2026-03-18); `knowledge/PV_LISTEDNESS_AUTHORITY.md` | IB/CCDS/local label | IN label not listed | In-scope POC (B) |
| INJ-041 | D06 | Pregnancy/paediatric sensitivity | `icsr_cases.csv`; `sensitive_segments.csv` | PV privacy | Elevated role required | In-scope POC (B/PRI) |
| INJ-042 | D06 | Social-media authenticity | `social_listening.csv` | Social listening | Unidentifiable reporter | In-scope POC (B) |
| INJ-043 | D06 | Product-quality and safety link | `product_complaints.csv`; `icsr_cases.csv` | Complaint + PV | Lot linkage uncertain | Supporting (B) |
| INJ-044 | D06 | Signal disproportionality instability | `signal_metrics.csv`; `exposure_estimates.csv` | Signal science | Duplicate/exposure sensitivity | Supporting (B advisory) |
| INJ-045 | D07 | IDMP identity conflict | `medicinal_products.csv`; `idmp_mappings.csv`; `knowledge/IDMP_MASTER_DATA_GOVERNANCE.md` | RIM vs ERP | Strength/form/substance disagree | In-scope POC (identity) |
| INJ-046 | D07 | Labeling divergence | `product_labels.csv`; `market_authorisations.csv` | Regional labels | EU vs US vs distributor | Supporting (B/C) |
| INJ-047 | D07 | Commitment deadline ambiguity | `regulatory_commitments.csv`; `authority_correspondence.csv`; `source_documents/EMA_letter_2026_114.md` (2026-07-28) | Authority correspondence | Conflicting due dates | Supporting |
| INJ-048 | D07 | eCTD sequence gap | `ectd_sequences.csv`; `document_catalog.csv` DOC-ECTD-1 | Submission archive | referenced_missing file | Supporting (gap honesty) |
| INJ-049 | D07 | Variation classification dispute | `regulatory_changes.csv` | Regulatory | Reportability disagreement | Deferred |
| INJ-050 | D07 | Inspection request surge | `inspection_requests.csv` | Regulators; 72h | Cross-domain pack need | Supporting (export) |
| INJ-051 | D08 | Cold-chain lane excursion | `shipments.csv`; `temperature_loggers.csv`; `source_documents/Cold_chain_logger_association_SH_901.md`; `knowledge/COLD_CHAIN_ASSESSMENT.md` | Logistics / logger | P-88 vs P-89; TZ mix | In-scope POC (C) |
| INJ-052 | D08 | Serialization aggregation break | `serialisation_events.csv`; `packaging_events.csv`; `knowledge/SERIALISATION_AND_RETURNS.md` | Serialisation | Case-to-pallet missing | Supporting (C) |
| INJ-053 | D08 | Counterfeit suspicion | `returns.csv`; `serialisation_events.csv` | Returns | Valid-looking serials, bad history | Supporting (C) |
| INJ-054 | D08 | Critical excipient shortage | `supplier_risks.csv`; `inventory.csv` | Supplier / inventory | 8-week recovery estimate | In-scope POC (C) |
| INJ-055 | D08 | CMO capacity conflict | `cmo_capacity.csv`; `vendor_contracts.csv` | CMO portal | Double-promised capacity | Supporting (C) |
| INJ-056 | D08 | Allocation ethics | `demand_forecast.csv`; `inventory.csv`; `allocation_constraints.csv`; `knowledge/SUPPLY_ALLOCATION_ETHICS.md` | Supply ethics | Demand > stock; no AI allocate | In-scope POC (C) |
| INJ-057 | D08 | Customs documentation mismatch | `shipments.csv`; `trade_documents.csv` | Trade | Description vs licence | Supporting (C) |
| INJ-058 | D08 | Recall-scope uncertainty | `recall_candidates.csv`; `material_genealogy.csv` | Quality / supply | Incomplete genealogy links | Supporting (multi-hop revisit) |
| INJ-059 | D09 | Genomic re-identification | `genomic_data.csv`; `privacy_risk.csv`; `knowledge/GENOMIC_DATA_STANDARD.md` | Privacy | High identifying combinations | Deferred |
| INJ-060 | D09 | Cross-border secondary use | `consents.csv`; `data_exports.csv`; `knowledge/ECONSENT_AND_SECONDARY_USE.md` | Consent | Purpose not explicit | Supporting (PRI) |
| INJ-061 | D09 | DSR versus GxP record | `deletion_requests.csv`; `retention_rules.csv` | Privacy + GxP | Linked to INJ-035 | In-scope POC (PRI) |
| INJ-062 | D09 | Patient-support leakage | `patient_support_cases.csv` | Support programme | Excess free text | Deferred |
| INJ-063 | D09 | Research-commercial boundary | `data_licenses.csv`; `commercial_use_requests.csv` | Licence | Commercial targeting risk | Supporting (PRI) |
| INJ-064 | D09 | Regional residency failure | `data_residency.csv`; `backup_inventory.csv` | Residency policy | Unapproved backup region | Supporting (PRI) |
| INJ-065 | D10 | Prompt injection in SOP | `knowledge_catalog.csv`; `knowledge/MALICIOUS_SUPPLIER_DEVIATION.md` | Untrusted supplier PDF | Hidden ignore-hold instructions | Hard-gate control |
| INJ-066 | D10 | Tool-manifest poisoning | `tool_catalog.csv`; `tool_manifest_poisoned.json` | Tool registry | Silent disposition write request | Hard-gate control |
| INJ-067 | D10 | Entitlement revocation lag | `users_entitlements.csv`; `access_cache.csv` | IAM vs gateway cache | Stale allow risk | Hard-gate control |
| INJ-068 | D10 | Safety-data exfiltration | `security_events.csv` | Security monitoring | Crafted cross-affiliate pull | Hard-gate control |
| INJ-069 | D10 | Ransomware / OT segmentation | `downtime_events.csv`; `network_zones.csv` | OT / IT | MES/QMS degraded | Supporting (continuity) |
| INJ-070 | D10 | Model supply-chain compromise | `model_registry.csv`; `model_artifacts.csv` | Model governance | Hash mismatch | Hard-gate control |
| INJ-071 | D11 | Automation bias | `candidate_outputs.csv`; `reviewer_feedback.csv` | Human factors | Omitted critical deviation | In-scope POC (A UX) |
| INJ-072 | D11 | Language inequity | `model_performance.csv`; `icsr_cases.csv`; `knowledge/PV_MULTILINGUAL_REVIEW.md` | PV / models | AR/HI quality gap | In-scope POC (B) |
| INJ-073 | D11 | Accessibility failure | `usability_findings.csv` | UX | Keyboard / colour-only | In-scope POC (NFR) |
| INJ-074 | D11 | Role conflict | `stakeholders.csv`; `decision_rights.csv`; `case/STAKEHOLDER_PACK.md` | RAPID | Global vs local accountability | Supporting (gov) |
| INJ-075 | D12 | Model price shock | `model_costs.csv`; `vendor_contracts.csv` | FinOps | +70% token price | Supporting |
| INJ-076 | D12 | Denial-of-wallet | `model_usage.csv`; `security_events.csv` | FinOps / security | Oversized submissions | Supporting |
| INJ-077 | D12 | Hidden human-review cost | `cost_model.csv`; `staff_rates.csv` | Business case | Review minutes omitted | Supporting |
| INJ-078 | D12 | Vendor concentration | `vendor_dependencies.csv` | Vendor mgmt | Single provider stack | Supporting (KG avoid) |
| INJ-079 | D13 | Regional platform outage | `downtime_events.csv`; `model_endpoints.csv` | Platform | Batch review + PV during outage | In-scope POC (continuity) |
| INJ-080 | D13 | Checkpoint corruption | `agent_runs.csv` | Agent runtime | Stale resume; draft reservations | Hard-gate control (C) |
| INJ-081 | D13 | Model substitution regression | `model_performance.csv`; `model_endpoints.csv` | Model ops | Schema ok, fidelity loss | Supporting |
| INJ-082 | D13 | AI-disabled continuity | `continuity_requirements.csv`; `knowledge/AI_DISABLED_CONTINUITY.md` | Continuity | 14-day / PV manual | In-scope POC |
| INJ-083 | D13 | Vendor exit deadline | `vendor_contracts.csv`; `vendor_exit_assets.csv`; `knowledge/VENDOR_EXIT_AND_RETIREMENT.md` | Vendor | 120 days; incomplete export | Supporting |
| INJ-084 | D13 | Retirement evidence preservation | `retention_rules.csv`; `retirement_assets.csv` | Retention / CSV | Inspectability after retire | Supporting |

---

## 3. Deep dive — Workflow A (batch evidence reconciliation)

### 3.1 Anchor objects

| Object | Fixture key | Status / date | Notes |
|---|---|---|---|
| Batch | NCB204-B24071 | quality_hold; manufacture_date 2026-07-10; site CMO-IE | Primary pack |
| Product | NCB-204 / NCB204-DE | IDMP conflict (INJ-045) | Cite both if product identity in scope |
| Material lot | SUA-88 | MES `missing_branch`; warehouse WM-90 issued | Core genealogy conflict |
| Lab result | LR-88 potency 0.92 mg/L; spec 0.85–1.05 ug/mL; OOS_LIMS | Unit defect | |
| Interface | CRO_LAB_TO_LIMS | conversion_rule 1:1_assumed; approved=no | Must abstain |

### 3.2 Evidence chain

1. **Identity / org:** `data/organisations.csv` (NTG, BIOX, CMO-IE); `data/system_inventory.csv` (LIMS-4 validated vs BIOX-ELN acquired).
2. **Genealogy:** `data/material_genealogy.csv` + `data/warehouse_movements.csv` → INJ-021 conflict.
3. **Lab/unit:** `data/lab_results.csv` + `data/interface_mappings.csv` + LIMS contracts in `source_documents/` → INJ-024.
4. **OOS narrative:** `data/oos_investigations.csv` + `knowledge/OOS_OOT_INVESTIGATION.md` → INJ-023.
5. **EM/sterility:** `data/environmental_monitoring.csv`; `data/microbiology_results.csv`; `knowledge/STERILE_MANUFACTURING_ESCALATION.md` → INJ-022.
6. **eBR/time:** `data/ebr_steps.csv`; `data/downtime_events.csv` → INJ-025 contemporaneous defect.
7. **QP gap:** `data/release_packets.csv`; `data/supplier_audits.csv`; `source_documents/CMO_audit_commitment_2025_14.md` → INJ-028.
8. **Integrity overlays:** audit gap INJ-029; shared account INJ-030; CoA transcription INJ-036; validation ambiguity INJ-031.
9. **Policy:** prefer `knowledge/BATCH_RELEASE_EVIDENCE_POLICY.md` over `knowledge/BATCH_RELEASE_POLICY_OLD.md` after catalog status check; `knowledge/GXP_DATA_INTEGRITY_STANDARD.md` (eff. 2026-02-15).
10. **Human factors:** `data/candidate_outputs.csv` omitted critical deviation → INJ-071.

### 3.3 Authority, conflicts, gaps

| Topic | Authority stance | Conflict / gap |
|---|---|---|
| Genealogy truth | None single; MES and warehouse both citeable | Broken branch |
| Unit | Approved mapping only | Mapping unapproved |
| Release decision | Human QP / Quality systems only | AEGIS readiness ≠ disposition |
| Missing eCTD analytic file | Archive declares referenced_missing | Do not fabricate DOC-ECTD-1 |

### 3.4 Planned POC outputs

Batch Evidence Pack with contradiction board; abstentions; citation list; no disposition fields (FR-A-*; TEST-A-*).

---

## 4. Deep dive — Workflow B (PV intake / signal support)

### 4.1 Anchor objects

| Object | Fixture key | Notes |
|---|---|---|
| Cases | PV-1001, PV-1014 (+ PV-1009 candidate) | Duplicate cluster |
| Codings | Anaphylactic reaction @ MedDRA 27.1; Infusion related reaction @ 28.0 | INJ-039 |
| Listedness | NCB-204 anaphylaxis: IB yes; CCDS yes; IN local label no | INJ-040 |
| CCDS extract | `source_documents/CCDS_NCB204_v4.md` effective 2026-03-18 | Approved synthetic extract |
| Sensitive | `sensitive_segments.csv` / RELATIONSHIP_MODEL exception for restricted stub | INJ-041 |

### 4.2 Evidence chain

1. **Intake corpus:** `data/icsr_cases.csv`; receipts in `data/safety_receipts.csv` → clock conflict INJ-038.
2. **Duplicates:** `data/duplicate_candidates.csv` similarity 0.93 / 0.71; aliases in `data/product_master_aliases.csv` → INJ-037.
3. **Terminology:** `data/adverse_events.csv` + `data/terminology_versions.csv` → INJ-039.
4. **Listedness:** `data/listedness_sources.csv` + `data/product_labels.csv` + CCDS + `knowledge/PV_LISTEDNESS_AUTHORITY.md` → INJ-040.
5. **Policies:** `knowledge/PHARMACOVIGILANCE_CASE_POLICY.md`; `knowledge/PV_DUPLICATE_MANAGEMENT.md`; `knowledge/PV_REPORTING_CLOCKS.md`; `knowledge/PV_MULTILINGUAL_REVIEW.md`.
6. **Authenticity:** `data/social_listening.csv` → INJ-042 abstain path.
7. **Complaint link:** `data/product_complaints.csv` → INJ-043 supporting.
8. **Signal instability:** `data/signal_metrics.csv`; `data/exposure_estimates.csv` → INJ-044 advisory only.
9. **Language equity:** `data/model_performance.csv` with icsr language mix → INJ-072.
10. **Trust:** reject `knowledge/FAKE_PV_EXPEDITED_RULE.md` if catalog marks untrusted/fake.

### 4.3 Authority, conflicts, gaps

| Topic | Authority stance | Conflict / gap |
|---|---|---|
| Expectedness | Source- and jurisdiction-specific | IN label vs CCDS |
| MedDRA | Versioned coding retained | Cross-version grouping risk |
| Final PV medical judgements | Human only (`ai_use_boundaries.csv`) | System clusters/cites only |
| Restricted case stub | RELATIONSHIP_MODEL declared_exception | Absent restricted case must not be invented |

### 4.4 Planned POC outputs

Human-ready case file: extracted fields, duplicate candidates, clock board, listedness matrix, sensitive-segment gates; no causality/seriousness/reportability/signal confirmation.

---

## 5. Deep dive — Workflow C (supply / cold-chain options)

### 5.1 Anchor objects

| Object | Fixture key | Notes |
|---|---|---|
| Shipment | SH-901 NCB-204 lot NCB204-B24062 IE→DE; quarantine; logger LG-31; pallet P-88 | Cold-chain |
| Logger rows | LG-31 temps with pallet P-89 local_unknown and P-88 UTC | Association dispute |
| Source note | `source_documents/Cold_chain_logger_association_SH_901.md` | Association evidence |
| Shortage | `supplier_risks.csv` + `inventory.csv` | INJ-054 |
| Ethics constraints | `allocation_constraints.csv`; `demand_forecast.csv` | INJ-056 |
| Agent risk | `agent_runs.csv` draft_reservations | INJ-080 must fail closed |

### 5.2 Evidence chain

1. **Shipment/logger:** `data/shipments.csv`; `data/temperature_loggers.csv`; cold-chain source doc; `knowledge/COLD_CHAIN_ASSESSMENT.md` → INJ-051.
2. **Quality/MA constraints:** batch/product quality status; `data/market_authorisations.csv` → block options that ignore holds/MA.
3. **Shortage/CMO:** `data/supplier_risks.csv`; `data/inventory.csv`; `data/cmo_capacity.csv`; `data/vendor_contracts.csv` → INJ-054/055.
4. **Ethics:** `data/allocation_constraints.csv`; `data/demand_forecast.csv`; `knowledge/SUPPLY_ALLOCATION_ETHICS.md` → INJ-056 options only.
5. **Serialization/returns:** `data/serialisation_events.csv`; `data/packaging_events.csv`; `data/returns.csv` → INJ-052/053 supporting.
6. **Customs:** `data/trade_documents.csv` → INJ-057.
7. **Recall scope:** `data/recall_candidates.csv` + genealogy → INJ-058 (options/impact analysis only; no recall initiation).
8. **Continuity:** `data/continuity_requirements.csv`; `knowledge/AI_DISABLED_CONTINUITY.md` → INJ-082.

### 5.3 Authority, conflicts, gaps

| Topic | Authority stance | Conflict / gap |
|---|---|---|
| Logger–pallet association | Unresolved until human logistics/QA | Dual pallet ids |
| Allocation/shipment | Human supply execution only | No AEGIS write tools |
| RELATIONSHIP_MODEL note | LG-42 optional readings absent | Do not invent logger data for SH-902 |

### 5.4 Planned POC outputs

Ranked option pack with constraints, cold-chain dispute board, ethics flags; zero reservations/allocations/shipments/recalls.

---

## 6. Cross-cutting integrity themes

### 6.1 Authority

| Issue | Injects | Map stance |
|---|---|---|
| No universal SoR | Fact pack | Authority by object/context/time |
| Validation label conflict | INJ-031 | Abstain on “validated” claims until reconciled |
| Policy supersession | BATCH_RELEASE_* ; protocol v4.1/v5.0 | Effective date + status required |
| Untrusted content | INJ-065, fake PV rule | Data only |
| Executive prohibitions | INJ-006 | Hard gate across A–C |

### 6.2 Identity

| Issue | Injects | Map stance |
|---|---|---|
| Acquisition BIOX | INJ-005 | Org-prefixed identifiers |
| Compound collision | INJ-008 | Structure/salt distinguish |
| IDMP strength/form | INJ-045 | Dual cite; no auto-merge |
| Product aliases | aliases CSV | Retrieval aids only |
| Duplicate cases via aliases | INJ-037 | Cluster with citations |

### 6.3 Time

| Issue | Injects | Map stance |
|---|---|---|
| Wearable DST / unknown TZ | INJ-018 | Preserve timezone tags |
| Logger mixed clocks | INJ-051 | Same |
| PV awareness channels | INJ-038 | Multi-clock board |
| eBR back-entry | INJ-025 | Contemporaneous defect tag |
| Commitment due dates | INJ-047 | Keep both correspondence and tracker dates |
| E2B precision variable | `api_contract_versions.csv` | Do not over-precision |

### 6.4 Unit

| Issue | Injects | Map stance |
|---|---|---|
| mg/L vs µg/mL unapproved | INJ-024 | Abstain (D-010) |
| LIMS contract field rename | LIMS v1/v2 docs | Version-aware ACL |
| Genealogy quantity unit | warehouse `assembly` | Preserve as received |

### 6.5 Retention / privacy intersection

| Issue | Injects | Map stance |
|---|---|---|
| LH-44 vs DSR-17 vs AI log delete-90d | INJ-035, INJ-061 | Legal hold + GxP retain suppress auto-delete (D-204) |
| Residency | INJ-064 | Flag unapproved region |

---

## 7. Knowledge and source-document quick index

| Path | Role in Phase 2 |
|---|---|
| `case/INTEGRATED_CASE.md` | Inject catalogue and workflow mandate |
| `case/SOURCE_SYSTEM_FACT_PACK.md` | System landscape; contextual authority |
| `case/STAKEHOLDER_PACK.md` | Decision tension |
| `case/REGULATORY_BOUNDARY_PACK.md` | Regulatory boundary cues |
| `knowledge/GXP_DATA_INTEGRITY_STANDARD.md` | ALCOA+ |
| `knowledge/IDMP_MASTER_DATA_GOVERNANCE.md` | Identity non-merge |
| `knowledge/PV_*.md` | PV clocks, duplicates, listedness, multilingual |
| `knowledge/COLD_CHAIN_ASSESSMENT.md` | Cold-chain assessment cues |
| `knowledge/SUPPLY_ALLOCATION_ETHICS.md` | Ethics constraints |
| `knowledge/MALICIOUS_SUPPLIER_DEVIATION.md` | Prompt-injection fixture |
| `knowledge/AI_DISABLED_CONTINUITY.md` | Continuity |
| `source_documents/LIMS_result_contract_v1.md` / `v2.md` | Unit/status contract drift |
| `source_documents/CCDS_NCB204_v4.md` | Listedness source extract |
| `source_documents/Cold_chain_logger_association_SH_901.md` | SH-901 association |
| `source_documents/CMO_audit_commitment_2025_14.md` | QP gap support |
| `source_documents/EMA_letter_2026_114.md` | Commitment date ambiguity |
| `source_documents/Protocol_NCB204_301_v4_1.md` / `v5_0.md` | Protocol temporal divergence |

Always re-check `data/knowledge_catalog.csv` and `data/document_catalog.csv` for status, authority and availability before use.

---

## 8. Gaps intentionally left open

| Gap | Why open | Handling |
|---|---|---|
| DOC-ECTD-1 missing bytes | Challenge `intentionally_absent` | Investigate/cite absence; never fabricate |
| IDMP mapping ambiguous | Stewardship required | Dual citation |
| Logger–pallet unresolved | Logistics/QA human | Abstain on single truth |
| DSR-17 open under LH-44 | Legal/Privacy/GxP co-decision | D-204 |
| Full clinical/research inject deep automation | Outside D-001 POC scope | Register only; deferred assessment |

---

## 9. Traceability

| Phase 2 artefact | Uses this map |
|---|---|
| `05_DDD_CONTEXT_MAP.md` | INJ-005, 021, 045; system ACLs |
| `06_DATA_GOVERNANCE_INTEGRITY.md` | INJ-018, 024, 029–036 |
| `07_ONTOLOGY_SEMANTIC_LAYER.md` | INJ-039, 040, 045 |
| `08_KNOWLEDGE_GRAPH_DECISION.md` | INJ-021, 037, 051, 058 |
| `09_REQUIREMENTS_TRACEABILITY.md` | Workflow A/B/C requirement tests |
| `ASSUMPTIONS_AND_DECISION_LOG.md` | A-201+ / D-201+ |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Domain/evidence lead | Domain | All 84 injects listed with paths | §2 complete | 2026-08-10 |
| GxP/quality lead | GxP | Workflow A deep dive sufficient for pack design | §3 accepted | 2026-08-10 |
| PV reviewer | Safety | Workflow B listedness/MedDRA covered | §4 accepted | 2026-08-10 |
| Supply reviewer | Supply | Cold-chain and no-allocate stance clear | §5 accepted | 2026-08-10 |
