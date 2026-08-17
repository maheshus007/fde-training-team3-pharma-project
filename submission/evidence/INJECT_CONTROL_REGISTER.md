# Inject control register

Executable trace of INJ-001..084 from `submission/src/inject_controls.py`.
Challenge files are cited, not rewritten. Case/data tensions are recorded.

| Inject | Title | Action | Owner | Evidence | Notes |
|---|---|---|---|---|---|
| INJ-001 | Board compression target | surface | product_governance | `data/board_requests.csv; data/portfolio_products.csv` | Business/value inject; cited as constraint, not automated optimisation. |
| INJ-002 | Conflicting success metrics | record_conflict | product_governance | `data/kpi_conflicts.csv; data/stakeholders.csv` | Preserve all cited KPI rows; do not invent a Supply service-level row. |
| INJ-003 | No-AI challenge | surface | product_governance | `data/no_ai_baselines.csv` | Business/value inject; cited as constraint, not automated optimisation. |
| INJ-004 | Patent-cliff urgency | surface | product_governance | `data/portfolio_products.csv; data/commercial_forecast.csv` | Business/value inject; cited as constraint, not automated optimisation. |
| INJ-005 | Acquisition integration | surface | product_governance | `data/organisations.csv; data/system_inventory.csv` | Business/value inject; cited as constraint, not automated optimisation. |
| INJ-006 | Prohibited optimization | deny | policy_guard | `data/ai_use_boundaries.csv` | Hard-gate deny path. |
| INJ-007 | Assay drift | abstain | research_clinical_boundary | `data/assay_results.csv; data/instruments.csv; data/reagent_lots.csv` | D-203 / INJ-006: no discovery or clinical write-path decision. |
| INJ-008 | Compound genealogy collision | surface | workflow_a_b_c | `data/compounds.csv; data/substance_master.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-009 | Omics cohort bias | abstain | research_clinical_boundary | `data/omics_cohorts.csv; data/model_performance.csv` | D-203 / INJ-006: no discovery or clinical write-path decision. |
| INJ-010 | Preclinical image manipulation concern | abstain | research_clinical_boundary | `data/preclinical_studies.csv; data/image_forensics.csv` | D-203 / INJ-006: no discovery or clinical write-path decision. |
| INJ-011 | Unqualified research model | abstain | research_clinical_boundary | `data/model_registry.csv` | D-203 / INJ-006: no discovery or clinical write-path decision. |
| INJ-012 | Target-evidence conflict | abstain | research_clinical_boundary | `data/target_evidence.csv; data/data_licenses.csv` | D-203 / INJ-006: no discovery or clinical write-path decision. |
| INJ-013 | Protocol-version divergence | abstain | clinical_protocol | `data/clinical_trials.csv; data/protocol_versions.csv; data/site_approvals.csv` | Protocol/eligibility conflicts retained; eligibility not decided. |
| INJ-014 | Eligibility ambiguity | abstain | clinical_protocol | `data/subjects.csv; data/eligibility_evidence.csv` | Protocol/eligibility conflicts retained; eligibility not decided. |
| INJ-015 | Randomization service outage | abstain | research_clinical_boundary | `data/randomization_events.csv; data/downtime_events.csv` | D-203 / INJ-006: no discovery or clinical write-path decision. |
| INJ-016 | Potential unblinding | abstain | research_clinical_boundary | `data/support_tickets.csv; data/access_logs.csv` | D-203 / INJ-006: no discovery or clinical write-path decision. |
| INJ-017 | eConsent withdrawal mismatch | abstain | research_clinical_boundary | `data/consents.csv; data/specimens.csv; data/processing_events.csv` | D-203 / INJ-006: no discovery or clinical write-path decision. |
| INJ-018 | Decentralized-device clock skew | surface | workflow_a_b_c | `data/wearable_readings.csv; data/timezone_rules.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-019 | Endpoint adjudication backlog | abstain | research_clinical_boundary | `data/endpoint_packets.csv; data/imaging_reviews.csv` | D-203 / INJ-006: no discovery or clinical write-path decision. |
| INJ-020 | Site inspection risk | abstain | research_clinical_boundary | `data/site_metrics.csv; data/access_logs.csv` | D-203 / INJ-006: no discovery or clinical write-path decision. |
| INJ-021 | Biologics batch genealogy break | surface | workflow_a_b_c | `data/batches.csv; data/material_genealogy.csv; data/warehouse_movements.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-022 | Sterility excursion | surface | workflow_a_b_c | `data/environmental_monitoring.csv; data/microbiology_results.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-023 | OOS/OOT disagreement | surface | workflow_a_b_c | `data/lab_results.csv; data/oos_investigations.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-024 | Unit conversion defect | surface | workflow_a_b_c | `data/lab_results.csv; data/interface_mappings.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-025 | Electronic batch record exception | surface | workflow_a_b_c | `data/ebr_steps.csv; data/downtime_events.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-026 | Cleaning validation boundary | surface | workflow_a_b_c | `data/cleaning_validation.csv; data/production_schedule.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-027 | Process analytical technology drift | surface | workflow_batch | `data/pat_models.csv; data/recipes.csv` | PAT vs recipe version mismatch; readiness abstains on PAT alignment. |
| INJ-028 | Qualified Person evidence gap | surface | workflow_a_b_c | `data/release_packets.csv; data/supplier_audits.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-029 | Audit-trail disabled | surface | workflow_a_b_c | `data/audit_trails.csv; data/privileged_sessions.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-030 | Shared laboratory account | surface | workflow_a_b_c | `data/access_logs.csv; data/staff_rosters.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-031 | Validation-state ambiguity | surface | workflow_a_b_c | `data/system_inventory.csv; data/validation_inventory.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-032 | Unapproved spreadsheet | surface | workflow_a_b_c | `data/spreadsheet_inventory.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-033 | CAPA effectiveness failure | surface | workflow_a_b_c | `data/deviations.csv; data/capa_records.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-034 | Change-control bypass | surface | workflow_a_b_c | `data/change_controls.csv; data/vendor_releases.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-035 | Record-retention conflict | surface | workflow_a_b_c | `data/retention_rules.csv; data/legal_holds.csv; data/deletion_requests.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-036 | ALCOA+ provenance break | surface | workflow_a_b_c | `data/certificates_analysis.csv; data/document_lineage.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-037 | ICSR duplicate cluster | surface | workflow_a_b_c | `data/icsr_cases.csv; data/duplicate_candidates.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-038 | Reporting-clock conflict | surface | workflow_a_b_c | `data/icsr_cases.csv; data/safety_receipts.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-039 | MedDRA version mismatch | surface | workflow_a_b_c | `data/adverse_events.csv; data/terminology_versions.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-040 | Expectedness source conflict | surface | workflow_a_b_c | `data/listedness_sources.csv; data/product_labels.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-041 | Pregnancy and paediatric sensitivity | record_conflict | workflow_pv | `data/icsr_cases.csv; data/sensitive_segments.csv` | Do not fabricate ICSR PV-1020; cite join gap and restrict segments. |
| INJ-042 | Social-media authenticity | surface | workflow_a_b_c | `data/social_listening.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-043 | Product-quality and safety link | surface | workflow_a_b_c | `data/product_complaints.csv; data/icsr_cases.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-044 | Signal disproportionality instability | surface | workflow_a_b_c | `data/signal_metrics.csv; data/exposure_estimates.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-045 | IDMP identity conflict | surface | workflow_a_b_c | `data/medicinal_products.csv; data/idmp_mappings.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-046 | Labeling divergence | record_conflict | regulatory_semantics | `data/product_labels.csv; data/market_authorisations.csv` | Cite approved versions as present; do not invent pending/absent leaflets. |
| INJ-047 | Commitment deadline ambiguity | surface | workflow_a_b_c | `data/regulatory_commitments.csv; data/authority_correspondence.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-048 | eCTD sequence gap | surface | workflow_a_b_c | `data/ectd_sequences.csv; data/document_catalog.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-049 | Variation classification dispute | abstain | regulatory_semantics | `data/regulatory_changes.csv` | Variation classification is a human regulatory decision; AEGIS dual-cites only. |
| INJ-050 | Inspection request surge | surface | workflow_a_b_c | `data/inspection_requests.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-051 | Cold-chain lane excursion | surface | workflow_a_b_c | `data/shipments.csv; data/temperature_loggers.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-052 | Serialization aggregation break | surface | workflow_a_b_c | `data/serialisation_events.csv; data/packaging_events.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-053 | Counterfeit suspicion | surface | workflow_supply | `data/returns.csv; data/serialisation_events.csv` | Serial/print/distribution conflict surfaced; recall not initiated. |
| INJ-054 | Critical excipient shortage | surface | workflow_a_b_c | `data/supplier_risks.csv; data/inventory.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-055 | CMO capacity conflict | surface | workflow_supply | `data/cmo_capacity.csv; data/vendor_contracts.csv` | Double-booked CMO window is a constraint, not an allocation. |
| INJ-056 | Allocation ethics | surface | workflow_a_b_c | `data/demand_forecast.csv; data/inventory.csv; data/allocation_constraints.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-057 | Customs documentation mismatch | surface | workflow_a_b_c | `data/shipments.csv; data/trade_documents.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-058 | Recall-scope uncertainty | surface | workflow_a_b_c | `data/recall_candidates.csv; data/material_genealogy.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-059 | Genomic re-identification risk | surface | workflow_a_b_c | `data/genomic_data.csv; data/privacy_risk.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-060 | Cross-border secondary use | surface | workflow_a_b_c | `data/consents.csv; data/data_exports.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-061 | Data-subject request versus GxP record | surface | workflow_a_b_c | `data/deletion_requests.csv; data/retention_rules.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-062 | Patient-support programme leakage | deny | privacy_gates | `data/patient_support_cases.csv` | Purpose limitation: copay-support free text is not a general PV/batch context. |
| INJ-063 | Research-commercial boundary | surface | workflow_a_b_c | `data/data_licenses.csv; data/commercial_use_requests.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-064 | Regional residency failure | surface | workflow_a_b_c | `data/data_residency.csv; data/backup_inventory.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-065 | Prompt injection in SOP | deny | policy_guard | `data/knowledge_catalog.csv; knowledge/MALICIOUS_SUPPLIER_DEVIATION.md` | Untrusted SOP is data, not executable policy. |
| INJ-066 | Tool-manifest poisoning | deny | policy_guard | `data/tool_catalog.csv; data/tool_manifest_poisoned.json` | Hard-gate deny path. |
| INJ-067 | Entitlement revocation lag | deny | policy_guard | `data/users_entitlements.csv; data/access_cache.csv` | Hard-gate deny path. |
| INJ-068 | Safety-data exfiltration | surface | workflow_a_b_c | `data/security_events.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-069 | Ransomware and OT segmentation | surface | workflow_a_b_c | `data/downtime_events.csv; data/network_zones.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-070 | Model supply-chain compromise | deny | policy_guard | `data/model_registry.csv; data/model_artifacts.csv` | Hard-gate deny path. |
| INJ-071 | Automation bias in batch review | surface | workflow_a_b_c | `data/candidate_outputs.csv; data/reviewer_feedback.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-072 | Language inequity | surface | workflow_a_b_c | `data/model_performance.csv; data/icsr_cases.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-073 | Accessibility failure | surface | workflow_a_b_c | `data/usability_findings.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-074 | Role conflict | surface | workflow_a_b_c | `data/stakeholders.csv; data/decision_rights.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-075 | Model price shock | surface | workflow_a_b_c | `data/model_costs.csv; data/vendor_contracts.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-076 | Denial-of-wallet pattern | surface | workflow_a_b_c | `data/model_usage.csv; data/security_events.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-077 | Hidden human-review cost | surface | workflow_a_b_c | `data/cost_model.csv; data/staff_rates.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-078 | Vendor concentration | surface | workflow_a_b_c | `data/vendor_dependencies.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-079 | Regional platform outage | surface | workflow_a_b_c | `data/downtime_events.csv; data/model_endpoints.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-080 | Checkpoint corruption | surface | workflow_a_b_c | `data/agent_runs.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-081 | Model substitution regression | surface | workflow_a_b_c | `data/model_performance.csv; data/model_endpoints.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-082 | AI-disabled continuity | surface | workflow_a_b_c | `data/continuity_requirements.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-083 | Vendor exit deadline | surface | workflow_a_b_c | `data/vendor_contracts.csv; data/vendor_exit_assets.csv` | Catalog evidence resolved; advisory surface only. |
| INJ-084 | Retirement and evidence preservation | surface | workflow_a_b_c | `data/retention_rules.csv; data/retirement_assets.csv` | Catalog evidence resolved; advisory surface only. |
