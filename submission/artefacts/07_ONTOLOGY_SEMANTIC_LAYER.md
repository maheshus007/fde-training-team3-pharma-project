# Ontology and Semantic Layer

> Participant working artefact for Project AEGIS-PHARMA. Pharmaceutical ontology, temporal/jurisdictional semantics and MedDRA/IDMP conflict handling cite challenge evidence. Implementation remains under `submission/`.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Domain / evidence lead |
| Version / date | 1.1 / 2026-08-10 |
| Reviewers | PV governance (Safety); Regulatory; Architecture/integration |
| Status | Reviewed |
| Related requirements / ADRs | INJ-039, INJ-040, INJ-045; `knowledge/IDMP_MASTER_DATA_GOVERNANCE.md`; `knowledge/PV_LISTEDNESS_AUTHORITY.md`; D-201, D-205 |

## Purpose

Define a lightweight, versioned semantic layer — concepts, relations, identifiers, temporal and jurisdictional qualifiers, controlled vocabularies and units — sufficient for Workflows A–C to reason over evidence without collapsing MedDRA or IDMP conflicts into a single cleaned world model.

Accountable owner: Domain/evidence lead. Completion criteria: competency questions answered for A–C; MedDRA version and IDMP ambiguity handling specified; temporal/jurisdictional qualifiers mandatory on applicable assertions.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-701 | `case/INTEGRATED_CASE.md` INJ-039, INJ-040, INJ-045 | Case inject catalogue | MedDRA mismatch; listedness conflict; IDMP conflict | Narrative |
| E-702 | `data/terminology_versions.csv` | Terminology registry | MedDRA 27.1 legacy_cases; 28.0 current_global | Two active versions |
| E-703 | `data/adverse_events.csv` | Safety coding | PV-1001 PT Anaphylactic reaction @27.1; PV-1014 Infusion related reaction @28.0 | Same clinical theme, different PT |
| E-704 | `data/listedness_sources.csv`; `source_documents/CCDS_NCB204_v4.md` | Labeling / CCDS 2026-03-18 | Anaphylaxis listed in IB v12 and CCDS v4; not listed on IN local label | Jurisdictional conflict |
| E-705 | `data/medicinal_products.csv`; `data/idmp_mappings.csv` | RIM / ERP | Strength and dose_form disagree; mapping ambiguous | INJ-045 |
| E-706 | `data/controlled_vocabularies.csv` | Vocab 2026-1 | dose_form DF-001; route ROA-IV | Sparse coverage |
| E-707 | `data/product_master_aliases.csv` | Alias table | NCB204, brand_alias_B → NCB-204 | Non-authoritative |
| E-708 | `knowledge/IDMP_MASTER_DATA_GOVERNANCE.md` | K-015; 2026-04-08 | Do not merge identity conflicts without stewardship | Synthetic |
| E-709 | `knowledge/PV_LISTEDNESS_AUTHORITY.md` | PV knowledge | Listedness authority expectations | Check catalog status at use |
| E-710 | `data/timezone_rules.csv`; `data/wearable_readings.csv`; `data/temperature_loggers.csv` | Time sources | DST and local_unknown clocks | INJ-018, INJ-051 |
| E-711 | `data/regional_rules.csv`; `data/market_authorisations.csv` | Regional / MA | Jurisdiction-specific constraints | Sparse fixtures |
| E-712 | `data/api_contract_versions.csv` | Interface semantics | ICSR date precision variable; LIMS unit field rename | Contract ontology |

## 1. Competency questions

| ID | Competency question | Semantic capability required | Workflow |
|---|---|---|---|
| CQ-1 | Which material lots are evidenced as consumed by batch NCB204-B24071, and where do MES and warehouse disagree? | Batch–MaterialLot–EvidenceSource relation with conflict flag | A |
| CQ-2 | Is lab result LR-88 comparable to its specification given units? | Quantity + Unit + MappingApproval | A |
| CQ-3 | Are PV-1001 and PV-1014 the same case under different product names/codings? | Case–Case similarity; ProductAlias; MedDRAVersion | B |
| CQ-4 | For NCB-204 anaphylaxis, what does each listedness source say in which jurisdiction/version? | Product–Risk–SourceDocument–Jurisdiction–EffectiveDate | B |
| CQ-5 | Are RIM NCB-204 and ERP NCB204-DE the same medicinal product for strength/form? | MedicinalProduct–IdentifierScheme–MappingStatus | A/C |
| CQ-6 | Did shipment SH-901 experience an out-of-range excursion on an authenticated logger–pallet association? | Shipment–Logger–Pallet–TemperatureObservation–TimeContext | C |
| CQ-7 | Which supply options respect quality hold, MA and allocation ethics constraints? | Inventory–QualityStatus–MA–Constraint (advisory) | C |

## 2. Core concepts and relations

| Concept | Meaning | Key attributes |
|---|---|---|
| Organisation | Legal/operating entity | org_id, role, country |
| MedicinalProduct | Regulated product presentation | product_id, source scheme, strength, dose_form, substance |
| Substance | Active moiety / antibody code | substance id as received |
| Batch | Manufactured lot instance | batch_id, site, status, manufacture_date |
| MaterialLot | Input/component lot | material_lot, relation to batch |
| LabResult | Analytical observation | value, unit, spec, status, contract_version |
| QualityEvent | Deviation/OOS/EM excursion | taxonomy, status, links |
| IcsrCase | Safety case | case_id, receipts, narratives, sensitive segments |
| AdverseEventCoding | MedDRA-coded event | verbatim, version, PT |
| ListednessAssertion | Expectedness claim | product, risk, source, listed, jurisdiction |
| Shipment | Logistics movement | shipment_id, lots, lane, logger, pallet |
| TemperatureObservation | Cold-chain reading | temp, timestamp, timezone, logger, pallet |
| MarketAuthorisation | Licence in a region | product, region, status |
| EvidenceFact | Provenanced assertion | source, authority, effective_time, integrity_tags |
| Mapping | Cross-scheme link | from, to, status, approved, effective |

Primary relations: `consumed` / `missing_branch` / `issued`; `coded_as` (with version); `listed_in` / `not_listed_in`; `aliased_as`; `constrained_by`; `observed_under_time_context`.

Implementation choice (with D-205): versioned structured contracts and relational tables, not a mandatory OWL/RDF platform for POC.

## 3. Identifiers and aliases

| Scheme | Example | Rule |
|---|---|---|
| NTG product id | NCB-204 | Prefer for cross-context citations when mapping unambiguous |
| ERP local product | NCB204-DE | Retain for logistics/ERP evidence |
| Alias | NCB204, NovaBio mAb, brand_alias_B | Search only; never sole identity key |
| Batch id | NCB204-B24071 | Shared kernel across Mfg/Lab/Quality |
| Material lot | SUA-88 | Independent id; link via genealogy/movements |
| Case id | PV-1001 | Safety namespace |
| Org prefix | BIOX\|, NTG\|, CMO-IE\| | Required after acquisition (INJ-005) |
| IDMP mapping status | ambiguous_strength_presentation | Blocks auto-equivalence (D-201) |

Conflict handling for INJ-045: emit `IdentityConflict` with both MedicinalProduct records and mapping_status; human steward resolves per E-708.

## 4. Temporal and jurisdictional semantics

| Dimension | Model | Challenge evidence |
|---|---|---|
| Effective date | Every policy, label, MA, mapping carries effective_date/status | CCDS 2026-03-18; EMA letter 2026-07-28 with conflicting due dates (INJ-047) |
| Knowledge time vs event time | Record `recorded_at` separately from `event_time` | eBR back-entry (INJ-025); PV receipt vs awareness (INJ-038) |
| Timezone / DST | Require explicit timezone or mark `timezone_unknown`; apply `timezone_rules.csv` only when site known | Wearable local_unknown on 2026-03-29 DST (INJ-018); logger LG-31 mixed zones (INJ-051) |
| Precision | Preserve date-only vs second precision (E2B variable) | `api_contract_versions.csv` Safety ICSR |
| Jurisdiction | Assertions qualified by country/region (EU, US, IN, AE, …) | IN local label vs CCDS (INJ-040); MA divergence (INJ-046) |
| Supersession | Old protocol/policy retained with status=superseded | Protocol v4.1 vs v5.0 under `source_documents/`; BATCH_RELEASE_POLICY_OLD |

Rule: never project a fact into another jurisdiction or effective period without an explicit applicability record.

## 5. Controlled vocabularies and units

| Vocabulary | Source | Conflict / control |
|---|---|---|
| MedDRA | `terminology_versions.csv` + coding in `adverse_events.csv` | INJ-039: do not mix versions in a single signal grouping without version-aware clustering; retain both PTs |
| Dose form / route | `controlled_vocabularies.csv` DF-001, ROA-IV | ERP `solution` vs RIM `concentrate_for_infusion` — map only with approved synonym rule |
| Units | UCUM-oriented codes in LIMS v2 (`ucum_code`); v1 free-text `unit` | INJ-024: mg/L vs µg/mL numerically equal only if mapping approved (it is not) |
| Quality status | Source strings (`quality_hold`, OOS_LIMS, quarantine) | Do not normalize to a single enum that hides disagreement |
| Deviation taxonomy | `deviations.csv` codes | INJ-033 recurrence across codes — similarity is not the same code |

Unit semantic rule: Quantity = (numeric value, unit code, unit system, mapping_id?). Comparison to spec requires same unit or approved conversion; else abstain.

## 6. Entitlements and policy context

| Context attribute | Effect |
|---|---|
| purpose | e.g. `batch_review_readiness`, `pv_intake`, `supply_options` — limits visible object classes |
| role | Sensitive segments (pregnancy/paediatric INJ-041) require elevated role |
| jurisdiction | Hides non-applicable local labels from “global listedness” summaries unless explicitly multi-jurisdiction mode |
| trust_status | untrusted / referenced_missing documents cannot ground actionable policy |
| ai_authority | From `decision_rights.csv` / `ai_use_boundaries.csv` — ontology cannot grant write/disposition powers |

Stale entitlement cache hits deny access (INJ-067); semantic layer must not cache authz decisions beyond execution check.

## 7. Versioning and validation

| Artefact | Versioning approach | Validation |
|---|---|---|
| Terminology | MedDRA version on every coding | Reject unversioned PT in Workflow B outputs |
| Product master | mapping_status + source system | Reject auto-merge when ambiguous |
| API contracts | LIMS v1/v2; E2B_R3 | Adapter negotiates version; unknown fields denied |
| Knowledge/policy | document_catalog authority, effective_date, status | Retrieval must expose metadata (INJ-065) |
| Semantic contracts | Versioned JSON schemas under `submission/` (Phase 3+) | additionalProperties=false; golden fixture tests |

Acceptance: competency questions CQ-1..CQ-7 answered with citations and abstentions where conflicts exist; zero silent MedDRA or IDMP merges.

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|
| R-701 | Risk | Signal metrics ignore MedDRA version (INJ-044 amplifies) | False disproportionality | PV | Signal-support tests | Open |
| R-702 | Assumption | Sparse `controlled_vocabularies.csv` plus fixture codes suffice for POC | Broader IDMP/SPOR needed in production | Regulatory | Post-POC | Accepted for POC |
| R-703 | Gap | Full formal ontology (OWL) not authored | Rely on contracts + glossary | Domain | Revisit if KG adopted later | Open |
| R-704 | Risk | Treating CCDS as globally listed | Wrong expectedness in IN | PV | INJ-040 fixture | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| MedDRA version retained and conflicted PTs surfaced | §5 / CQ-3 | Fixture PV-1001 vs PV-1014 | E-702, E-703 | Design accepted |
| Listedness multi-source | §4 jurisdiction | IB/CCDS/IN label test | E-704 | Design accepted |
| IDMP non-merge | §3 / CQ-5; D-201 | NCB-204 vs NCB204-DE | E-705, E-708 | Design accepted |
| Temporal/timezone honesty | §4 | Wearable and logger fixtures | E-710 | Design accepted |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| PV / Safety reviewer | Safety | Require version-aware duplicate clustering | Adopted §5 MedDRA rule | 2026-08-10 |
| Regulatory | Regulatory | IDMP stewardship pointer | Linked E-708 / D-201 | 2026-08-10 |
| Architecture | Architecture | Align to non-mandatory KG | D-205 / artefact 08 | 2026-08-10 |
