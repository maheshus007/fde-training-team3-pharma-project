# DDD Context Map — AgenticApp (Prompt 04)

> Deepened from `submission/artefacts/05_DDD_CONTEXT_MAP.md` plus Gen AI / agent / offline-KG domain extensions. Challenge evidence remains authoritative; this file is the SDD working domain model.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Domain / evidence lead |
| Version / date | 2.0 / 2026-08-10 |
| Prompt | `submission/prompts/04_ddd.md` |
| Artifact status | **stable** for ubiquitous language, contexts, ACLs, aggregates, ownership; **provisional** for offline evidence KG as *runtime* (awaiting CQ proofs — see ADR-AA-015) |
| Narrative class (Prompt 02) | decision-ready |
| Seed | `submission/artefacts/05_DDD_CONTEXT_MAP.md` v1.1 |
| Related | PRD `03_prd/PRD.md`; SCQA `02_scqa/`; D-001..D-010, D-201..D-203, D-205; INJ-005/021/024/037–040/045/051/006 |

## Purpose

Define ubiquitous language, bounded contexts (Research through Supply + Evidence Platform), context relationships, anti-corruption layers, aggregates/invariants, event semantics, and Gen AI / HITL / agent boundaries so AEGIS AgenticApp can reconcile evidence with ontology and citeable paths **without** becoming a system of record or transferring regulated decisions.

**Completion criteria:** each POC workflow maps to owning contexts; ACLs preserve source identity, unit, time and authority; acquisition/IDMP conflicts remain explicit; rules vs AI vs HITL are explicit; Prompt 04 Produce §§1–16 covered (Gen AI detail also in `GEN_AI_BOUNDARIES.md`).

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-501 | `case/INTEGRATED_CASE.md` §2, §4, §5, §7 | Case narrative | Fragmented estate; workflows A/B/C; operating properties; injects | Narrative, not SoR |
| E-502 | `case/SOURCE_SYSTEM_FACT_PACK.md` | Fact pack | Domain systems; authority is contextual | Summary |
| E-503 | `data/organisations.csv` | Org master | NTG; BIOX acquired; CMO-IE | Three orgs only |
| E-504 | `data/system_inventory.csv` | Inventory | LIMS-4 validated; BIOX-ELN research; AI pilot | Conflicts with validation inventory (INJ-031) |
| E-505 | `data/material_genealogy.csv`; `warehouse_movements.csv`; `batches.csv` | MES / WM / batch | SUA-88 `missing_branch` vs WM-90 issued for NCB204-B24071 | INJ-021 |
| E-506 | `data/medicinal_products.csv`; `idmp_mappings.csv` | RIM vs ERP | NCB-204 vs NCB204-DE; `ambiguous_strength_presentation` | INJ-045 |
| E-507 | `data/RELATIONSHIP_MODEL.csv` | Package model | Declared parent/child links | Join rules, not runtime ACL |
| E-508 | `knowledge/IDMP_MASTER_DATA_GOVERNANCE.md` | K-015; 2026-04-08 | No merge without stewardship | Synthetic |
| E-509 | `knowledge/BATCH_RELEASE_EVIDENCE_POLICY.md` | Knowledge catalog | Batch evidence expectations | Check vs OLD policy |
| E-510 | `source_documents/LIMS_result_contract_v1.md` / `v2.md` | Contract extracts | Unit/status field rename | Drift risk |
| E-511 | `data/ai_use_boundaries.csv` | Executive | Allowed reconcile/cite/flag/abstain; prohibited disposition/PV final/allocate | Binding |
| E-512 | `data/api_contract_versions.csv` | Interface registry | LIMS v1/v2; ICSR date precision variable | Versioned contracts |
| E-513 | `data/duplicate_candidates.csv`; `icsr_cases.csv` | Safety | PV-1001 / PV-1009 / PV-1014 cluster | INJ-037 |
| E-514 | `data/interface_mappings.csv` | Mapping registry | CRO_LAB_TO_LIMS `approved=no` | INJ-024 |
| E-515 | `data/shipments.csv`; `temperature_loggers.csv`; cold-chain note | Supply | SH-901 / LG-31 / P-88 vs P-89 | INJ-051 |
| E-516 | `data/ai_use_boundaries.csv` + case INJ-006 | Executive | Also prohibits autonomous formulation/specification/eligibility change | Binding |

---

## 1. Frame business problem (domain terms)

Authorized **Quality, PV and Supply** reviewers must obtain a provenanced **BatchEvidencePack**, **IcsrIntakeCluster**, and **SupplyOptionSet** that surface contradictions, gaps and abstentions — without AEGIS owning **disposition**, **final PV judgements**, **stock execution**, **formulation/specification change**, or **clinical eligibility** (E-501; E-511; E-516; PRD in/out scope).

Capability question (from Prompt 02, capability-level): what bounded advisory domain capability improves reconciliation across A/B/C while preserving human decision rights? Architecture choices (KG runtime, agent topology) are **candidates**, not domain facts — recorded as provisional under ADR-AA-015 / C4.

---

## 2. Domains and subdomains

| Type | Subdomain | Notes |
|---|---|---|
| **Core** | Quality evidence reconciliation (batch-review readiness) | Workflow A |
| **Core** | PV intake and signal-**support** (not confirmation) | Workflow B |
| **Core** | Supply shortage / cold-chain **option advising** | Workflow C |
| **Supporting** | Ontology / semantic governance | Meaning, units, MedDRA, IDMP |
| **Supporting** | Evidence graph / multi-hop citation (logical; runtime provisional) | Citeable paths |
| **Supporting** | Authorization, purpose-binding, audit | Cross-cutting |
| **Generic** | Identity & access plumbing; fixture/file storage | Not the domain model |

Research and Clinical are **supporting adjacency contexts** for POC (identity/time collisions only) — not full core automation (D-203).

---

## 3. Ubiquitous language

| Term / question | Evidence-based meaning | Decision / owner | Acceptance |
|---|---|---|---|
| Batch vs lot vs material_lot | `batch_id` (e.g. NCB204-B24071) ≠ `material_lot` (SUA-88, RESIN-R44); warehouse issues material_lot against batch_id | Keep native terms; map via ACL | E-505; INJ-021 |
| Product identity | RIM `NCB-204` (100 mg/10 mL concentrate) vs ERP `NCB204-DE` (10 mg/mL solution); aliases non-authoritative | Never auto-collapse; IDMP conflict (D-201) | E-506; E-508; INJ-045 |
| Quality hold vs disposition | `status=quality_hold` is SoR state; disposition (release/reject/reprocess/relabel/recall) is human-only outside AEGIS | Product + GxP | E-505; E-511 |
| Case vs signal | ICSR intake/clustering = Workflow B; **signal confirmation prohibited** | PV governance | E-501; E-511 |
| Option vs allocation | Options = advisory drafts; reserve/allocate/ship prohibited | Supply + Quality | E-511 |
| Readiness | Evidence completeness for **authorized human review** — not “released” | Quality | E-501 |
| Duplicate candidate | Similarity proposal with reason; **not** merged case | PV | E-513; INJ-037 |
| Abstain | Explicit non-resolution with reason code | Domain + GxP | Hard gates |
| EvidenceFact | Provenanced assertion (source, authority, time, integrity) | Domain | Contracts |
| Authority | Later timestamp ≠ higher authority automatically | Domain | E-502 |
| Acquisition language | BIOX codes / BIOX-ELN remain acquired-context until stewardship maps (INJ-005) | Domain | E-503; E-504 |
| Awareness clock | Receipt/awareness dates may differ by channel; do not collapse | PV | INJ-038 |
| Listedness | Per IB / CCDS / local label + jurisdiction; no global collapse | PV + Regulatory | INJ-040 |

**Unresolved (flagged, not invented):** measured BR-01 cycle-time hours (Unknown); exact agent token budgets (provisional in ADR-AA-009).

---

## 4. Bounded contexts

| Context | Core responsibility | Primary systems (E-502) | POC workflow touch | Owner role | Decisions owned |
|---|---|---|---|---|---|
| Research / Discovery | Compound, assay, omics; research-only models | ELN, assay, compound registry, BIOX-ELN | Identity collisions into Mfg/Regulatory (INJ-005, INJ-008) | Research steward | Research identity stewardship — **not** automated by AEGIS |
| Clinical | Protocol, consent, eligibility, endpoints, clocks | EDC, CTMS, eConsent, IRT, wearables | Time integrity (INJ-018); **no eligibility determination** | Clinical ops | Eligibility / protocol execution — human |
| Manufacturing | Genealogy, eBR, PAT, campaign | ERP, MES, eBR, historian, warehouse | Workflow A (INJ-021..028) | Manufacturing / CMO liaison | Campaign/genealogy SoR facts |
| Laboratory (QC) | Assay results, OOS/OOT, units | LIMS, CDS, instruments | Workflow A unit/OOS (INJ-023, INJ-024) | QC | Lab status SoR |
| Quality | Deviations, CAPA, validation, supplier quality, release-packet completeness | eQMS, DMS, training, supplier quality | Workflow A readiness; **never disposition** | Quality / QP support | Disposition / certification (QP) |
| Safety (PV) | ICSR intake, clocks, listedness, duplicates | Global safety DB, affiliates, vendors | Workflow B (INJ-037..044) | PV | Final seriousness/causality/reportability/signal |
| Regulatory | MA, labels, IDMP/SPOR, commitments, eCTD | RIM, eCTD, labeling | Product identity + MA for A/C (INJ-045..050) | Regulatory | IDMP merge / labeling authority |
| Supply | Inventory, cold-chain, serialization, shortage options | Serialization, logistics, CMO portals | Workflow C (INJ-051..058) | Supply | Allocation/shipment execution (governance board) |
| Evidence / AI platform | Contracts, ontology, (logical) evidence graph, entitlements, audit, offline mode, agent orchestration | AI gateway, tools, model registry | All; **advisory only** | Architecture + Security | Tool allowlist / kill switch — not GxP finals |

AEGIS is a **consumer with ACLs**, not a new SoR (D-203).

---

## 5. Context map (relationships)

```
Research --(conformist / ACL)--> Regulatory (substance/product codes)
Clinical --(customer-supplier)--> Supply (trial demand) and Safety (SUSAR clocks)
Manufacturing --(shared kernel: batch_id)--> Laboratory --> Quality
Manufacturing <-> Warehouse --(partnership + conflict surfacing)-- INJ-021
Quality --(customer-supplier evidence)--> Regulatory (release/MA evidence)
Safety --(published language via ACL)--> Regulatory (listedness / labels)
Supply --(anticorruption)--> Manufacturing (lot/genealogy) and Quality (hold status)
BIOX --(ACL / open-host)--> NTG contexts (INJ-005)
AEGIS Evidence Platform --(ACL consumer of all; never upstream SoR)--> all contexts
```

| Relationship | Pattern | Why | Inject / evidence |
|---|---|---|---|
| Manufacturing ↔ Warehouse | Partnership with conflict surfacing | MES `missing_branch` vs warehouse issued | INJ-021; E-505 |
| Laboratory ↔ Manufacturing | Customer-supplier via versioned LIMS contract | Unit/status field drift v1→v2 | E-510; E-512; INJ-024 |
| Safety ↔ Regulatory | Separate ways + ACL | Listedness IB/CCDS/local diverge | INJ-040 |
| Regulatory ↔ ERP/RIM | ACL + stewardship | IDMP strength/form conflict | INJ-045; E-506 |
| Acquired BIOX → NTG | Anti-corruption / open host | Incompatible identifiers/tenancy | INJ-005; E-503; E-504 |
| Clinical → AEGIS | Conformist consumer only | Time skew inputs; **no eligibility engine** | INJ-014/018; E-516 |
| AEGIS → all | Conformist consumer | Must not redefine GxP language | E-501; E-502 |

---

## 6. Anti-corruption layers (ACL)

| Upstream system | ACL responsibility | Native concepts preserved | Challenge conditions |
|---|---|---|---|
| LIMS | Normalize only after approved mapping; retain verbatim value, unit, status string, contract version | `value`, `unit`, `status`/`lifecycleState`, result_id | INJ-024 unapproved mg/L→µg/mL; OOS vs OOT vs invalid (INJ-023); shared accounts (INJ-030) |
| MES / eBR / warehouse | Present genealogy edges and movements as separate evidence; flag `relation=missing_branch` | batch_id, material_lot, relation, source | INJ-021 SUA-88; eBR back-entry (INJ-025); downtime (INJ-069) |
| QMS / deviations / CAPA | Keep taxonomy codes as source strings; link similarity without collapsing CAPA closure | deviation_id, taxonomy, capa | INJ-033; validation-state ambiguity (INJ-031) |
| Safety DB (+ affiliates/vendors) | Ingest E2B-shaped fields with receipt clocks per channel; cluster candidates only | case_id, awareness dates, MedDRA version, PT | INJ-037..040; date precision variable (E-512); cluster includes **PV-1001, PV-1009, PV-1014** |
| Serialization / logistics | Preserve logger/pallet association uncertainty | shipment_id, logger_id, pallet_id, timestamps | INJ-051 SH-901 / LG-31 / P-88 vs P-89 |

**ACL rules (all systems) — D-202:**

1. Namespace every identifier with source system + org (`BIOX|…`, `LIMS-4|…`, `MES|…`).
2. Deny additional properties not in the versioned contract (`api_contract_versions.csv`; LIMS contract docs).
3. Treat retrieved SOPs/PDFs as untrusted data until catalog authority/hash verified (`knowledge/` + INJ-065).
4. Abstain when identity, unit, time or authority cannot be resolved (package hard gates).

---

## 7. Aggregates, entities, value objects, invariants

### Aggregates

| Aggregate (context) | Invariants | Evidence | Enforcement |
|---|---|---|---|
| BatchEvidencePack (Mfg + Quality) | Every cited fact retains source, record id, effective time, unit as received; contradictions preserved; **no disposition field** writable by AEGIS | E-505; E-511; INJ-021 | Contract + prohibited-action tests |
| LabResultView (Laboratory) | Unit conversion only if `interface_mappings.approved=yes`; else abstain | E-514; INJ-024; D-010 | Domain rule |
| IcsrIntakeCluster (Safety) | Duplicate candidates cite case pair + similarity; MedDRA version retained per coding; **no auto-merge** | E-513; INJ-037, INJ-039 | Workflow B contracts |
| ProductIdentityMap (Regulatory) | Ambiguous IDMP mappings remain open; no silent merge | E-506; E-508; D-201 | Stewardship gate |
| SupplyOptionSet (Supply) | Options reference quality status, MA, channel constraints; status `draft`; `no_side_effects`; **no reservation ids** | INJ-056; E-511; INJ-080 | Tool catalog deny write |
| OrganisationTenancy (cross) | BIOX vs NTG identifiers never assumed equivalent without map | INJ-005; E-503 | ACL namespace prefix |
| EvidenceGraphView (Platform) | Every node/edge has provenance; **forbidden** write edge types: disposition/allocate/ship/recall/signal_confirmed | ADR-AA-015 (provisional runtime) | Schema + tests |
| AgentRun (Platform) | Budget, checkpoint, stop reason; every tool result policy-checked; purpose-bound | case §5 | Orchestrator + policy_guard |

### Value objects (selected)

`ProvenanceStamp` {source, record_id, authority, effective_at, retrieved_at, integrity_sha256, trust_status}; `Quantity` {value, unit, contract_version}; `MedDRACoding` {pt, version}; `ListednessAssertion` {source_doc, jurisdiction, listed, effective_at}; `PurposeCode`; `EntitlementDecision`.

### Entities (selected)

Batch, MaterialLot, LabResult, Deviation, IcsrCase, Shipment, TemperatureLogger, MarketAuthorisation, ToolManifest, ReviewAcknowledgement.

---

## 8. Ownership and change boundaries

| Object | System of record | AEGIS may | AEGIS must not |
|---|---|---|---|
| Batch disposition / quality status change | Quality / QP systems | Cite hold and evidence gaps | Release, reject, reprocess, relabel, recall, change quality status |
| Lab result / OOS conclusion | LIMS / QC investigation | Flag conflicts | Overwrite status |
| ICSR final seriousness/causality/expectedness/reportability / signal confirmation | PV medical review | Extract, cluster, cite | Final PV judgement / signal confirmation |
| Product IDMP merge | Regulatory stewardship | Show conflict | Auto-merge |
| Stock reservation / allocation / shipment | Supply execution | Rank **draft** options | Reserve, allocate, ship |
| Formulation / specification | CMC / Quality | Cite registered specs | Autonomous change (INJ-006) |
| Clinical eligibility | Clinical | N/A in POC | Determine eligibility (INJ-014) |
| Entitlements | IAM | Re-check at execution | Trust stale gateway cache (INJ-067) |

Change control for ACL mappings: Domain/evidence + Architecture review. Emergency vendor hotfixes without retrospective approval = defects (INJ-034), not bypasses.

---

## 9. Event storming / event semantics

| Event | Publisher | Consumers | Semantics |
|---|---|---|---|
| `EvidenceFactObserved` | ACL adapters | Workflows A/B/C | Immutable observation with provenance; not a decision |
| `ContradictionDetected` | Reconciliation engine | HITL workbench | Includes **both** sides verbatim |
| `AbstentionRaised` | Rules / optional inference | Human queue | Reason codes: unit, identity, time, authority, trust |
| `ReadinessAssessed` | Batch engine | HITL | States: insufficient_evidence / conflicted_evidence / ready_for_authorized_review — **not** released |
| `DuplicateCandidateProposed` | PV intake | PV specialist | Non-final; human merge outside AEGIS write path |
| `ClockConflictSurfaced` | PV intake | PV specialist | Multi-channel awareness dates retained |
| `SupplyOptionGenerated` | Supply planner | Planner + Quality | Advisory; no inventory lock |
| `AuthorizationDenied` | Entitlement gate | All | Deny-by-default on stale/ambiguous authz |
| `BudgetExhausted` | Agent runtime | Audit + HITL | Stop without partial regulated side effects |
| `CheckpointSaved` | Agent runtime | Recovery | Resume must be idempotent |
| `HumanReviewRequested` | Orchestrator | Workbench | Forced evidence viewing |
| `KillSwitchEngaged` | Ops / Security | Inference adapter | Rules/KG/HITL remain |

**Time semantics:** preserve source precision (date-only vs timestamp vs timezone unknown). Do not coerce wearable or logger clocks to a single zone without `timezone_rules.csv` applicability (INJ-018; INJ-051).

---

## 10. Gen AI boundary design (summary)

Full detail: `GEN_AI_BOUNDARIES.md`. Required Prompt 04 coverage:

| # | Topic | Location |
|---|---|---|
| 8 | Rules vs AI reasoning | GEN_AI §1 |
| 9 | RAG from DDD artefacts | GEN_AI §2 |
| 10 | Agent responsibilities | GEN_AI §3 |
| 11 | HITL & decision ownership | GEN_AI §4 + ownership table §8 |
| 12 | Evidence & audit trail | GEN_AI §5 |
| 13 | Evaluation in DDD vocabulary | GEN_AI §6 |
| 14 | Minimum governed workflow | GEN_AI §7 |
| 15 | Pilot / refine notes | GEN_AI §8 |
| 16 | Production readiness (domain view) | GEN_AI §9 |

**AI must never decide alone:** batch disposition; final PV seriousness/causality/expectedness/reportability; signal confirmation; reserve/allocate/ship; quality-status change; recall initiation; formulation/specification change; clinical eligibility (E-511; E-516).

---

## 11. Boundary risks and unresolved questions (→ Prompt 05/06)

| ID | Type | Description | Impact | Owner | Status |
|---|---|---|---|---|---|
| R-501 | Risk | Teams treat RIM strength as ERP strength after aliases | Wrong product evidence | Domain | Open |
| R-502 | Assumption | Offline CSV/fixture ACLs substitute for live adapters in POC | Examiner expects live connectors | Architecture | Accepted for POC |
| R-503 | Gap | Full event bus not implemented; events are logical | Integration detail in C4/SRS | Architecture | Open |
| R-504 | Risk | BIOX mapping incomplete | Silent cross-tenant joins | Domain | Open |
| R-505 | Risk | Offline KG runtime adopted before CQ proofs | Examiner cites D-205 | Architecture | Mitigate: **provisional** ADR-AA-015; RER fallback |
| R-506 | Gap | `policy_guard` still uses `supply_planning` string | Supply denies miss | Build | **Closed T-001** — canonical `supply_options`; alias unknown |
| Q-D1 | Question | Does examiner accept provisional KG if RER parity holds? | Defence | Architecture | Open |
| Q-D2 | Question | Measured BR-01 baseline | Value claim | Evaluation | Unknown |

**Backlog links that de-risk provisional KG:** Prompt 01 backlog P1 CQ executable proofs; P0 supply enum fix.

---

## 12. Lean / DMAIC Analyze notes (thin → artefact 02)

1. **Defects removed by invariants:** no silent unit convert; no IDMP/MedDRA collapse; no auto-merge; no disposition fields — not left to the model.  
2. **HITL:** force conflict viewing on readiness/options; do not require re-review of already-cited verbatim facts.  
3. **RAG/agent waste:** purpose-bound retrieval; budgets/stop; signed tools only.  
4. **Ambiguities causing Motion:** batch vs material_lot; hold vs disposition; option vs allocation — glossary mandatory in UI copy.

---

## 13. Traceability and acceptance

| Claim | Control | Test / evaluation | Evidence | Result |
|---|---|---|---|---|
| Business contexts + AEGIS consumer | §§4–5 | Review vs SOURCE_SYSTEM_FACT_PACK | E-502 | Design accepted |
| LIMS/MES/QMS/Safety ACLs | §6; D-202 | Contract tests unit/identity/time | E-505, E-510, E-512 | Design accepted |
| INJ-005 / 021 / 045 modeled | Aggregates + relationships | Fixture assertions BIOX, SUA-88, NCB204-DE | E-503..E-506 | Design accepted |
| INJ-037 cluster includes PV-1009 | IcsrIntakeCluster | Duplicate candidate fixtures | E-513 | Design accepted |
| No regulated write paths | §7–8; E-511/516 | Prohibited-action suite | `ai_use_boundaries.csv` | Design accepted |
| Gen AI §§8–16 | GEN_AI_BOUNDARIES.md | Architecture review | This pack | Design accepted |
| KG runtime | Provisional | CQ-1/3/6 tests before “accepted” | ADR-AA-015 | **Provisional** |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Domain/evidence | Domain | AgenticApp v1 DDD omitted ACLs/Research/Clinical/events | Expanded to v2.0 from seed 05 | 2026-08-10 |
| Architecture | Architecture | KG must not silently override D-205 | Status provisional + RER fallback + ADR-AA-015 | 2026-08-10 |
| GxP | GxP | Confirm formulation/eligibility prohibitions | Added to ownership + never-alone | 2026-08-10 |
