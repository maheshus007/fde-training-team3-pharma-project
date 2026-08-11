# Discovery Register — Prompt 01

| Field | Entry |
|---|---|
| Team | Team 3 |
| Date | 2026-08-10 |
| Prompt | `submission/prompts/01_discovery.md` |
| Framing mode | **decision-ready** (scope/problem); measured cycle-time baselines remain Unknown |
| Status | Complete — exit criteria met |

## 1. Repository and source-system map

| Area | Path / system | Role | Trust |
|---|---|---|---|
| Case mandate | `case/INTEGRATED_CASE.md`, stakeholder/source/regulatory packs | Problem + workflow boundaries | Narrative authority for workshop |
| Synthetic data | `data/*.csv` (139+ datasets) | Inject evidence, masters, entitlements | Deliberately defective; preserve contradictions |
| Knowledge | `knowledge/*.md` | Policies of mixed authority | Untrusted until status/hash/applicability checked |
| Source extracts | `source_documents/` | LIMS contracts, CCDS, protocol, cold-chain note | Versioned extracts |
| Evaluation | `evaluation/contracts/`, `public_fixtures/` | Fail-closed schemas + PUB inputs | Immutable challenge contracts |
| Starter defects | `starter/` | Unsafe brownfield clues | Not a solution |
| Explorer | `app/` (repo root) | Inject browser | Not participant product |
| Prior work | `submission/artefacts/01–21`, `src/`, `tests/` | Phase 0–4 design + hard-gate code | Reuse seed for AgenticApp |

**Fact:** Brownfield estate spans LIMS, MES/eBR, QMS, safety DB, RIM, IRT, serialization, vendor portals (`SOURCE_SYSTEM_FACT_PACK.md`).  
**Fact:** No system is universally authoritative — authority is by object, jurisdiction, effective time, process state, role.

## 2. Entities, identifiers, timestamp semantics

| Entity | Example IDs | Notes |
|---|---|---|
| Batch | `NCB204-B24071` | `batches.csv` |
| Material lot | `SUA-88`, `RESIN-R44` | Not interchangeable with batch_id |
| Product | RIM `NCB-204` vs ERP `NCB204-DE` | IDMP conflict INJ-045 |
| Lab result | `LR-88` | Units mg/L vs µg/mL INJ-024 |
| ICSR | `PV-1001`, `PV-1009`, `PV-1014` (INJ-037 triad — not a continuous 1001–1014 range) | Duplicate cluster |
| Shipment / logger / pallet | `SH-901`, `LG-31`, `P-88`/`P-89` | Association dispute INJ-051 |
| Organisation | NTG, BIOX, CMO-IE | Acquisition language INJ-005 |

**Time:** event time vs report time vs awareness clocks differ (PV INJ-038; wearables INJ-018; logger clocks INJ-051). Timezone tags required; `local_unknown` possible.

## 3. Evidence ownership and authority

| Data class | Primary SoT (contextual) | May not silently override |
|---|---|---|
| Batch genealogy | MES + warehouse (both required when conflict) | Neither alone |
| Lab results | LIMS (contract version matters v1/v2) | Unapproved CRO mapping |
| Quality events | eQMS | Spreadsheet calculators |
| ICSR facts | Global safety DB + affiliate/vendor receipts | Social media without authenticity |
| Listedness | IB / CCDS / local label per jurisdiction | Collapsed “global expectedness” |
| Inventory / quality status | Inventory + quality systems | Quarantined stock as available |
| AI boundaries | `ai_use_boundaries.csv` + executives | Speed KPIs |

## 4. Material inconsistencies / gaps (preserve)

| Inject | Conflict | Class |
|---|---|---|
| INJ-021 | SUA-88 `missing_branch` in MES yet issued in WM-90 | Fact |
| INJ-023 | OOS vs OOT vs invalid | Fact |
| INJ-024 | mg/L vs µg/mL; mapping `approved=no` | Fact |
| INJ-028 | QP packet missing supplier audit commitment | Fact |
| INJ-037/038/039/040 | Duplicates, clocks, MedDRA versions, listedness | Fact |
| INJ-045 | Strength/form/substance disagree | Fact |
| INJ-051 | Logger–pallet association disputed | Fact |
| INJ-031 | Validated vs conditional vs research labels | Fact |
| INJ-065/066/067/070 | Untrusted SOP, poisoned tool, stale auth, model hash | Fact (diagnostics) |

## 5. Stakeholder decisions and horizons

| Decision | Human owner | AI authority | Horizon |
|---|---|---|---|
| Batch certification / disposition | EU QP / Quality | **none** | Release lead time BR-01 due 2026-11-30 |
| Final PV seriousness/causality/reportability/signal | Safety Physician / PV | **none** | Expedited clocks |
| Stock reserve/allocate/ship/recall | Supply Governance + Quality | **draft options only** | Shortage / cold-chain events |
| Clinical eligibility | Clinical | **none** (out of AgenticApp POC) | — |

## 6. Constraints register

| Type | Constraint | Evidence |
|---|---|---|
| Board | −14% release lead time; no spec or Quality-authority change | BR-01 |
| Hard gate | No autonomous disposition / final PV / allocate-ship-recall | `ai_use_boundaries.csv` |
| Runtime | Offline synthetic mode; no secrets required | Package scope |
| Continuity | Batch/supply 14-day AI outage; PV manual (0h AI tolerance for expedited) | `continuity_requirements.csv` |
| Integrity | No silent unit conversion; no irreversible auto-merge | Scoring hard gates |
| Trust | Docs/tools untrusted until verified | INJ-065/066; D-008 |
| AuthZ | Execution-time re-check; deny stale cache | INJ-067; D-009 |

## 7. Current-state workflow sketch (as observed)

1. Humans chase evidence across LIMS/MES/QMS/safety/inventory spreadsheets.  
2. Conflicts often resolved informally or left opaque.  
3. Gateway may cache entitlements; tools may be mutable (starter defects).  
4. No unified citeable multi-hop path for genealogy / duplicates / cold-chain.  
5. AI pilots exist without fail-closed contracts in starter anti-patterns.

*(Inferred redesign steps marked out of Discovery — deferred to later prompts.)*

## 8. Fact / derivation / assumption / question

| ID | Type | Statement |
|---|---|---|
| F-01 | Fact | Three mandatory workflows A/B/C with prohibited actions defined in case §4 |
| F-02 | Fact | 84 injects pre-disclosed; no later instructor injects |
| F-03 | Fact | Contract schemas enforce `execution_status: not_executed` and supply `no_side_effects: true` |
| F-04 | Fact | Team 3 has policy_guard + 35 hard-gate tests; no workflow engines yet |
| D-01 | Derivation | Advisory reconciliation is the only capability class that satisfies BR-01 pressure without violating INJ-006 |
| A-01 | Assumption | Offline KG can express CQ multi-hop with provenance without cloud graph vendor (AA-003) |
| Q-01 | Question | What measured cycle-time baseline proves BR-01 contribution? (Unknown) |
| Q-02 | Question | Does examiner accept offline evidence KG superseding D-205 if RER fallback remains? |

## 9. Top ten investigation hypotheses

1. Genealogy conflict (INJ-021) is the highest-signal Workflow A demo.  
2. Unit abstention (INJ-024) is a hard-gate proof point.  
3. PV duplicate+clock+listedness cluster is Workflow B core.  
4. Cold-chain association (INJ-051) is Workflow C core.  
5. Stale auth + poisoned tools must sit in every agent tool path.  
6. Ontology prevents silent IDMP/MedDRA collapse.  
7. Offline KG improves citeable paths vs flat joins for defence narrative.  
8. HITL workbench required to counter automation bias (INJ-071).  
9. AI-disabled path must run same conflict detections.  
10. Naming split `supply_planning` vs `supply_options` will break orchestration if unfixed.

## 10. Early waste signals (Lean preview)

| Signal | DOWNTIME / AI waste | Observed vs hypothesized |
|---|---|---|
| Waiting on cross-system evidence chase | Waiting | Observed (case narrative) |
| Rework from unit/ID conflicts | Defects | Observed (injects) |
| Re-review of opaque packs | Extra processing | Hypothesized |
| Unbounded retrieval / token use | Retrieval waste | Hypothesized |
| Over-processing into disposition | Overproduction (risk) | Hypothesized if agent unconstrained |

## 11. Lean / DMAIC thin notes (for artefact 02)

1. Measurable today: diagnostic defect presence; contract pass/fail; prohibited-action deny rate.  
2. Unknown baselines: actual release lead time hours; PV intake cycle time.  
3. Top wastes: Waiting, Defects, Extra processing.  
4. Prompt 09 must Measure before claiming BR-01 %.

## Exit checklist

- [x] SoT and trust gaps explicit  
- [x] No target architecture proposed in this register  
- [x] Assumptions/questions separated  
- [x] Framing mode declared  
- [x] Backlog exists (see companion file)  
- [x] Early waste signals listed  
