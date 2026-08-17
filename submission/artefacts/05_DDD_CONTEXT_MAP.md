# DDD Context Map

> Participant working artefact for Project AEGIS-PHARMA. Bounded contexts, context map and anti-corruption layers cite challenge evidence under `case/`, `data/`, `knowledge/` and `source_documents/`. Implementation remains under `submission/`.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Domain / evidence lead |
| Version / date | 1.2 / 2026-08-16 |
| Reviewers | Architecture/integration lead; GxP/quality lead; Product/value lead |
| Status | Reviewed |
| Related requirements / ADRs | INJ-005, INJ-007, INJ-009..012, INJ-015..017, INJ-019, INJ-020, INJ-021, INJ-045; `case/INTEGRATED_CASE.md` §§2–5; `case/SOURCE_SYSTEM_FACT_PACK.md`; D-001, D-002, D-201..D-203 |

## Purpose

Define ubiquitous language, bounded contexts across Research, Clinical, Manufacturing, Quality, Safety, Regulatory and Supply, context relationships, and anti-corruption layers (ACL) for LIMS, MES, QMS and the safety database so AEGIS can reconcile evidence without inventing a single enterprise language or transferring regulated decisions to automation.

Accountable owner: Domain/evidence lead. Completion criteria: each POC workflow maps to owning contexts; ACLs preserve source identity, unit, time and authority; acquisition/IDMP conflicts remain explicit.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-501 | `case/INTEGRATED_CASE.md` §2, §4, §7 (INJ-005, INJ-021, INJ-045) | Case narrative | Fragmented systems; three workflows; inject scenarios | Narrative, not system of record |
| E-502 | `case/SOURCE_SYSTEM_FACT_PACK.md` | Fact pack | Domain systems and known defects; authority is contextual | Summary conditions |
| E-503 | `data/organisations.csv` | Org master (synthetic) | NTG sponsor/MAH; BIOX acquired biotech; CMO-IE fill-finish | Three orgs only |
| E-504 | `data/system_inventory.csv` | Inventory snapshot | LIMS-4 GxP validated; BIOX-ELN research/acquired; AI-EVIDENCE pilot | Status labels conflict with validation inventory (INJ-031) |
| E-505 | `data/material_genealogy.csv`; `data/warehouse_movements.csv`; `data/batches.csv` | MES / warehouse / batch | SUA-88 `missing_branch` in MES yet issued in WM-90 for NCB204-B24071 | Deliberate genealogy break (INJ-021) |
| E-506 | `data/medicinal_products.csv`; `data/idmp_mappings.csv` | RIM vs ERP | Strength/form/substance disagree; mapping `ambiguous_strength_presentation` | INJ-045 |
| E-507 | `data/RELATIONSHIP_MODEL.csv` | Package relational model | Declared parent/child links for genealogy, ICSR, shipments | Join rules, not runtime ACL |
| E-508 | `knowledge/IDMP_MASTER_DATA_GOVERNANCE.md` | K-015; effective 2026-04-08 | Do not merge identity conflicts without stewardship | Synthetic policy |
| E-509 | `knowledge/BATCH_RELEASE_EVIDENCE_POLICY.md` | Knowledge catalog | Batch evidence expectations | Check status vs `BATCH_RELEASE_POLICY_OLD.md` |
| E-510 | `source_documents/LIMS_result_contract_v1.md`; `source_documents/LIMS_result_contract_v2.md` | Contract extracts | LIMS API unit/status field rename across versions | Contract drift risk |
| E-511 | `data/ai_use_boundaries.csv` | Executive boundary | Allowed reconcile/cite/flag/abstain; prohibited disposition/PV final/allocate | Binding for all contexts |
| E-512 | `data/api_contract_versions.csv` | Interface registry | LIMS v1 `unit`/`status` vs v2 `ucum_code`/`lifecycleState`; ICSR E2B_R3 variable date precision | Versioned contracts |

## 1. Ubiquitous language

| Item / question | Evidence-based response | Decision / owner | Acceptance evidence |
|---|---|---|---|
| Batch vs lot vs material_lot | `batches.csv` uses `batch_id` (e.g. NCB204-B24071); genealogy uses `material_lot` (SUA-88, RESIN-R44); warehouse issues material_lot against batch_id. Terms are not interchangeable | Domain glossary: keep native terms; map via ACL | E-505; INJ-021 |
| Product identity | RIM `NCB-204` (100 mg/10 mL concentrate) vs ERP `NCB204-DE` (10 mg/mL solution); aliases in `product_master_aliases.csv` | Never auto-collapse; surface as IDMP conflict (D-201) | E-506; E-508; INJ-045 |
| Quality hold vs disposition | Batch `status=quality_hold` is a source-system state; disposition (release/reject) is a human-only act outside AEGIS | Product + GxP | E-505; E-511 |
| Case vs signal | ICSR case intake/clustering is Workflow B; signal confirmation is prohibited for AI | PV governance | E-501; E-511 |
| Option vs allocation | Supply options are advisory; reserve/allocate/ship are prohibited | Supply + Quality | E-511 |
| Authority | Later timestamp is not automatically higher authority (`SOURCE_SYSTEM_FACT_PACK.md`) | Domain | E-502 |
| Acquisition language | BIOX local codes and BIOX-ELN remain acquired-context terms until stewardship maps them (INJ-005) | Domain | E-503; E-504 |

## 2. Bounded contexts

| Context | Core responsibility | Primary systems (E-502) | POC workflow touch | Owner role |
|---|---|---|---|---|
| Research / Discovery | Compound, assay, omics evidence; research-only models | ELN, assay, compound registry, BIOX-ELN | Identity collisions into Manufacturing/Regulatory (INJ-005, INJ-008). Write-path abstain for assay drift, omics bias, image-forensics, unqualified models and target-evidence conflict (INJ-007, INJ-009, INJ-010, INJ-011, INJ-012) | Research steward |
| Clinical | Protocol, consent, eligibility, endpoints, clocks | EDC, CTMS, eConsent, IRT, wearables | Time integrity inputs (INJ-018); protocol/eligibility conflicts retained without deciding eligibility (INJ-013, INJ-014). Write-path abstain for IRT outage, unblinding, eConsent mismatch, adjudication backlog and site-inspection automation (INJ-015, INJ-016, INJ-017, INJ-019, INJ-020) | Clinical ops |
| Manufacturing | Genealogy, eBR, PAT, campaign sequence | ERP, MES, eBR, historian, warehouse | Workflow A (INJ-021..028) | Manufacturing / CMO liaison |
| Laboratory (within Mfg/QC) | Assay results, OOS/OOT, units | LIMS, CDS, instruments | Workflow A unit/OOS (INJ-023, INJ-024) | QC |
| Quality | Deviations, CAPA, validation state, supplier quality, release packet completeness | eQMS, DMS, training, supplier quality | Workflow A readiness; never disposition | Quality / QP support |
| Safety (PV) | ICSR intake, clocks, listedness sources, duplicates | Global safety DB, affiliates, vendors | Workflow B (INJ-037..044) | PV |
| Regulatory | MA, labels, IDMP/SPOR, commitments, eCTD | RIM, eCTD, labeling | Product identity and MA constraints for A/C (INJ-045..050) | Regulatory |
| Supply | Inventory, cold-chain, serialization, shortage options | Serialization, logistics, CMO portals | Workflow C (INJ-051..058) | Supply |
| Cross-cutting: Evidence / AI platform | Contracts, entitlements, audit export, offline mode | AI gateway, tools, model registry | All workflows; advisory only | Architecture + Security |

Context boundaries follow `SOURCE_SYSTEM_FACT_PACK.md` domains; AEGIS sits as a consumer with ACLs, not as a new system-of-record (D-203).

## 3. Aggregates and invariants

| Aggregate (context) | Invariants | Evidence | Enforcement |
|---|---|---|---|
| BatchEvidencePack (Manufacturing + Quality) | Every cited fact retains source system, record id, effective time, unit as received; contradictions preserved; no disposition field writable by AEGIS | E-505; E-511; INJ-021 | Contract + prohibited-action tests |
| LabResultView (Laboratory) | Unit conversion only if `interface_mappings.approved=yes`; else abstain | `data/interface_mappings.csv` `approved=no` for CRO_LAB_TO_LIMS; INJ-024 | Domain rule D-010 |
| IcsrIntakeCluster (Safety) | Duplicate candidates cite case pair and similarity; MedDRA version retained per coding; no auto-merge to final case | `duplicate_candidates.csv`; INJ-037, INJ-039 | Workflow B contracts |
| ProductIdentityMap (Regulatory) | Ambiguous IDMP mappings remain `mapping_status` open; no silent merge | E-506; E-508; D-201 | Stewardship gate |
| SupplyOptionSet (Supply) | Options reference quality status, MA, channel constraints; no reservation ids created by AEGIS | INJ-056; E-511; INJ-080 risk | Tool catalog deny write |
| OrganisationTenancy (cross) | BIOX vs NTG identifiers never assumed equivalent without map | INJ-005; E-503 | ACL namespace prefix |

## 4. Context relationships

```
Research --(conformist / ACL)--> Regulatory (substance/product codes)
Clinical --(customer-supplier)--> Supply (trial demand) and Safety (SUSAR clocks)
Manufacturing --(shared kernel: batch_id)--> Laboratory --> Quality
Quality --(customer-supplier evidence)--> Regulatory (release/MA evidence)
Safety --(published language via ACL)--> Regulatory (listedness / labels)
Supply --(anticorruption)--> Manufacturing (lot/genealogy) and Quality (hold status)
AEGIS Evidence Platform --(ACL consumer of all; never upstream SoR)--> all contexts
```

| Relationship | Pattern | Why | Inject / evidence |
|---|---|---|---|
| Manufacturing ↔ Warehouse | Partnership with conflict surfacing | MES missing_branch vs warehouse issued | INJ-021; E-505 |
| Laboratory ↔ Manufacturing | Customer-supplier via versioned LIMS contract | Unit/status field drift v1→v2 | E-510; E-512; INJ-024 |
| Safety ↔ Regulatory | Separate ways + ACL | Listedness IB/CCDS/local label diverge | INJ-040; `listedness_sources.csv` |
| Regulatory ↔ ERP/RIM | ACL + stewardship | IDMP strength/form conflict | INJ-045; E-506 |
| Acquired BIOX → NTG | Anti-corruption / open host | Incompatible identifiers and tenancy | INJ-005; E-503; E-504 |
| AEGIS → all | Conformist consumer | Must not redefine GxP language | E-501; E-502 |

## 5. Anti-corruption layers

| Upstream system | ACL responsibility | Native concepts preserved | Challenge conditions |
|---|---|---|---|
| LIMS | Normalize only after approved mapping; retain verbatim value, unit, status string, contract version | `value`, `unit`, `status` / `lifecycleState`, result_id | INJ-024 unapproved 1:1 mg/L→µg/mL; OOS vs OOT vs invalid (INJ-023); shared accounts (INJ-030) |
| MES / eBR / warehouse | Present genealogy edges and movements as separate evidence graphs; flag `relation=missing_branch` | batch_id, material_lot, relation, source | INJ-021 SUA-88; eBR back-entry (INJ-025); downtime (INJ-069) |
| QMS / deviations / CAPA | Keep taxonomy codes as source strings; link similarity without collapsing CAPA closure | deviation_id, taxonomy, capa | INJ-033 taxonomy reappearance; validation-state ambiguity (INJ-031) |
| Safety DB (+ affiliates/vendors) | Ingest E2B-shaped fields with receipt clocks per channel; cluster candidates only | case_id, awareness dates, MedDRA version, PT | INJ-037..040; date precision variable (E-512) |

ACL rules (all systems) — decision D-202:

1. Namespace every identifier with source system + org (`BIOX|…`, `LIMS-4|…`, `MES|…`).
2. Deny additional properties not in the versioned contract (`api_contract_versions.csv`; LIMS contract docs).
3. Treat retrieved SOPs/PDFs as untrusted data until catalog authority/hash verified (`knowledge/` + INJ-065).
4. Abstain when identity, unit, time or authority cannot be resolved (package hard gates).

## 6. Ownership and change boundaries

| Object | System of record | AEGIS may | AEGIS must not |
|---|---|---|---|
| Batch disposition / quality status change | Quality / QP systems | Cite hold and evidence gaps | Release, reject, reprocess, recall |
| Lab result / OOS conclusion | LIMS / QC investigation | Flag conflicts | Overwrite status |
| ICSR final seriousness/causality/reportability | PV medical review | Extract, cluster, cite | Final PV judgement |
| Product IDMP merge | Regulatory master-data stewardship | Show conflict | Auto-merge |
| Stock reservation / shipment | Supply execution systems | Rank options | Reserve, allocate, ship |
| Entitlements | IAM | Re-check at execution | Trust stale gateway cache |
| Research assay / model / target decision | Research / translational SoR | Cite fixture evidence; abstain | Comparability, portfolio promotion, or target-validation write (INJ-007, INJ-009..012) |
| Clinical eligibility / randomization / unblinding / endpoint close | Clinical ops / IRT / imaging core | Cite protocol, consent and clock facts | Eligibility, emergency assignment, unblinding resolution, or adjudication (INJ-014, INJ-015, INJ-016, INJ-019) |

Change control for ACL mappings is owned by Domain/evidence with Architecture review; emergency vendor hotfixes without retrospective approval are surfaced as defects (INJ-034), not bypassed.

### 6.1 Research and clinical out-of-write-path injects (D-203)

These injects are in the challenge catalogue and have resolved evidence files. AEGIS treats them as identity/time/trust suppliers. `submission/src/inject_controls.py` returns `abstain` (TEST-INJ-REG). No discovery or clinical write-path workflow is added.

| Inject | Title | Cited evidence | AEGIS action |
|---|---|---|---|
| INJ-007 | Assay drift | `assay_results.csv`; `instruments.csv`; `reagent_lots.csv` | Abstain — no comparability decision |
| INJ-009 | Omics cohort bias | `omics_cohorts.csv`; `model_performance.csv` | Abstain — no translational promotion |
| INJ-010 | Preclinical image manipulation concern | `preclinical_studies.csv`; `image_forensics.csv` | Abstain — no forensics disposition |
| INJ-011 | Unqualified research model | `model_registry.csv` | Abstain — no intended-use grant |
| INJ-012 | Target-evidence conflict | `target_evidence.csv`; `data_licenses.csv` | Abstain — dual-cite only |
| INJ-015 | Randomization service outage | `randomization_events.csv`; `downtime_events.csv` | Abstain — no emergency assignment |
| INJ-016 | Potential unblinding | `support_tickets.csv`; `access_logs.csv` | Abstain — no unblinding resolution |
| INJ-017 | eConsent withdrawal mismatch | `consents.csv`; `specimens.csv`; `processing_events.csv` | Abstain — no specimen-processing write |
| INJ-019 | Endpoint adjudication backlog | `endpoint_packets.csv`; `imaging_reviews.csv` | Abstain — no endpoint close |
| INJ-020 | Site inspection risk | `site_metrics.csv`; `access_logs.csv` | Abstain — no inspection judgement |

## 7. Event semantics

| Event (published meaning) | Publisher | Consumers | Semantics notes |
|---|---|---|---|
| `EvidenceFactObserved` | ACL adapters | Workflow A/B/C | Immutable observation with provenance; not a decision |
| `ContradictionDetected` | Reconciliation engine | Reviewer UI | Includes both sides verbatim |
| `AbstentionRaised` | Rules / optional inference | Human queue | Reason codes: unit, identity, time, authority, trust |
| `DuplicateCandidateProposed` | PV intake | PV specialist | Non-final; human merge outside AEGIS write path |
| `SupplyOptionGenerated` | Supply planner | Planner + Quality | Advisory; no inventory lock |
| `AuthorizationDenied` | Entitlement gate | All | Deny by default on stale/ambiguous authz |

Time semantics: preserve source precision (date-only vs timestamp vs timezone unknown). Do not coerce wearable or logger clocks to a single zone without `timezone_rules.csv` applicability (INJ-018; INJ-051).

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|
| R-501 | Risk | Teams treat RIM strength as ERP strength after seeing aliases | Wrong product evidence in release/supply packs | Domain | IDMP stewardship tests | Open |
| R-502 | Assumption | Offline CSV/fixture ACLs are sufficient substitutes for live LIMS/MES/QMS/safety adapters in POC | Examiner expects live connector demos | Architecture | Phase 5 defence | Accepted for POC |
| R-503 | Gap | Full event bus not implemented in Phase 2; events are logical contracts | Integration ADR needed in Phase 3 | Architecture | Artefacts 10–15 | Open |
| R-504 | Risk | BIOX acquisition mapping incomplete beyond organisations/system_inventory rows | Silent cross-tenant joins | Domain | INJ-005 deep dive in Evidence Map | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Seven business contexts + AEGIS consumer | Context map §2–4 | Review against SOURCE_SYSTEM_FACT_PACK | E-502 | Design accepted |
| LIMS/MES/QMS/Safety ACLs | §5 ACL table; D-202 | Contract tests on unit/identity/time preservation | E-505, E-510, E-512 | Design accepted |
| INJ-005 / INJ-021 / INJ-045 explicitly modeled | Aggregates + relationships | Fixture assertions on BIOX, SUA-88, NCB204-DE | E-503..E-506 | Design accepted |
| No regulated write paths | Aggregate invariants + E-511 | Prohibited-action suite; TEST-INJ-REG | `data/ai_use_boundaries.csv` | Accepted |
| D02/D03 write-path injects named and abstained | §6.1; D-203 | TEST-INJ-REG D02/D03 abstain | `submission/src/inject_controls.py` | Accepted |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Architecture/integration lead | Architecture | Confirm ACL deny-additional-properties | Adopted in §5 and D-202 | 2026-08-10 |
| GxP/quality lead | GxP | Confirm disposition remains outside aggregates | Confirmed §3 / §6 | 2026-08-10 |
| Product/value lead | Product | Align contexts to Workflows A–C only for POC | Confirmed §2 POC touch column; D-203 | 2026-08-10 |
