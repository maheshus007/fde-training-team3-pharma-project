# Acceptance criteria test plan

Every in-scope acceptance criterion maps to at least one test task. Tests are written **before** the implementation they verify — that ordering is a hard rule, not a preference.

| AC | Test task | Test type | Location | Status |
|---|---|---|---|---|
| AC-FR001-01 | TASK-009 | Contract | `tests/contract/test_batch_contract.py` | Not started |
| AC-FR001-02 | TASK-004 | Contract | `tests/contract/test_invariants.py` | Not started |
| AC-FR001-03 | TASK-004 | Security / deny-list | `tests/security/test_prohibited_language.py` | Not started |
| AC-FR001-04 | TASK-009 | Integration | `tests/integration/test_batch_contradictions.py` | Not started |
| AC-FR001-05 | TASK-008 | Unit | `tests/unit/test_unit_mapping.py` | Not started |
| AC-FR001-06 | TASK-007 | Unit + contract | `tests/unit/test_evidence_item.py` | Not started |
| AC-FR001-07 | TASK-009 | Integration | `tests/integration/test_readiness_state.py` | Not started |
| AC-FR001-08 | TASK-009 | Integration | `tests/integration/test_readiness_state.py` | Not started |
| AC-FR001-09 | TASK-003 | Determinism | `tests/unit/test_canonical_json.py`, `tests/regression/test_byte_identical.py` | Not started |
| AC-FR001-10 | TASK-006 | Resilience | `tests/resilience/test_ai_disabled.py` | Not started |
| AC-FR001-11 | TASK-002 | Security | `tests/security/test_integrity_failure.py` | Not started |
| AC-FR001-12 | TASK-010 | Security | `tests/security/test_prompt_injection.py` | Not started |
| AC-FR002-01 | TASK-012 | Contract | `tests/contract/test_pv_contract.py` | Not started |
| AC-FR002-02 | TASK-004 | Security / deny-list | `tests/security/test_prohibited_language.py` | Not started |
| AC-FR002-03 | TASK-011 | Unit | `tests/unit/test_duplicate_candidates.py` | Not started |
| AC-FR002-04 | TASK-011 | Unit / boundary | `tests/unit/test_duplicate_candidates.py` | Not started |
| AC-FR002-05 | TASK-012 | Integration | `tests/integration/test_pv_clocks.py` | Not started |
| AC-FR002-06 | TASK-008 | Unit | `tests/unit/test_terminology_versions.py` | Not started |
| AC-FR002-07 | TASK-012 | Integration | `tests/integration/test_listedness.py` | Not started |
| AC-FR002-08 | TASK-013 | Security | `tests/security/test_purpose_limitation.py` | Not started |
| AC-FR002-09 | TASK-013 | Security | `tests/security/test_dsr_vs_hold.py` | Not started |
| AC-FR002-10 | TASK-012 | Subgroup | `tests/subgroup/test_language_scope.py` | Not started |
| AC-FR002-11 | TASK-013 | Security | `tests/security/test_sensitive_segments.py` | Not started |
| AC-FR002-12 | TASK-003, TASK-006 | Determinism / resilience | as above | Not started |
| AC-FR002-13 | TASK-013 | Security / privacy | `tests/security/test_pseudonymisation.py` | Not started |
| AC-FR003-01 | TASK-014 | Contract | `tests/contract/test_supply_contract.py` | Not started |
| AC-FR003-02 | TASK-014 | Contract | `tests/contract/test_supply_contract.py` | Not started |
| AC-FR003-03 | TASK-004 | Security / deny-list | `tests/security/test_prohibited_language.py` | Not started |
| AC-FR003-04 | TASK-014 | Integration | `tests/integration/test_supply_options.py` | Not started |
| AC-FR003-05 | TASK-014 | Integration | `tests/integration/test_quality_holds.py` | Not started |
| AC-FR003-06 | TASK-014 | Integration | `tests/integration/test_cold_chain_dispute.py` | Not started |
| AC-FR003-07 | TASK-015 | Graph | `tests/integration/test_bounded_traversal.py` | Not started |
| AC-FR003-08 | TASK-014 | Security | `tests/security/test_no_recall_initiation.py` | Not started |
| AC-FR003-09 | TASK-016 | Resilience | `tests/resilience/test_idempotent_replay.py` | Not started |
| AC-FR003-10 | TASK-016 | Security | `tests/resilience/test_checkpoint_freshness.py` | Not started |
| AC-FR003-11 | TASK-003, TASK-006 | Determinism / resilience | as above | Not started |
| AC-FR004-01 | TASK-007 | Contract | `tests/contract/test_evidence_provenance.py` | Not started |
| AC-FR004-02 | TASK-002 | Security | `tests/security/test_integrity_failure.py` | Not started |
| AC-FR004-03 | TASK-007 | Unit | `tests/unit/test_authority_resolution.py` | Not started |
| AC-FR004-04 | TASK-007 | Unit | `tests/unit/test_supersession.py` | Not started |
| AC-FR004-05 | TASK-007 | Unit | `tests/unit/test_authority_resolution.py` | Not started |
| AC-FR004-06 | TASK-010 | Security | `tests/security/test_prompt_injection.py` | Not started |
| AC-FR004-07 | TASK-007 | Unit | `tests/unit/test_missing_reference.py` | Not started |
| AC-FR004-08 | TASK-008 | Unit | `tests/unit/test_temporal_precision.py` | Not started |
| AC-FR004-09 | TASK-007 | Integration | `tests/integration/test_back_entry_flag.py` | Not started |
| AC-FR004-10 | TASK-001 | Static analysis | `quality/static-analysis/test_evidence_construction.py` | Not started |
| AC-FR005-01 | TASK-013 | Contract | `tests/contract/test_advisory_contract.py` | Not started |
| AC-FR005-02 | TASK-005 | Security | `tests/security/test_execution_time_authz.py` | Not started |
| AC-FR005-03 | TASK-005 | Integration | `tests/integration/test_revocation_lag.py` | Not started |
| AC-FR005-04 | TASK-005 | Contract | `tests/contract/test_denial_pack.py` | Not started |
| AC-FR005-05 | TASK-005 | Security | `tests/security/test_execution_time_authz.py` | Not started |
| AC-FR005-06 | TASK-013 | Security | `tests/security/test_dsr_vs_hold.py` | Not started |
| AC-FR005-07 | TASK-013 | Security | `tests/security/test_consent_per_purpose.py` | Not started |
| AC-FR005-08 | TASK-013 | Integration | `tests/integration/test_retention_rules.py` | Not started |
| AC-FR005-09 | TASK-013 | Security | `tests/security/test_purpose_limitation.py` | Not started |
| AC-FR005-10 | TASK-013 | Security | `tests/security/test_residency.py` | Not started |
| AC-FR005-11 | TASK-013 | Security | `tests/security/test_sensitive_segments.py` | Not started |
| AC-FR005-12 | TASK-013 | Security | `tests/security/test_cache_boundaries.py` | Not started |
| AC-FR005-13 | TASK-005 | Integration | `tests/integration/test_account_attribution.py` | Not started |
| AC-FR005-14 | TASK-023 | Security | `tests/security/test_tool_manifest.py` | Not started |
| AC-FR005-15 | TASK-013 | Security | `tests/security/test_exfiltration.py` | Not started |
| AC-FR005-16 | TASK-003, TASK-006 | Determinism / resilience | as above | Not started |
| AC-FR006-01 | TASK-020 | Contract | `tests/contract/test_advisory_contract.py` | Not started |
| AC-FR006-02 | TASK-016 | Security | `tests/resilience/test_checkpoint_freshness.py` | Not started |
| AC-FR006-03 | TASK-016 | Resilience | `tests/resilience/test_idempotent_replay.py` | Not started |
| AC-FR006-04 | TASK-020 | Security | `tests/security/test_draft_has_no_power.py` | Not started |
| AC-FR006-05 | TASK-016 | Security | `tests/resilience/test_checkpoint_freshness.py` | Not started |
| AC-FR006-06 | TASK-020 | Security | `tests/security/test_checkpoint_contents.py` | Not started |
| AC-FR006-07 | TASK-020 | Resilience | `tests/resilience/test_budget_stop.py` | Not started |
| AC-FR006-08 | TASK-020 | Security | `tests/security/test_excessive_agency.py` | Not started |
| AC-FR006-09 | TASK-020 | Resilience | `tests/resilience/test_retry_bound.py` | Not started |
| AC-FR006-10 | TASK-021 | Orchestration | `tests/orchestration/test_parity.py` | Not started |
| AC-FR006-11 | TASK-003, TASK-006 | Determinism / resilience | as above | Not started |
| AC-FR007-01 | TASK-026 | Contract | `tests/contract/test_advisory_contract.py` | Not started |
| AC-FR007-02 | TASK-026 | Unit | `tests/unit/test_inference_cost.py` | Not started |
| AC-FR007-03 | TASK-026 | Unit | `tests/unit/test_cost_per_successful_task.py` | Not started |
| AC-FR007-04 | TASK-026 | Unit | `tests/unit/test_missing_cost_is_gap.py` | Not started |
| AC-FR007-05 | TASK-026 | Integration | `tests/integration/test_cost_abstention.py` | Not started |
| AC-FR007-06 | TASK-026 | Unit | `tests/unit/test_price_change.py` | Not started |
| AC-FR007-07 | TASK-026 | Security | `tests/security/test_no_estimated_cost.py` | Not started |
| AC-FR007-08 | TASK-020 | Resilience | `tests/resilience/test_budget_stop.py` | Not started |
| AC-FR007-09 | TASK-026 | Security | `tests/security/test_wallet_ceiling.py` | Not started |
| AC-FR007-10 | TASK-026 | Performance | `tests/performance/test_avoided_inference.py` | Not started |
| AC-FR007-10a | TASK-026 | Integration | `tests/integration/test_vendor_concentration.py` | Not started |
| AC-FR007-11 | TASK-003 | Determinism | `tests/unit/test_decimal_arithmetic.py` | Not started |
| AC-FR007-12 | TASK-003, TASK-006 | Determinism / resilience | as above | Not started |
| AC-FR008-01 | TASK-025 | Security | `tests/security/test_no_action_controls.py` | Not started |
| AC-FR008-02 | TASK-025 | E2E | `tests/e2e/test_forced_evidence_view.py` | Not started |
| AC-FR008-03 | TASK-025 | E2E | `tests/e2e/test_acknowledgement.py` | Not started |
| AC-FR008-04 | TASK-025 | E2E | `tests/e2e/test_gap_prominence.py` | Not started |
| AC-FR008-05 | TASK-024 | Security | `tests/security/test_payload_entitlement.py` | Not started |
| AC-FR008-06 | TASK-025 | E2E | `tests/e2e/test_evidence_links.py` | Not started |
| AC-FR008-07 | TASK-025 | Accessibility | `tests/e2e/test_accessibility.py` | Not started |
| AC-FR008-08 | TASK-025 | Accessibility | `tests/e2e/test_keyboard.py` | Not started |
| AC-FR008-09 | TASK-025 | i18n | `tests/e2e/test_rtl_and_scripts.py` | Not started |
| AC-FR008-10 | TASK-025 | Resilience | `tests/e2e/test_degraded_state.py` | Not started |
| AC-FR008-11 | TASK-025 | E2E | `tests/e2e/test_contradiction_render.py` | Not started |
| AC-FR008-12 | TASK-024 | Security | `tests/security/test_segregation_of_duties.py` | Not started |
| AC-FR009-01 | TASK-022 | Contract | `tests/contract/test_advisory_contract.py` | Not started |
| AC-FR009-02 | TASK-022 | Resilience | `tests/resilience/test_outage_tolerance.py` | Not started |
| AC-FR009-03 | TASK-022 | Resilience | `tests/resilience/test_outage_tolerance.py` | Not started |
| AC-FR009-04 | TASK-022 | Unit | `tests/unit/test_empty_is_not_zero.py` | Not started |
| AC-FR009-05 | TASK-022 | Security | `tests/security/test_model_substitution.py` | Not started |
| AC-FR009-06 | TASK-022 | Security | `tests/security/test_residency.py` | Not started |
| AC-FR009-07 | TASK-022 | Security | `tests/security/test_degraded_no_wider_authority.py` | Not started |
| AC-FR009-08 | TASK-006 | Resilience | `tests/resilience/test_ai_disabled.py` | Not started |
| AC-FR009-09 | TASK-022 | Resilience | `tests/resilience/test_kill_switch.py` | Not started |
| AC-FR009-10 | TASK-022 | Artefact | `tests/integration/test_runbooks_exist.py` | Not started |
| AC-FR009-11 | TASK-022 | Integration | `tests/integration/test_outage_reconciliation.py` | Not started |
| AC-FR009-12 | TASK-022 | Resilience | `tests/resilience/test_vendor_removal.py` | Not started |
| AC-FR009-13 | TASK-003 | Determinism | `tests/regression/test_byte_identical.py` | Not started |
| AC-FR010-01 | TASK-018 | Contract | `tests/contract/test_advisory_contract.py` | Not started |
| AC-FR010-02 | TASK-018 | Integration | `tests/integration/test_protocol_applicability.py` | Not started |
| AC-FR010-03 | TASK-018 | Integration | `tests/integration/test_protocol_applicability.py` | Not started |
| AC-FR010-04 | TASK-018 | Integration | `tests/integration/test_pending_amendment.py` | Not started |
| AC-FR010-05 | TASK-018 | Unit | `tests/unit/test_reference_ranges.py` | Not started |
| AC-FR010-06 | TASK-004 | Security / deny-list | `tests/security/test_prohibited_language.py` | Not started |
| AC-FR010-07 | TASK-018 | Unit | `tests/unit/test_reference_ranges.py` | Not started |
| AC-FR010-08 | TASK-013 | Security | `tests/security/test_consent_per_purpose.py` | Not started |
| AC-FR010-09 | TASK-008 | Unit | `tests/unit/test_temporal_precision.py` | Not started |
| AC-FR010-10 | TASK-010 | Security | `tests/security/test_prompt_injection.py` | Not started |
| AC-FR010-11 | TASK-003, TASK-006 | Determinism / resilience | as above | Not started |
| AC-FR011-01 | TASK-017 | Contract | `tests/contract/test_advisory_contract.py` | Not started |
| AC-FR011-02 | TASK-017 | Unit | `tests/unit/test_unit_mapping.py` | Not started |
| AC-FR011-03 | TASK-017 | Security | `tests/security/test_no_unapproved_conversion.py` | Not started |
| AC-FR011-04 | TASK-017 | Integration | `tests/integration/test_lims_reconciliation.py` | Not started |
| AC-FR011-05 | TASK-017 | Integration | `tests/integration/test_lims_reconciliation.py` | Not started |
| AC-FR011-06 | TASK-017 | Unit | `tests/unit/test_ucum_validation.py` | Not started |
| AC-FR011-07 | TASK-017 | Unit | `tests/unit/test_status_vocabularies.py` | Not started |
| AC-FR011-08 | TASK-017 | Unit | `tests/unit/test_ucum_validation.py` | Not started |
| AC-FR011-09 | TASK-017 | Unit | `tests/unit/test_contract_version_required.py` | Not started |
| AC-FR011-10 | TASK-008 | Unit | `tests/unit/test_temporal_precision.py` | Not started |
| AC-FR011-11 | TASK-003, TASK-006 | Determinism / resilience | as above | Not started |
| AC-FR012-01 | TASK-019 | Contract | `tests/contract/test_advisory_contract.py` | Not started |
| AC-FR012-02 | TASK-019 | Unit | `tests/unit/test_identity_conflict.py` | Not started |
| AC-FR012-03 | TASK-019 | Integration | `tests/integration/test_label_divergence.py` | Not started |
| AC-FR012-04 | TASK-019 | Unit | `tests/unit/test_commitment_deadlines.py` | Not started |
| AC-FR012-05 | TASK-019 | Unit | `tests/unit/test_sequence_gap.py` | Not started |
| AC-FR012-06 | TASK-004 | Security / deny-list | `tests/security/test_prohibited_language.py` | Not started |
| AC-FR012-07 | TASK-019 | Regression | `tests/regression/test_urgency_invariance.py` | Not started |
| AC-FR012-08 | TASK-004 | Security / deny-list | `tests/security/test_prohibited_language.py` | Not started |
| AC-FR012-09 | TASK-019 | Contract | `tests/contract/test_evidence_provenance.py` | Not started |
| AC-FR012-10 | TASK-003, TASK-006 | Determinism / resilience | as above | Not started |

| AC-FR013-01 | TASK-030 | Orchestration | `tests/orchestration/test_advisory_parity.py` | Not started |
| AC-FR013-02 | TASK-030 | Resilience | `tests/resilience/test_kill_switch.py` | Not started |
| AC-FR013-03 | TASK-031 | Security | `tests/security/test_guard_numeric_closure.py` | Not started |
| AC-FR013-04 | TASK-031 | Security | `tests/security/test_guard_citation_closure.py` | Not started |
| AC-FR013-05 | TASK-031 | Security | `tests/security/test_guard_denylist.py` | Not started |
| AC-FR013-06 | TASK-031 | Security | `tests/security/test_guard_abstention.py` | Not started |
| AC-FR013-07 | TASK-031 | Security | `tests/security/test_prompt_injection.py` | Not started |
| AC-FR013-08 | TASK-030 | Security | `tests/security/test_prompt_minimisation.py` | Not started |
| AC-FR013-09 | TASK-030 | Security | `tests/security/test_residency.py` | Not started |
| AC-FR013-10 | TASK-030 | Security | `tests/security/test_azure_auth.py` | Not started |
| AC-FR013-11 | TASK-030 | Integration | `tests/integration/test_model_metadata.py` | Not started |
| AC-FR013-12 | TASK-030 | Static analysis | `quality/static-analysis/test_model_pinning.py` | Not started |
| AC-FR013-13 | TASK-032 | Regression | `tests/regression/test_advice_replay.py` | Not started |
| AC-FR013-14 | TASK-030 | Resilience | `tests/resilience/test_azure_degradation.py` | Not started |
| AC-FR013-15 | TASK-026 | Resilience | `tests/resilience/test_budget_stop.py` | Not started |
| AC-FR013-16 | TASK-025 | E2E | `tests/e2e/test_annotation_labelling.py` | Not started |
| AC-FR013-17 | TASK-030 | Integration | `tests/integration/test_content_filter_record.py` | Not started |
| AC-FR013-18 | TASK-032 | Eval | `evals/graders/deterministic/groundedness.py` | Not started |
| AC-FR013-19 | TASK-030 | Security | `tests/security/test_unconfigured_fails_closed.py` | Not started |
| AC-FR014-01 | TASK-033 | Integration | `tests/integration/test_evidence_chain.py` | Not started |
| AC-FR014-02 | TASK-033 | Security | `tests/security/test_chain_tamper.py` | Not started |
| AC-FR014-03 | TASK-033 | Security | `tests/security/test_chain_tamper.py` | Not started |
| AC-FR014-04 | TASK-033 | Resilience | `tests/resilience/test_evidence_fail_closed.py` | Not started |
| AC-FR014-05 | TASK-030 | Integration | `tests/integration/test_llm_record.py` | Not started |
| AC-FR014-06 | TASK-033 | Security | `tests/security/test_store_scan.py` | Not started |
| AC-FR014-07 | TASK-034 | Integration | `tests/integration/test_retention_expiry.py` | Not started |
| AC-FR014-08 | TASK-034 | Security | `tests/security/test_hold_blocks_expiry.py` | Not started |
| AC-FR014-09 | TASK-034 | Security | `tests/security/test_cache_boundaries.py` | Not started |
| AC-FR014-10 | TASK-034 | Integration | `tests/integration/test_retention_expiry.py` | Not started |
| AC-FR014-11 | TASK-033 | Integration | `tests/integration/test_evidence_retrieval.py` | Not started |
| AC-FR014-12 | TASK-033 | Resilience | `tests/resilience/test_vendor_removal.py` | Not started |
| AC-FR014-13 | TASK-033 | Resilience | `tests/resilience/test_index_rebuild.py` | Not started |
| AC-FR014-14 | TASK-033 | Determinism | `tests/regression/test_record_layout.py` | Not started |
| AC-FR014-15 | TASK-035 | Security | `tests/security/test_blob_immutability.py` | Not started |

## Additional suites not derived from feature ACs

| Purpose | Task | Location |
|---|---|---|
| Advisory contract for the 7 non-workflow fixtures (AMB-01) | TASK-004 | `tests/contract/test_advisory_contract.py` |
| Copy-set derivation and hash verification | TASK-002 | `tests/unit/test_copyset.py` |
| Stdlib-only import gate, now including `openai` and `azure` | TASK-001 | `quality/static-analysis/test_no_third_party.py` |
| Interpreter range check | TASK-001 | `tests/unit/test_setup_guard.py` |

## Coverage

177 acceptance criteria, 177 mapped, zero unmapped and zero deferred at authoring time. Thirty-five tasks carry them.

## Rules

No AC is silently skipped. A test that cannot yet pass is committed as failing or explicitly marked deferred with a reason in this table — never deleted, never `skip` without a recorded rationale. When an AC is verified, the status changes here and the result is written to `evidence/tests/`.

Deferral count is a release-gate input: a deferred AC on a hard gate blocks release regardless of every other result.
