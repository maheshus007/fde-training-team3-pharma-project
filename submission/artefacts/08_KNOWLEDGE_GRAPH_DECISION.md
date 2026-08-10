# Knowledge Graph Decision

> Participant working artefact for Project AEGIS-PHARMA. Decides whether a knowledge graph is required for the POC, with a simpler relational benchmark. Implementation remains under `submission/`.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Architecture/integration lead with Domain/evidence lead |
| Version / date | 1.1 / 2026-08-10 |
| Reviewers | Product/value lead; Evaluation/reliability lead; GxP/quality lead |
| Status | Reviewed |
| Related requirements / ADRs | `case/INTEGRATED_CASE.md` §8 KG decision; INJ-021, INJ-037, INJ-051, INJ-058; `data/RELATIONSHIP_MODEL.csv`; D-004, D-011, D-205 |

## Purpose

Decide whether AEGIS-PHARMA must implement a graph database / knowledge-graph runtime for Phase 2–5, or whether a simpler relational evidence register plus versioned contracts meets multi-hop inject needs (genealogy, duplicate PV, cold-chain) with lower complexity and clearer GxP validation.

Accountable owner: Architecture/integration lead. Completion criteria: written decision, benchmark comparison, exit criteria for revisiting, and explicit handling of multi-hop injects.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-801 | `case/INTEGRATED_CASE.md` §8 | Case | Participants must decide if KG is necessary | Strategic decision |
| E-802 | `data/RELATIONSHIP_MODEL.csv` | Package model | Declared parent/child rules including genealogy, duplicates, shipments | Relational-ready |
| E-803 | `data/material_genealogy.csv`; `data/warehouse_movements.csv`; `data/batches.csv` | Mfg evidence | SUA-88 missing_branch vs issued — shallow multi-hop conflict | INJ-021 |
| E-804 | `data/duplicate_candidates.csv`; `data/icsr_cases.csv`; `data/product_master_aliases.csv` | PV evidence | Precomputed similarity edges 0.93 / 0.71 | INJ-037 |
| E-805 | `data/shipments.csv`; `data/temperature_loggers.csv`; `source_documents/Cold_chain_logger_association_SH_901.md` | Supply evidence | SH-901 / LG-31 / P-88 vs P-89 dispute | INJ-051 |
| E-806 | `data/recall_candidates.csv`; `data/material_genealogy.csv` | Recall scope | Incomplete genealogy links | INJ-058 multi-hop pressure |
| E-807 | `data/inject_evidence_map.csv` | Inject index | Evidence file pointers for all 84 injects | Catalogue |
| E-808 | `PACKAGE_SCOPE_AND_ASSUMPTIONS.md` (package root) | Package scope | Offline synthetic mode; participant architecture freedom | Constraint |
| E-809 | `data/no_ai_baselines.csv` | Process excellence | Master-data/rules alternatives compete with AI | Prefer simple durable stores |

## 1. Decision criteria

| Criterion | Weight | Pass condition for adopting KG now |
|---|---|---|
| Multi-hop necessity | High | Relational joins/recursive CTE cannot express required hops with provenance |
| Fixture scale | Medium | Graph needed for performance at package scale (unlikely) |
| Validation / GxP burden | High | Graph runtime and query language can be validated as readily as SQL/contracts |
| Offline / vendor exit | High | Graph vendor does not worsen INJ-078/083 concentration |
| Time-to-working POC | High | Three workflows demonstrable within Phase 5 hours |
| Explainability | High | Paths remain citeable edge-by-edge to source rows |
| Reversibility | Medium | Can add graph later without rewriting evidence register |

Scoring rule: adopt KG in POC only if multi-hop necessity fails the relational benchmark on Workflow A/B/C fixtures.

## 2. Graph-required use cases

| Use case | Inject | Hop pattern | Graph-native appeal | Relational feasibility |
|---|---|---|---|---|
| Biologics genealogy break | INJ-021 | Batch → material_lot (MES) → warehouse movement → same lot | Path query highlights missing edge | Two-table join + conflict predicate on SUA-88 already exhibits break |
| Duplicate PV cluster | INJ-037 | Case ↔ case via similarity; case → product alias → product | Community detection | `duplicate_candidates` is already an edge list; alias join is 1–2 hops |
| Cold-chain association | INJ-051 | Shipment → logger → temperature rows → pallet ids | Inconsistency path | Join on logger; compare pallet attributes; preserve both P-88 and P-89 |
| Recall scope uncertainty | INJ-058 | Lot ↔ shared component ↔ equipment ↔ route | Deep variable-depth walk | Harder; may need recursive CTE; primary revisit trigger |
| Quality–safety link | INJ-043 | Complaint lot → batch → ICSR | Light multi-hop | Standard joins |
| Inspection evidence spanning domains | INJ-050 | Cross-context gather | Knowledge hub narrative | Evidence register + inject map sufficient for POC pack assembly |

Interpretation: A/B/C mandatory multi-hop injects are expressible without a graph DB because the package already materializes critical edges (`RELATIONSHIP_MODEL.csv`, `duplicate_candidates.csv`, genealogy rows).

## 3. Simpler alternative benchmark

**Chosen benchmark architecture: Relational Evidence Register + Versioned Contracts (RER+C)**

| Component | Description |
|---|---|
| Evidence register tables | Immutable fact rows: object_type, object_id, attribute, verbatim_value, unit, source_system, source_record_id, authority, effective_time, integrity_tags, retrieval_time |
| Relationship edges (relational) | Explicit edge table for genealogy, duplicate_candidates, logger associations, IDMP mappings — same grain as graph edges, stored as SQL/CSV |
| Contracts | JSON Schema / typed models per ACL; additional properties denied; idempotency keys |
| Multi-hop queries | Documented SQL/view patterns (or offline joins) with max-hop budget |
| Provenance | Every answer node/edge cites register row ids |
| Offline mode | Native CSV under `data/` + `submission/` derived views; no graph server |

Benchmark tasks (must pass before claiming unique KG value):

| Task | Success metric | Fixture oracle |
|---|---|---|
| T1 Genealogy conflict | Detect SUA-88 MES missing_branch vs WM-90 issued; cite both | E-803 |
| T2 Duplicate cluster | Return PV-1001–PV-1014 at similarity ≥ 0.9 with reasons; do not auto-merge | E-804 |
| T3 Cold-chain dispute | Flag SH-901 logger LG-31 pallet disagreement; abstain on single-pallet truth | E-805 |
| T4 Unit abstain | LR-88 abstain on unapproved mapping | `interface_mappings.csv` |
| T5 AI-disabled | T1–T4 succeed with inference off | INJ-082 |

If RER+C passes T1–T5, KG is not justified for POC.

## 4. Graph model and provenance

Although a graph DB is not selected for POC, the logical property-graph shape is recorded so a future migration is possible:

| Node types | Edge types | Provenance on every edge/node |
|---|---|---|
| Batch, MaterialLot, LabResult, Case, Product, Shipment, Logger, Organisation, Document | CONSUMED, ISSUED, MISSING_BRANCH, DUPLICATE_CANDIDATE, ALIAS_OF, OBSERVED_BY, CONSTRAINED_BY, CITES | source_system, record_id, effective_time, hash/status |

RER+C stores the same nodes/edges as tables. No separate mutable graph projection is allowed to become a system of record.

## 5. Query patterns and performance

| Pattern | RER+C approach | KG approach | POC choice |
|---|---|---|---|
| 1–2 hop conflict | SQL join + predicate | MATCH path | RER+C |
| Precomputed similarity | Read `duplicate_candidates` | Edge property | RER+C |
| Bounded recursion (recall) | Recursive CTE depth ≤ N with budget | Variable path | RER+C first; revisit |
| Full-text narrative | Optional embeddings behind kill switch | Graph+vector hybrid | Out of KG decision; optional AI |
| Package scale | Tens–hundreds of rows per dataset (`DATASET_PROFILE.csv`) | Overhead dominates | RER+C |

Performance claim: at disclosed fixture scale, relational joins meet interactive review latency; graph runtime would add operational dependency without accuracy gain on T1–T3.

## 6. Security and temporal filtering

| Control | How RER+C enforces | KG-specific risk avoided |
|---|---|---|
| Entitlement at execution | Filter register queries by purpose/role; deny stale cache | Graph traversal accidentally walking unauthorized nodes |
| Temporal applicability | Predicates on effective_time/timezone tags | Path queries ignoring time and mixing eras |
| Untrusted documents | trust_status attribute blocks policy edges | Prompt-injected SOP becoming a traversable “instruction” node (INJ-065) |
| Prohibited writes | No disposition/allocate edge types writable | Agent creating RESERVED_FOR edges (INJ-080) |
| Provenance | Mandatory columns | Orphan graph nodes without CSV lineage |

## 7. Decision and exit criteria

**Decision D-205 (elaborates D-011): Do not implement a knowledge-graph database for the Phase 2–5 AEGIS-PHARMA POC. Implement the Relational Evidence Register + Versioned Contracts benchmark as the system of evidence assembly.**

Rationale:

1. INJ-021, INJ-037 and INJ-051 multi-hop needs are satisfied by existing edge-like fixtures and shallow joins.
2. Aligns with D-004 (deterministic/offline first) and process-excellence competition (E-809).
3. Lower validation and vendor-concentration burden (INJ-078, INJ-083).
4. Preserves a logical graph model (§4) for later adoption without treating KG as mandatory.

**Exit criteria — reopen KG adoption if any become true:**

| ID | Trigger |
|---|---|
| X-1 | Evaluation shows INJ-058 recall-scope completeness/latency fails recursive CTE under agreed budgets |
| X-2 | Cross-domain inspection pack (INJ-050) cannot be assembled with citeable paths without graph traversal features |
| X-3 | Examiner-accepted production constraint requires standardized graph interchange already validated elsewhere — still must pass T1–T5 parity |

Until an exit trigger fires, team communications and architecture diagrams present RER+C, not a graph product dependency.

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|
| R-801 | Risk | Stakeholders equate “semantic layer” with mandatory Neo4j-style KG | Scope creep | Architecture | Defence narrative | Open |
| R-802 | Assumption | Precomputed `duplicate_candidates` remain available offline | Would need online similarity service | Domain | Fixture change | Accepted |
| R-803 | Gap | Recursive recall queries not yet coded | Phase 5 implementation | Build | POC | Open |
| R-804 | Risk | Future KG added without migrating provenance columns | Integrity break | Architecture | X-1..X-3 | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| Explicit KG decision | D-205 / D-011 / §7 | Design review | E-801 | Accepted — KG not required for POC |
| Simpler alternative benchmarked | RER+C §3 | T1–T5 planned tests | E-802..E-805 | Design accepted |
| Multi-hop injects covered | §2 table | Genealogy, duplicate, cold-chain fixtures | INJ-021/037/051 | Design accepted |
| Revisit path for deep recall | X-1 / INJ-058 | Evaluation gate | E-806 | Documented |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Product/value lead | Product | Prefer simplest path that hits workflows | Confirmed D-205 | 2026-08-10 |
| Evaluation lead | Evaluation | Require T1–T5 before any KG claim | Adopted §3 | 2026-08-10 |
| GxP lead | GxP | Graph must not become SoR if added later | §4 / §6 | 2026-08-10 |
| Domain lead | Domain | Logical graph shape retained | §4 | 2026-08-10 |
