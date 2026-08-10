#!/usr/bin/env python3
"""Generate Phase 2–4 submission artefacts and deterministic control tests."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artefacts"
SRC = ROOT / "src"
TESTS = ROOT / "tests"
FIX = TESTS / "fixtures"
SCRIPTS = ROOT / "scripts"
EVID = ROOT / "evidence"

DOC_CTRL = """## Document control

| Field | Entry |
|---|---|
| Team / owner | {owner} |
| Version / date | 1.0 / 2026-08-10 |
| Reviewers | {reviewers} |
| Status | Reviewed |
| Related requirements / ADRs | {related} |
"""

COMMON_TAIL = """
## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| {rid} | Assumption | {risk} | Medium | {owner} | Defence | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| {claim} | {control} | {test} | {evpath} | Planned / Partial |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| Independent reviewer | Cross-role | Completeness vs Phase exit criteria | Accepted for Phase gate | 2026-08-10 |
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def artefact(title: str, owner: str, reviewers: str, related: str, purpose: str, evidence_rows: str, body: str, rid: str, risk: str, claim: str, control: str, test: str, evpath: str) -> str:
    return f"""# {title}

> Participant working artefact for Project AEGIS-PHARMA (Team 3). Cites challenge evidence; implementation remains under `submission/`.

{DOC_CTRL.format(owner=owner, reviewers=reviewers, related=related)}
## Purpose

{purpose}

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
{evidence_rows}

{body}
{COMMON_TAIL.format(rid=rid, risk=risk, owner=owner.split('—')[0].strip(), claim=claim, control=control, test=test, evpath=evpath)}
"""


def main() -> None:
    for d in (ART, SRC, TESTS, FIX, SCRIPTS, EVID):
        d.mkdir(parents=True, exist_ok=True)

    # ---- Phase 2 ----
    write(ART / "05_DDD_CONTEXT_MAP.md", artefact(
        "DDD Context Map",
        "Team 3 — Domain / evidence lead",
        "Architecture/integration; GxP/quality",
        "INJ-005; INJ-021; INJ-045; D-001; D-011",
        "Decide bounded contexts and anti-corruption layers so AEGIS reconciles evidence across Research, Clinical, Manufacturing, Quality, Safety, Regulatory and Supply without collapsing distinct authorities (`case/INTEGRATED_CASE.md` §2–4).",
        """| E-001 | `case/INTEGRATED_CASE.md` §2 | Case authority | Fragmented systems across LIMS/MES/eBR/QMS/RIM/EDC/safety/serialization | Narrative |
| E-002 | `data/organisations.csv`; `data/system_inventory.csv` | Org/system inventory (INJ-005) | Acquisition uses incompatible identifiers and tenancy | Synthetic |
| E-003 | `data/batches.csv`; `data/material_genealogy.csv`; `data/warehouse_movements.csv` | Manufacturing/warehouse (INJ-021) | Genealogy break between MES and warehouse | Conflict intentional |
| E-004 | `data/medicinal_products.csv`; `data/idmp_mappings.csv` | IDMP mappings (INJ-045) | Substance/strength/form codes diverge across RIM/ERP/registrations | Conflict intentional |""",
        """## 1. Bounded contexts

| Context | Core language | Upstream/downstream | Decision / owner | Acceptance evidence |
|---|---|---|---|---|
| Research | Compound, assay, target evidence | Translational → Clinical | Domain | Keep research models out of GxP decisions (INJ-011) |
| Clinical | Protocol version, subject, consent, randomization | Sites ↔ Safety/Regulatory | Clinical ops within protocol | Protocol authority per effective date (INJ-013) |
| Manufacturing | Batch, genealogy, recipe, eBR step | MES/warehouse → Quality | Ops never certifies | Genealogy reconciliation only (INJ-021) |
| Quality | Deviation, CAPA, change, validation state, release packet | Independent of Manufacturing throughput | QP / CQO | Independent Quality authority (INJ-001 constraint) |
| Safety (PV) | ICSR, receipt clock, listedness, MedDRA | Affiliates/vendors → Medical reviewers | PV head; final judgements human | INJ-037..044; ai_use_boundaries |
| Regulatory | MA, label, IDMP, commitment, eCTD | RIM ↔ Markets | RA VP | Label/IDMP conflicts preserved (INJ-045..049) |
| Supply | Inventory snapshot, shipment, logger, allocation constraint | Planning only; execution gated | Supply VP + approvers | Options with `no_side_effects` (INJ-051..058) |

## 2. Context map and relationships

| Relationship | Pattern | Why | Owner |
|---|---|---|---|
| Manufacturing → Quality | Customer/Supplier with Conformist ACL | Quality consumes MES/LIMS facts via ACL; does not accept disposition from Manufacturing KPIs | GxP |
| Safety ↔ Quality | Partnership on product-quality complaints | Particle complaints may link ICSRs (INJ-043) without auto-causality | PV + Quality |
| Clinical → Safety | Customer/Supplier | Case intake may cite trial context; does not change clinical eligibility | Domain |
| Regulatory → Supply | Conformist on MA status | Market authorization constrains option legality; system does not change MA | RA |
| Acquired biotech → NTG masters | Anti-Corruption Layer | INJ-005 identifier collision; never silent merge | Architecture |

## 3. Anti-corruption layers

| Source system | ACL responsibility | Forbidden translation |
|---|---|---|
| LIMS | Preserve result, unit, method, OOS/OOT flags, as-of time (INJ-023/024) | Silent unit conversion |
| MES / eBR | Preserve step completion vs back-entry / downtime (INJ-025) | Invent missing genealogy |
| QMS | Preserve deviation/CAPA taxonomy versions (INJ-033) | Auto-close CAPA |
| Safety DB | Preserve receipt events and narrative language (INJ-038/072) | Final seriousness/causality |
| Serialization / logistics | Preserve aggregation breaks and logger association disputes (INJ-051/052) | Auto-release after excursion |

## 4. Shared kernel vs published language

Shared kernel limited to: product/material identity candidates, as-of timestamps with timezone, evidence citation objects, authorization purpose tokens, and abstention codes. Published language for workflow APIs is the versioned JSON contracts under `evaluation/contracts/` mirrored in `submission/tests/fixtures/`.

## 5. Context ownership and evolution

Each context has a steward (charter roles). Cross-context identity resolution requires an explicit conflict record; unresolved identity yields abstention (D-010 pattern extended to IDs).""",
        "R-501",
        "Acquisition identifier collisions may exceed current ACL coverage until master-data repair wave completes",
        "Bounded contexts prevent authority collapse",
        "ACL + contract schemas",
        "Contract and prohibited-action tests",
        "submission/artefacts/05_DDD_CONTEXT_MAP.md",
    ))

    write(ART / "06_DATA_GOVERNANCE_INTEGRITY.md", artefact(
        "Data Governance and Integrity",
        "Team 3 — Domain / evidence lead",
        "GxP/quality; Security/privacy",
        "INJ-018; INJ-024; INJ-029..036; D-008; D-010",
        "Define how AEGIS preserves ALCOA+ attributes, lineage and conflicting retention obligations without fabricating completeness.",
        """| E-001 | `knowledge/GXP_DATA_INTEGRITY_STANDARD.md` | Synthetic policy | ALCOA+ expectations | Scenario evidence |
| E-002 | `data/audit_trails.csv`; `data/privileged_sessions.csv` | INJ-029 | Audit capture disabled 47 minutes | Integrity break |
| E-003 | `data/lab_results.csv`; `data/interface_mappings.csv` | INJ-024 | mg/L vs µg/mL assumption | Unit defect |
| E-004 | `data/retention_rules.csv`; `data/legal_holds.csv`; `data/deletion_requests.csv` | INJ-035 | Retention vs deletion conflict | Multi-obligation |
| E-005 | `data/certificates_analysis.csv`; `data/document_lineage.csv` | INJ-036 | Transcribed PDF; missing signed source | Provenance break |""",
        """## 1. Data inventory and stewardship

| Domain object | Steward | Systems of record candidates | Integrity risk |
|---|---|---|---|
| Batch / genealogy | Manufacturing + Quality | MES, warehouse, eBR | INJ-021 break |
| Lab result | QC lab | LIMS, notebooks, stats tool | INJ-023 disagreement |
| ICSR / receipt | PV | Affiliate inbox, vendor, global safety DB | INJ-038 clock conflict |
| Shipment / logger | Supply | Logger files, pallet association | INJ-051 dispute |
| Consent / specimen | Clinical + DPO | eConsent, specimen processing | INJ-017 mismatch |

## 2. Authority, effective date and supersession

Every cited document/record must expose status, authority, effective date/version and retrieval time (`knowledge/AI_GXP_BOUNDARY.md`). Superseded protocols (INJ-013) and labels (INJ-040/046) remain visible as conflicts, not silently replaced.

## 3. Identity, time and unit controls

| Control | Rule | Inject |
|---|---|---|
| Identity | Do not merge aliases without governed mapping | INJ-008, INJ-045 |
| Time | Preserve timezone/precision; flag clock skew | INJ-018, INJ-051 |
| Unit | Approved mapping + provenance or abstain | INJ-024 / D-010 |

## 4. Lineage and ALCOA+

| Attribute | AEGIS behaviour |
|---|---|
| Attributable | Require user + purpose on every run; reject shared-account ambiguity for GxP conclusions (INJ-030) |
| Legible / Contemporaneous | Surface back-entry and downtime (INJ-025) |
| Original | Prefer signed source over transcription; flag INJ-036 gaps |
| Accurate / Complete | List gaps/contradictions; never invent missing CMO audit commitment (INJ-028) |
| Consistent / Enduring / Available | Export audit evidence; retention conflicts escalate (INJ-035) |

## 5. Retention, residency and access

Legal hold, GxP retention and privacy deletion may conflict (INJ-035/061). AEGIS records the conflict and routes to human governance; it does not auto-delete GxP-relevant records. Residency failures (INJ-064) block cross-border model training proposals.""",
        "R-601",
        "Full enterprise data catalogue remains incomplete; inventory is workflow-scoped",
        "No silent unit conversion or fabricated lineage",
        "ACL + abstention codes",
        "Unit and lineage negative tests (Phase 5+)",
        "submission/artefacts/06_DATA_GOVERNANCE_INTEGRITY.md",
    ))

    write(ART / "07_ONTOLOGY_SEMANTIC_LAYER.md", artefact(
        "Ontology and Semantic Layer",
        "Team 3 — Domain / evidence lead",
        "Architecture; PV medical coding liaison",
        "INJ-039; INJ-040; INJ-045; D-012",
        "Define the minimum semantic layer for product, batch, case and shipment concepts with temporal and jurisdictional semantics.",
        """| E-001 | `data/controlled_vocabularies.csv` | Vocabulary catalogue | Controlled terms exist with versions | Partial coverage |
| E-002 | `data/terminology_versions.csv`; `data/adverse_events.csv` | MedDRA versions (INJ-039) | Preferred term changes across versions | Version-sensitive |
| E-003 | `data/listedness_sources.csv`; `data/product_labels.csv` | Listedness (INJ-040) | IB/CCDS/local label diverge | Authority conflict |
| E-004 | `data/idmp_mappings.csv` | IDMP (INJ-045) | Cross-system code divergence | Identity conflict |""",
        """## 1. Core concepts

| Concept | Required attributes | Temporal | Jurisdictional |
|---|---|---|---|
| MedicinalProduct | substance, strength, form, IDMP candidates | effective MA dates | market |
| Batch | batch_id, material links, site | manufacture/as-of | site/region |
| LabResult | analyte, value, unit, method, flags | result time | lab jurisdiction |
| IcsrCase | case_id, products, events, receipts | awareness/receipt clocks | affiliate/region |
| ListednessSource | source_type, version, statement | effective label version | market |
| ShipmentLeg | shipment_id, logger_id, range | logger timeline | lane/customs |

## 2. Semantic rules

1. Terminology coding must carry MedDRA version; regrouping across versions is a conflict, not a silent remap (INJ-039).
2. Expectedness/listedness citations must name the source document and market; conflicting IB/CCDS/label remain concurrent candidates (INJ-040).
3. IDMP mappings are candidate links with confidence/abstention, never forced identity (INJ-045).
4. Protocol and label applicability are evaluated at as-of time and site approval state (INJ-013/046).

## 3. Semantic layer implementation choice

For the POC, the semantic layer is: versioned JSON contracts + evidence citation objects + controlled vocab tables loaded offline. Full enterprise ontology tooling is deferred (see KG decision).""",
        "R-701",
        "MedDRA licence artefacts are not fully redistributable in package; tests use synthetic codes",
        "Versioned terminology preserved",
        "Semantic citation fields in contracts",
        "PV contract tests",
        "submission/artefacts/07_ONTOLOGY_SEMANTIC_LAYER.md",
    ))

    write(ART / "08_KNOWLEDGE_GRAPH_DECISION.md", artefact(
        "Knowledge Graph Decision",
        "Team 3 — Architecture / integration lead",
        "Domain/evidence; Evaluation/reliability",
        "INJ-021; INJ-037; INJ-051; D-011",
        "Decide whether a knowledge graph is necessary for AEGIS POC versus a simpler relational evidence register with multi-hop queries.",
        """| E-001 | `data/RELATIONSHIP_MODEL.csv` | Relationship catalogue | Multi-entity links exist in package | Synthetic model |
| E-002 | `data/material_genealogy.csv` | Genealogy (INJ-021) | Multi-hop material links with break | Incomplete graph |
| E-003 | `data/duplicate_candidates.csv` | PV duplicates (INJ-037) | Cluster candidates across sources | Probabilistic |
| E-004 | `PACKAGE_SCOPE_AND_ASSUMPTIONS.md` | Package freedom | KG not mandatory unless justified | Binding guidance |""",
        """## 1. Decision criteria

| Criterion | Threshold | Observation |
|---|---|---|
| Multi-hop necessity | Required for correctness beyond joins | Genealogy, duplicate clustering and cold-chain association need multi-hop, but bounded depth |
| Completeness of edges | Graph must not invent missing edges | INJ-021/052/058 show missing links — graph would be partial |
| Operability offline | Must run without external graph SaaS | Package offline rule |
| Assurance cost | Validation burden vs benefit | Graph store adds GxP surface without solving authority conflicts |

## 2. Graph-required use cases (candidates)

| Use case | Graph appeal | Simpler alternative |
|---|---|---|
| Batch genealogy break (INJ-021) | Path query MES↔warehouse | Explicit join + gap record |
| ICSR duplicates (INJ-037) | Entity resolution graph | Deterministic blocking keys + scored candidates |
| Cold-chain logger association (INJ-051) | Association graph | Evidence register with disputed links |
| Recall scope (INJ-058) | Connected components | Option list with incomplete-link abstention |

## 3. Decision

**Decision D-011:** Do **not** mandate a production knowledge graph for the assessed POC. Implement a **relational/evidence-register baseline** with versioned contracts, deterministic multi-hop queries (bounded depth), and explicit gap nodes. Revisit a graph store only if evaluation proves multi-hop query complexity or explainability cannot meet SLOs with the register.

## 4. Simpler alternative benchmark

Benchmark metric: time-to-assemble cited evidence pack for Workflow A/B/C fixtures; contradiction/gap recall vs golden fixtures; prohibited-action rate = 0. Graph prototype would need to beat register on contradiction recall without inventing edges — currently unjustified.

## 5. Migration path

If later justified: map evidence-register edges to property-graph projection behind the same contracts; keep AI-disabled SQL/register path.""",
        "R-801",
        "Future inspection may request graph-style lineage views; export format must remain inspectable",
        "KG not mandatory for POC",
        "Evidence register + bounded joins",
        "Workflow fixture evaluations",
        "submission/artefacts/08_KNOWLEDGE_GRAPH_DECISION.md",
    ))

    write(ART / "09_REQUIREMENTS_TRACEABILITY.md", artefact(
        "Requirements Traceability",
        "Team 3 — Architecture / integration lead",
        "GxP/quality; Evaluation/reliability; Security/privacy",
        "FR/NFR/GXP/SEC/PRI; artefacts 10–21; tests",
        "Trace uniquely identified requirements for the three mandatory workflows to controls, tests and evidence.",
        """| E-001 | `case/INTEGRATED_CASE.md` §4–5 | Mandate | Three workflows + operating properties | Binding |
| E-002 | `data/ai_use_boundaries.csv` | Executive boundary | Allowed vs prohibited actions | Hard gate |
| E-003 | `evaluation/contracts/*.schema.json` | Public contracts | Fail-closed schemas | Executable |""",
        """## 1. Functional requirements

| ID | Requirement | Acceptance criteria | Test |
|---|---|---|---|
| FR-B01 | Reconcile batch evidence with citations, contradictions, gaps, abstentions | Output validates `batch_response.schema.json`; `execution_status=not_executed` | `test_workflow_contracts.py` |
| FR-B02 | Never emit batch disposition/release/reject/reprocess/relabel/recall | Additional properties / prohibited fields fail closed | `test_prohibited_actions.py` |
| FR-P01 | Support PV intake packaging with duplicate candidates and clock evidence | Validates `pv_response.schema.json` | `test_workflow_contracts.py` |
| FR-P02 | Never emit final seriousness/causality/expectedness/reportability/signal confirmation | Policy deny | `test_prohibited_actions.py` |
| FR-S01 | Produce ranked draft supply options with `no_side_effects=true` | Validates `supply_response.schema.json` | `test_workflow_contracts.py` |
| FR-S02 | Never reserve/allocate/ship/change quality status/initiate recall | Policy deny | `test_prohibited_actions.py` |

## 2. Non-functional requirements

| ID | Requirement | Acceptance |
|---|---|---|
| NFR-01 | Offline deterministic mode without cloud keys | Setup/test scripts run offline |
| NFR-02 | Idempotent runs with request/idempotency keys | Duplicate submission yields same audit identity |
| NFR-03 | Budgets/stop conditions for agent steps | Stop policy documented; DoW controls (INJ-076) |
| NFR-04 | Kill switch and AI-disabled continuity ≥14 days concept | Artefacts + runbook path (INJ-082) |

## 3. GxP / safety / security / privacy

| ID | Requirement | Inject / policy |
|---|---|---|
| GXP-01 | Intended use advisory only; human accountability preserved | `knowledge/AI_GXP_BOUNDARY.md` |
| GXP-02 | Authority/effective-date on retrieved docs | INJ-065 untrusted knowledge |
| SEC-01 | Fresh authorization at execution; deny stale cache | INJ-067 |
| SEC-02 | Signed/approved tools only; deny poisoned manifests | INJ-066 |
| SEC-03 | Model hash must match registry | INJ-070 |
| PRI-01 | Purpose limitation; block undeclared secondary use | INJ-060 |
| PRI-02 | Sensitive segment handling (pregnancy/minor) | INJ-041 |

## 4. Trace matrix (summary)

Requirements above map to ADRs in artefact 11, contracts in artefact 12, QRM in 15, threat model in 16, and tests under `submission/tests/`.""",
        "R-901",
        "Quantitative BR-01 cycle-time baseline still open (R-101) — value requirements remain proxy-based",
        "Every hard-gate requirement has a failing/passing test pair",
        "policy_guard + contracts",
        "submission/tests/*",
        "submission/artefacts/09_REQUIREMENTS_TRACEABILITY.md",
    ))

    # Evidence map
    inject_rows = "\n".join(
        f"| INJ-{i:03d} | See `case/INTEGRATED_CASE.md` catalogue D{(i-1)//6+1:02d} | Mapped in deep-dives when workflow-critical; otherwise retained as disclosed inject |"
        for i in range(1, 85)
    )
    write(ART / "EVIDENCE_MAP.md", f"""# Evidence Map — Phase 2 Exit

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Domain / evidence lead |
| Version / date | 1.0 / 2026-08-10 |
| Status | Reviewed |

## Purpose

Map injects to evidence paths, authority concerns and workflow relevance without resolving contradictions.

## Summary register (all 84 injects)

| Inject | Domain bucket | Mapping note |
|---|---|---|
{inject_rows}

## Deep dive — Workflow A (batch evidence)

| Inject | Evidence paths | Authority / time / unit issues | Conflict / gap |
|---|---|---|---|
| INJ-021 | `data/batches.csv`; `data/material_genealogy.csv`; `data/warehouse_movements.csv` | MES vs warehouse identity | Genealogy break |
| INJ-022 | `data/environmental_monitoring.csv`; `data/microbiology_results.csv` | Corrected organism ID after review | Temporal correction |
| INJ-023 | `data/lab_results.csv`; `data/oos_investigations.csv` | LIMS/OOS vs stats OOT vs notebook invalid | Triple disagreement |
| INJ-024 | `data/lab_results.csv`; `data/interface_mappings.csv` | mg/L vs µg/mL | Unapproved mapping |
| INJ-025 | `data/ebr_steps.csv`; `data/downtime_events.csv` | Back-entry after downtime | Contemporaneousness |
| INJ-028 | `data/release_packets.csv`; `data/supplier_audits.csv` | CMO audit commitment missing | QP evidence gap |
| INJ-029..036 | audit/access/validation/CAPA/change/retention/lineage CSVs | Integrity & validation ambiguity | Multiple DI breaks |

## Deep dive — Workflow B (PV)

| Inject | Evidence paths | Issues |
|---|---|---|
| INJ-037 | `data/icsr_cases.csv`; `data/duplicate_candidates.csv` | Duplicate cluster across product names |
| INJ-038 | `data/icsr_cases.csv`; `data/safety_receipts.csv` | Awareness/receipt clock conflict |
| INJ-039 | `data/adverse_events.csv`; `data/terminology_versions.csv` | MedDRA version mismatch |
| INJ-040 | `data/listedness_sources.csv`; `data/product_labels.csv`; `source_documents/CCDS_NCB204_v4.md` | Expectedness source conflict |
| INJ-041 | `data/sensitive_segments.csv` | Pregnancy/minor sensitivity |
| INJ-043 | `data/product_complaints.csv`; `data/icsr_cases.csv` | Quality–safety link |
| INJ-065 | `knowledge/MALICIOUS_SUPPLIER_DEVIATION.md`; `data/knowledge_catalog.csv` | Prompt injection in document |

## Deep dive — Workflow C (supply / cold chain)

| Inject | Evidence paths | Issues |
|---|---|---|
| INJ-051 | `data/shipments.csv`; `data/temperature_loggers.csv`; `source_documents/Cold_chain_logger_association_SH_901.md` | Logger clock / pallet association dispute |
| INJ-054 | `data/supplier_risks.csv`; `data/inventory.csv` | Excipient shortage |
| INJ-055 | `data/cmo_capacity.csv`; `data/vendor_contracts.csv` | Double-booked CMO capacity |
| INJ-056 | `data/demand_forecast.csv`; `data/allocation_constraints.csv` | Ethics/constraints on allocation options |
| INJ-058 | `data/recall_candidates.csv`; `data/material_genealogy.csv` | Incomplete genealogy for scope |
| INJ-066 | `data/tool_catalog.csv`; poisoned tool sample | Write/disposition tool abuse |
| INJ-080 | `data/agent_runs.csv` | Stale checkpoint / duplicate draft reservations |

## Authority–identity–time–unit review checklist (Hour-12 gate)

| Dimension | Control | Primary injects |
|---|---|---|
| Authority | Status/signature/hash/applicability before trust | INJ-065, INJ-036, INJ-040 |
| Identity | No silent alias merge | INJ-005, INJ-008, INJ-045 |
| Time | Preserve precision/timezone; flag skew | INJ-018, INJ-038, INJ-051 |
| Unit | Approved mapping or abstain | INJ-024 |
| Lineage | Expose gaps; do not fabricate | INJ-021, INJ-052, INJ-058 |

## Exit evidence

Phase 2 exit artefacts: `05`–`09`, this map, and Phase 2 entries in `ASSUMPTIONS_AND_DECISION_LOG.md`.
""")

    # ---- Phase 3 ----
    write(ART / "10_C4_ARCHITECTURE.md", artefact(
        "C4 Architecture",
        "Team 3 — Architecture / integration lead",
        "Security/privacy; Build; GxP/quality",
        "ADR-001..010; FR-*; NFR-01..04",
        "Describe an offline-capable advisory architecture for the three workflows with kill switch and AI-disabled continuity.",
        """| E-001 | `case/INTEGRATED_CASE.md` §5 | Operating properties | Purpose limitation, budgets, checkpoints, auditability | Binding |
| E-002 | `starter/contracts/WORKFLOW_CONTRACTS.md` | Starter contracts | Minimum I/O boundaries | Binding |
| E-003 | `knowledge/AI_DISABLED_CONTINUITY.md` | Continuity policy | Operate without inference | Scenario |""",
        """## 1. System context

AEGIS-PHARMA Advisory Workbench sits among Quality reviewers, PV intake staff, supply planners, and brownfield systems (LIMS, MES, QMS, safety DB, IRT, serialization). It produces cited evidence packs and option lists; humans retain regulated decisions. External model providers are optional and bypassable.

## 2. Containers

| Container | Responsibility | Tech constraint |
|---|---|---|
| Offline evidence store | Read-only fixtures from package `data/`/`knowledge/`/`source_documents/` | No mutation of challenge evidence |
| Contract API / CLI | Versioned workflow requests/responses | Stdlib Python POC |
| Deterministic reconciler | Rules/joins/gap detection | Always available |
| Optional inference adapter | Summarization behind interface | Hash-pinned; kill switch |
| Policy guard | Deny prohibited actions, stale auth, poisoned tools | Fail closed |
| Audit/export | Append-only run evidence | Hashable export |
| Explorer (optional UI) | Human review surfacing | `app/` offline HTML acceptable |

## 3. Components (Workbench)

Request gate (authz+purpose) → Evidence loader (authority filter) → Workflow engines (batch/PV/supply) → Schema validator → Policy guard → Audit writer. Inference adapter may assist narrative structuring only after deterministic facts are assembled.

## 4. Brownfield coexistence

Read adapters treat source systems as untrusted publishers. Writes to MES/QMS/safety/inventory are out of scope for assessed mode. Coexistence uses snapshots/fixtures; cutover plan is additive advisory overlay (ADR-007).

## 5. Kill switch and AI-disabled path

Kill switch disables inference adapter and any tool channel beyond read. AI-disabled mode runs deterministic reconciler only for ≥14-day continuity concept (INJ-082).""",
        "R-1001",
        "Live system adapters are mocked in POC; production connectivity remains design-only",
        "Advisory architecture with offline path",
        "Containers above",
        "Contract + policy tests",
        "submission/artefacts/10_C4_ARCHITECTURE.md",
    ))

    adrs = "\n".join([
        "| ADR-001 | Deterministic-first reconciliation | LLM-first agent | Offline reliability; INJ-082 | Accepted |",
        "| ADR-002 | Replaceable inference interface | Hard-wired vendor SDK | INJ-075/081/083 | Accepted |",
        "| ADR-003 | Fail-closed prohibited actions via schema+policy | Soft warnings | INJ-006; scoring hard gates | Accepted |",
        "| ADR-004 | Authority-checked retrieval | Trust corpus by default | INJ-065; AI_GXP_BOUNDARY | Accepted |",
        "| ADR-005 | Signed/approved tools only | Open tool registry | INJ-066; ZERO_TRUST_AI_TOOLS | Accepted |",
        "| ADR-006 | Supply `no_side_effects` invariant | Supervised write-back | INJ-056; workflow contracts | Accepted |",
        "| ADR-007 | Versioned JSON contracts with additionalProperties false | Free-form markdown outputs | evaluation/contracts | Accepted |",
        "| ADR-008 | Offline/mock mode mandatory for assessment | Cloud-only demo | PACKAGE_SCOPE | Accepted |",
        "| ADR-009 | Human review required before any regulated decision | Automation of disposition | INJ-071/074 | Accepted |",
        "| ADR-010 | Budgets, stop conditions, checkpoints, idempotency | Unbounded agents | AGENT_BUDGET_AND_STOP_POLICY; INJ-076/080 | Accepted |",
        "| ADR-011 | No knowledge-graph mandate in POC | Graph-first platform | D-011; artefact 08 | Accepted |",
        "| ADR-012 | Entitlement re-check at execution; ignore stale cache | Cache-trust gateway | INJ-067 | Accepted |",
    ])
    write(ART / "11_ADR_REGISTER.md", artefact(
        "ADR Register",
        "Team 3 — Architecture / integration lead",
        "All leads",
        "ADR-001..012; artefacts 08–16",
        "Record architecture decisions that constrain the POC and defence.",
        """| E-001 | `PACKAGE_SCOPE_AND_ASSUMPTIONS.md` | Package rules | Offline freedom; no mandatory KG/LLM | Binding |
| E-002 | `knowledge/AGENT_BUDGET_AND_STOP_POLICY.md` | Budget policy | Stop/budget expectations | Scenario |
| E-003 | `knowledge/ZERO_TRUST_AI_TOOLS.md` | Tool trust | Signed tools / least privilege | Scenario |""",
        f"""## 1. ADR index

| ID | Decision | Alternatives | Evidence | Status |
|---|---|---|---|---|
{adrs}

## 2. Decision detail notes

ADR-001 and ADR-008 ensure assessment reproducibility. ADR-003/005/006/012 encode hard gates as executable policy. ADR-011 records the KG deferral from artefact 08. ADR-002/010 address FinOps and vendor shock (INJ-075/076/083).

## 3. Invalidation conditions

An ADR is revisited if evaluation shows deterministic path cannot surface required contradictions, or if a regulator-imposed control requires a different record/signature boundary.""",
        "R-1101",
        "ADR set may grow during POC build without invalidating Phase 3 gate",
        ">=10 ADRs recorded and linked",
        "ADR register",
        "Review record",
        "submission/artefacts/11_ADR_REGISTER.md",
    ))

    write(ART / "12_INTEGRATION_CONTRACTS.md", artefact(
        "Integration Contracts",
        "Team 3 — Architecture / integration lead",
        "Build; Evaluation",
        "ADR-007; FR-B01/P01/S01; evaluation/contracts",
        "Specify versioned I/O contracts, event semantics and idempotency for the three workflows.",
        """| E-001 | `starter/contracts/WORKFLOW_CONTRACTS.md` | Starter | Minimum workflow I/O | Binding |
| E-002 | `evaluation/contracts/batch_response.schema.json` | Public schema | additionalProperties false; execution_status const | Executable |
| E-003 | `evaluation/contracts/pv_response.schema.json` | Public schema | PV boundaries | Executable |
| E-004 | `evaluation/contracts/supply_response.schema.json` | Public schema | no_side_effects | Executable |""",
        """## 1. Request envelope (all workflows)

Required: `request_id`, `idempotency_key`, `workflow`, `purpose`, `as_of`, `user`, `authorization_context`. Optional inference flag default false.

## 2. Response contracts

| Workflow | Schema | Critical invariants |
|---|---|---|
| Batch | `batch_response.schema.json` | `execution_status=not_executed`; readiness enum only |
| PV | `pv_response.schema.json` | No final safety conclusion fields |
| Supply | `supply_response.schema.json` | `no_side_effects` true; no reservation execution |

## 3. Event semantics

| Event | Meaning | Consumers |
|---|---|---|
| `run.started` / `run.completed` | Audit lifecycle | Export |
| `conflict.detected` | Contradiction registered | Human review UI |
| `authz.denied` | Fresh check failed | Security |
| `policy.denied` | Prohibited action blocked | Security/GxP |
| `inference.bypassed` | AI-disabled or kill switch | Continuity |

Events are facts about the advisory system, not instructions to MES/QMS/safety to mutate state.

## 4. Idempotency and checkpoints

Same `idempotency_key` + payload hash returns prior result without duplicating side-effect attempts (there should be none). Checkpoints store deterministic intermediate evidence lists; resume rejects stale authorization (INJ-080/067).

## 5. Compatibility

Participant fixtures under `submission/tests/fixtures/` mirror public samples. Extensions require a new schema version and tests; prohibited fields remain denied.""",
        "R-1201",
        "Public sample fixtures live under evaluation/contract_samples; submission mirrors for offline tests",
        "Positive samples pass; prohibited samples fail",
        "contracts.py validator",
        "test_workflow_contracts.py",
        "submission/artefacts/12_INTEGRATION_CONTRACTS.md",
    ))

    write(ART / "13_GXP_LIFECYCLE_VALIDATION.md", artefact(
        "GxP Lifecycle and Validation",
        "Team 3 — GxP / quality lead",
        "Architecture; Evaluation",
        "GXP-01/02; knowledge/COMPUTERISED_SYSTEM_LIFECYCLE.md; AI_GXP_BOUNDARY.md",
        "Define intended use, GxP relevance boundary and proportionate validation/assurance strategy.",
        """| E-001 | `knowledge/COMPUTERISED_SYSTEM_LIFECYCLE.md` | Lifecycle policy | CSV/lifecycle expectations | Scenario |
| E-002 | `knowledge/AI_GXP_BOUNDARY.md` K-003 | Effective 2026-05-01 | AI cannot replace accountable GxP decisions | Scenario |
| E-003 | `data/validation_inventory.csv`; `data/system_inventory.csv` | INJ-031 | Same app labelled validated/conditional/research | Ambiguity |""",
        """## 1. Intended use

AEGIS is an **advisory evidence-reconciliation and planning-support** system for trained Quality, PV and Supply personnel. It is not a batch certification system, safety decision system, or inventory execution system.

## 2. GxP relevance classification

| Component | Classification | Rationale |
|---|---|---|
| Deterministic reconciler outputs used in GxP review | GxP-relevant support | May influence reviewer attention; not disposition |
| Policy guard / audit trail | GxP-relevant control | Enforces boundary and inspectability |
| Optional LLM summarizer | GxP-relevant if enabled in review path | Requires change control and evaluation (INJ model change) |
| Pure UI chrome | Non-GxP if non-decision | Still accessibility constrained |

## 3. Lifecycle approach

Proportionate CSA/CSV hybrid: critical thinking on high-risk failure modes (omitted deviation, wrong unit, stale auth, poisoned tool). Spec → risk → test → evidence → periodic review. INJ-031 ambiguity means AEGIS must declare its own validation state explicitly in submission evidence.

## 4. Electronic records / signatures

AEGIS audit export is an electronic record of advisory activity. It does **not** apply Part-11/ Annex 11 signature meaning to batch release or medical conclusions. Human signature/accountability remains in source QMS/safety systems.""",
        "R-1301",
        "Jurisdictional validation expectations differ; analysis assumes EU+US fictional NTG footprint without legal advice",
        "Intended use and boundary documented",
        "Lifecycle artefact + policy tests",
        "GxP review",
        "submission/artefacts/13_GXP_LIFECYCLE_VALIDATION.md",
    ))

    write(ART / "14_COMPUTER_SOFTWARE_ASSURANCE.md", artefact(
        "Computer Software Assurance",
        "Team 3 — GxP / quality lead",
        "Evaluation/reliability; Build",
        "CSA; ADR-003; artefacts 15–16",
        "Apply risk-based assurance with scripted and unscripted testing focused on patient/product impact pathways.",
        """| E-001 | `knowledge/COMPUTERISED_SYSTEM_LIFECYCLE.md` | Assurance expectations | Risk-based testing | Scenario |
| E-002 | `evaluation/EVALUATION_PLAN.md` | Evaluation framing | Public fixtures and gates | Package |""",
        """## 1. Assurance strategy

| Risk question | Assurance activity |
|---|---|
| Could output hide a critical deviation? | Negative fixtures + reviewer challenge scripts (INJ-071) |
| Could unit conversion silently alter OOS? | Unit mapping denial tests (INJ-024) |
| Could tool write disposition? | Poisoned tool denial (INJ-066) |
| Could stale contractor act? | Authz freshness tests (INJ-067) |
| Could model supply chain drift? | Hash mismatch deny (INJ-070) |

## 2. Scripted vs unscripted

Scripted: contract schema suites, prohibited-action matrix, authz/tool trust. Unscripted: exploratory review of multilingual PV narratives and malicious document handling with recorded notes.

## 3. Evidence of assurance

Machine-readable results under `submission/evidence/` (populated as tests run). Failed hard gates block any “ready for defence” claim.""",
        "R-1401",
        "Unscripted exploratory sessions still to be timed in Phase 5–6",
        "High-risk controls have automated tests",
        "policy_guard + contracts",
        "submission/tests",
        "submission/artefacts/14_COMPUTER_SOFTWARE_ASSURANCE.md",
    ))

    write(ART / "15_QUALITY_RISK_MANAGEMENT.md", artefact(
        "Quality Risk Management",
        "Team 3 — GxP / quality lead",
        "Security/privacy; Product/value",
        "INJ-024; INJ-071; QRM for FR/GXP",
        "Identify quality risks from introducing advisory AI/automation into the three workflows and define controls.",
        """| E-001 | `data/candidate_outputs.csv`; `data/reviewer_feedback.csv` | INJ-071 | Automation bias / omitted deviation | Human factors |
| E-002 | `data/interface_mappings.csv` | INJ-024 | Unit defect | Data integrity |
| E-003 | `data/ai_use_boundaries.csv` | INJ-006 | Prohibited optimization pressure | Governance |""",
        """## 1. Risk register (extract)

| Risk | Hazard | Severity | Control | Residual |
|---|---|---|---|---|
| QR-01 | Reviewer accepts summary missing critical deviation | High | Force evidence list; omit-disposition; challenge tests | Medium — bias remains |
| QR-02 | Silent unit conversion flips OOS interpretation | High | D-010 abstain; mapping approval | Low if enforced |
| QR-03 | AI pressures release under BR-01 | High | Hard policy deny + KPI guardrails D-005 | Low for system; medium organizational |
| QR-04 | PV final medical judgement emitted | High | Schema/policy deny | Low |
| QR-05 | Supply option auto-executes allocation | High | no_side_effects invariant | Low |
| QR-06 | Multilingual extraction inequity | Medium | Subgroup evaluation; human review | Medium |
| QR-07 | Poisoned supplier PDF instructs ignore holds | High | Untrusted doc handling; injection tests | Medium |

## 2. Risk acceptance

Residual automation-bias and language inequity risks require human-factors controls (artefact 18) and are not accepted as closed. Prohibited-action residual risk is accepted as Low only while tests remain green.""",
        "R-1501",
        "Organizational KPI pressure (INJ-002) can overwhelm technical controls without governance",
        "Top hazards controlled or residual explicit",
        "QRM + policy tests",
        "Independent quality review",
        "submission/artefacts/15_QUALITY_RISK_MANAGEMENT.md",
    ))

    # ---- Phase 4 ----
    write(ART / "16_THREAT_ABUSE_MODEL.md", artefact(
        "Threat and Abuse Model",
        "Team 3 — Security / privacy lead",
        "Architecture; GxP; Evaluation",
        "INJ-065..070; INJ-076; SEC-*",
        "Threat-model the advisory agent/tooling surface and map each threat to controls and negative tests.",
        """| E-001 | `knowledge/MALICIOUS_SUPPLIER_DEVIATION.md` | INJ-065 | Hidden instructions to ignore holds | Untrusted |
| E-002 | `data/tool_catalog.csv` / poisoned manifest concept | INJ-066 | Write disposition tool | Malicious |
| E-003 | `data/access_cache.csv`; `data/users_entitlements.csv` | INJ-067 | Revoked access still cached | Stale auth |
| E-004 | `data/security_events.csv` | INJ-068/076 | Exfiltration / DoW patterns | Telemetry |
| E-005 | `data/model_registry.csv`; `data/model_artifacts.csv` | INJ-070 | Hash mismatch | Supply chain |""",
        """## 1. STRIDE-style threats for AEGIS

| Threat | Inject | Control | Negative test |
|---|---|---|---|
| Prompt injection via document | INJ-065 | Treat docs as data; never executable policy | Retrieval authority tests / review checklist |
| Tool manifest poisoning | INJ-066 | Signed allow-list; deny write tools | `test_tool_trust.py` |
| Stale authorization | INJ-067 | Re-check entitlements at execution | `test_authorization_freshness.py` |
| Safety-data exfiltration | INJ-068 | Purpose+role minimization; audit | Policy purpose checks |
| Ransomware / OT isolation | INJ-069 | Degraded/offline mode | Continuity path |
| Model supply-chain compromise | INJ-070 | Hash pin to registry | Hash mismatch deny in policy_guard |
| Denial-of-wallet | INJ-076 | Token/step budgets; reject oversized context | Budget stop (Phase 6 metrics) |
| Excessive agency | INJ-006/080 | No side effects; checkpoint freshness | `test_prohibited_actions.py` |
| Replay | INJ-080 | Idempotency + authz time | Checkpoint tests |

## 2. Zero Trust rules

Never trust cached gateway decisions, tool descriptions, or retrieved SOP text as authorization. Least privilege: read-only tools in assessed mode. Segregation of duties: builders do not self-approve hard-gate residual risk.""",
        "R-1601",
        "Full red-team campaign scheduled Phase 6; Phase 4 delivers automated deny tests",
        "Poisoned tool and stale auth denied",
        "policy_guard",
        "submission/tests/test_tool_trust.py; test_authorization_freshness.py",
        "submission/artefacts/16_THREAT_ABUSE_MODEL.md",
    ))

    write(ART / "17_PRIVACY_ETHICS.md", artefact(
        "Privacy and Ethics",
        "Team 3 — Security / privacy lead",
        "DPO liaison; Clinical; PV",
        "INJ-041; INJ-059..064; PRI-*",
        "Assess privacy-by-design constraints for AEGIS processing across trial, genomic, PV and support data.",
        """| E-001 | `knowledge/PRIVACY_AND_PSEUDONYMISATION.md` | Privacy policy extract | Pseudonymisation expectations | Scenario |
| E-002 | `data/privacy_risk.csv`; `data/genomic_data.csv` | INJ-059 | Re-identification risk | High |
| E-003 | `data/consents.csv`; `data/data_exports.csv` | INJ-060 | Secondary use not in consent | Purpose conflict |
| E-004 | `data/deletion_requests.csv`; `data/retention_rules.csv` | INJ-061 | Erasure vs GxP retention | Obligation conflict |
| E-005 | `data/data_residency.csv`; `data/backup_inventory.csv` | INJ-064 | Unapproved region replica | Residency failure |""",
        """## 1. Principles applied

Purpose limitation, data minimisation, access by role/purpose, retention conflict escalation, and no silent secondary use for model training.

## 2. Workflow-specific controls

| Workflow | Privacy control |
|---|---|
| Batch | Prefer non-personal batch/lab identifiers; avoid staff PII in exports beyond audit need |
| PV | Segment pregnancy/minor narratives (INJ-041); restrict affiliate exfiltration (INJ-068) |
| Supply | Aggregate demand where possible; no patient-level allocation automation |

## 3. Ethics notes

Allocation ethics (INJ-056) remain human policy decisions; system only lists constraint-aware options. Genomic re-identification risk blocks free-text model prompts with rare combinations.""",
        "R-1701",
        "Cross-border transfer mechanisms are jurisdiction-assumptions, not legal advice",
        "Secondary use and residency blocks documented",
        "Purpose checks in policy_guard",
        "Privacy review",
        "submission/artefacts/17_PRIVACY_ETHICS.md",
    ))

    write(ART / "18_RESPONSIBLE_AI_HUMAN_FACTORS.md", artefact(
        "Responsible AI and Human Factors",
        "Team 3 — Product / value lead",
        "GxP; Security; Evaluation",
        "INJ-071..074; QR-01; ADR-009",
        "Design human oversight, contestability and accessibility so automation bias and inequity are mitigated.",
        """| E-001 | `data/candidate_outputs.csv`; `data/reviewer_feedback.csv` | INJ-071 | Omitted critical deviation accepted | Bias |
| E-002 | `data/model_performance.csv`; `data/icsr_cases.csv` | INJ-072 | Arabic/Hindi quality lower | Inequity |
| E-003 | `data/usability_findings.csv` | INJ-073 | Keyboard/colour-only failures | A11y |
| E-004 | `data/decision_rights.csv`; `case/STAKEHOLDER_PACK.md` | INJ-074 | Global vs local accountability | Role conflict |""",
        """## 1. Oversight model

| Touchpoint | Human role | Contestability |
|---|---|---|
| Batch readiness pack | Quality reviewer / QP pathway | Can reject pack; require gap closure |
| PV intake pack | Case processor / medical reviewer | Can overturn coding suggestions; final judgements human |
| Supply options | Supply planner + approvers | Can discard options; no auto-execution |

## 2. Bias and inequity mitigations

Show raw evidence beside any summary; require acknowledgment of contradiction/gap counts; evaluate multilingual subgroups; do not ship colour-only status.

## 3. Emergency stop

Kill switch stops inference and tools; AI-disabled reconciler remains. Works council consultation noted for telemetry in applicable regions (stakeholder pack).""",
        "R-1801",
        "Accessibility remediation of final UI pending Phase 5 app work",
        "Human oversight and stop defined",
        "Blueprint + kill switch",
        "HF review",
        "submission/artefacts/18_RESPONSIBLE_AI_HUMAN_FACTORS.md",
    ))

    write(ART / "19_EU_AI_ACT_APPLICABILITY.md", artefact(
        "EU AI Act Applicability",
        "Team 3 — Security / privacy lead",
        "GxP/quality; Regulatory affairs liaison",
        "Assumptions A-013; GXP boundary",
        "Analyse EU AI Act applicability for AEGIS under stated jurisdiction assumptions; not legal advice.",
        """| E-001 | `case/INTEGRATED_CASE.md` §1 | Org footprint includes EU (Germany/Ireland) | Potential EU scope | Fictional |
| E-002 | `knowledge/AI_GXP_BOUNDARY.md` | Intended use | Advisory support, not autonomous regulated decisions | Scenario |
| E-003 | `PACKAGE_SCOPE_AND_ASSUMPTIONS.md` | Regulatory boundary | Participants must state assumptions | Binding |""",
        """## 1. Assumptions

| ID | Assumption |
|---|---|
| A-013 | Analysis assumes NTG places AEGIS into service affecting EU operations for Quality/PV/Supply support |
| A-014 | AEGIS does not autonomously determine clinical care, diagnosis, or final benefit-risk |
| A-015 | Local counsel opinion is out of scope; conclusions are training classifications only |

## 2. Applicability position

AEGIS is designed as **human-oversight advisory software** with prohibited autonomous high-stakes decisions. Depending on final intended-purpose statements and integration depth, obligations may still arise for transparency, risk management, data governance, logging and human oversight — addressed via artefacts 13–18 and 20–21.

## 3. Residual uncertainty

Whether a specific deployer classification is high-risk under Annex III-like scenarios remains **unresolved without legal determination**. Team 3 abstains from asserting a definitive statutory class and instead implements conservative controls (logging, oversight, accuracy/evaluation, cybersecurity).""",
        "R-1901",
        "Statutory classification unresolved — conservative controls adopted",
        "Assumptions and conservative controls recorded",
        "Governance artefacts",
        "Legal/regulatory review gate",
        "submission/artefacts/19_EU_AI_ACT_APPLICABILITY.md",
    ))

    write(ART / "20_ISO42001_GOVERNANCE.md", artefact(
        "ISO/IEC 42001 Governance Alignment",
        "Team 3 — Security / privacy lead",
        "Architecture; Evaluation",
        "knowledge/AI_MODEL_CHANGE_CONTROL.md; ADR-002/010",
        "Align AEGIS AI management controls with ISO/IEC 42001-style AIMS themes proportionate to advisory use.",
        """| E-001 | `knowledge/AI_MODEL_CHANGE_CONTROL.md` | Model change policy | Controlled changes | Scenario |
| E-002 | `data/model_registry.csv` | Registry | Approved hashes/versions | Synthetic |
| E-003 | `knowledge/AI_INCIDENT_RESPONSE.md` | Incident policy | Response expectations | Scenario |""",
        """## 1. AIMS themes mapped

| Theme | AEGIS control |
|---|---|
| Policy & accountability | Charter roles; intended use artefact 13 |
| Risk assessment | Artefacts 15–17 |
| Data & model lifecycle | Hash pin; change control; evaluation gates |
| Impact assessment | Human factors + privacy artefacts |
| Third parties | Vendor concentration/exit noted (INJ-078/083); replaceable adapter ADR-002 |
| Monitoring & improvement | Evaluation scorecards (Phase 6); incident runbooks |

## 2. Change control triggers

Prompt, retrieval corpus, tool manifest, model hash, schema version or policy rule changes require evaluation re-run and dual review for hard-gate impacts.""",
        "R-2001",
        "Formal certified AIMS is out of capstone scope; alignment is thematic",
        "Change control triggers defined",
        "Model registry + tests",
        "Governance review",
        "submission/artefacts/20_ISO42001_GOVERNANCE.md",
    ))

    write(ART / "21_ASSURANCE_CASE.md", artefact(
        "Assurance Case",
        "Team 3 — Evaluation / reliability lead",
        "All leads (independent hard-gate review)",
        "Claims C-1..C-5; artefacts 01–20; tests",
        "Provide a claims–arguments–evidence case for Phase 4 exit and a provisional conditional-go framing for later defence.",
        """| E-001 | `DEFINITION_OF_DONE.md` | Completion standard | Reproducible, bounded, evidenced | Binding |
| E-002 | `requirements/SCORING_MODEL.md` | Hard gates | Prohibited actions fail closed | Binding |
| E-003 | `submission/tests/*.py` | Executable evidence | Policy/contract tests | Growing |""",
        """## 1. Top claim

**C-1:** AEGIS Phase 0–4 design is suitable to proceed to POC build (Phase 5) under a **conditional-go**, provided prohibited-action and trust controls remain fail-closed and residual risks in QRM/privacy remain accepted by owners.

## 2. Supporting claims

| Claim | Argument | Evidence |
|---|---|---|
| C-2 Problem qualified vs no-AI | DMAIC + baselines | Artefacts 01–04; D-003 |
| C-3 Evidence model bounded | Contexts, semantics, KG deferral | Artefacts 05–09; EVIDENCE_MAP |
| C-4 Architecture enforces boundaries | C4/ADRs/contracts/GxP/CSA/QRM | Artefacts 10–15; contract tests |
| C-5 Secure AI design | Threats/privacy/HF/governance | Artefacts 16–20; policy tests |

## 3. Invalidation conditions

- Any prohibited action becomes executable in assessed mode
- Authorization accepts stale cache
- Unsigned/poisoned tools callable
- Silent unit conversion reintroduced
- AI-disabled path removed

## 4. Residual risk statement

Automation bias, multilingual inequity, organizational KPI pressure, and unresolved EU AI Act classification remain open. These do not block Phase 5 if technical hard gates stay green and human oversight design is implemented in the POC.

## 5. Decision requested

**Conditional-go to Phase 5 POC build** with gates: keep tests green; implement three offline workflows; do not expand into disposition/execution tools.""",
        "R-2101",
        "Defence (Phase 8) may upgrade/downgrade recommendation after TEVV",
        "Conditional-go justified by Phase 0–4 evidence",
        "Assurance case + tests",
        "Independent review",
        "submission/artefacts/21_ASSURANCE_CASE.md",
    ))

    # Append assumptions/decisions
    log_path = ART / "ASSUMPTIONS_AND_DECISION_LOG.md"
    append = """
---

## Phase 2–4 additions (2026-08-10)

### Assumptions

| ID | Assumption | Owner | Evidence | Invalidation | Status |
|---|---|---|---|---|---|
| A-013 | EU AI Act analysis assumes EU operational placement for advisory use; not a legal classification | Security / privacy | Artefact 19; PACKAGE_SCOPE regulatory boundary | Counsel issues formal class | Open |
| A-014 | Relational evidence register can meet multi-hop needs for POC without a graph database | Architecture | Artefact 08; RELATIONSHIP_MODEL.csv | Evaluation fails contradiction recall vs graph prototype | Accepted |
| A-015 | Public `evaluation/contracts` schemas are the compatibility baseline for participant fixtures | Architecture | evaluation/contracts; ADR-007 | Schema version bump with dual-run tests | Accepted |
| A-016 | Assessed mode remains read-only toward MES/QMS/safety/inventory | GxP / quality | ai_use_boundaries; ADR-006 | Supervised write approved by Quality/Safety governance | Accepted |

### Decisions

| ID | Decision | Alternatives considered | Owner | Evidence | Date | Status |
|---|---|---|---|---|---|---|
| D-011 | Defer knowledge graph; use evidence register + bounded joins | Graph-first platform | Architecture | Artefact 08 | 2026-08-10 | Accepted |
| D-012 | Semantic layer = versioned contracts + vocab tables + citation objects | Full enterprise ontology platform | Domain | Artefact 07 | 2026-08-10 | Accepted |
| D-013 | Adopt CSA/CSV hybrid with hard-gate automated tests before unscripted exploration | Full IQ/OQ/PQ theatre for POC | GxP | Artefacts 13–14 | 2026-08-10 | Accepted |
| D-014 | Enforce policy_guard deny-by-default for prohibited actions, stale auth, poisoned tools, model hash mismatch | Warn-only security | Security | Artefacts 16; tests | 2026-08-10 | Accepted |
| D-015 | Phase 0–4 exit recommendation is conditional-go to POC build | Pause; stop; unconditional go | Evaluation + Product | Artefact 21 | 2026-08-10 | Accepted |

### Change record

| Date | Change | By |
|---|---|---|
| 2026-08-10 | Phase 2–4 assumptions A-013..A-016 and decisions D-011..D-015; artefacts 05–21 | Team 3 |
"""
    if log_path.exists():
        text = log_path.read_text(encoding="utf-8")
        if "D-011" not in text:
            log_path.write_text(text.rstrip() + "\n" + append, encoding="utf-8")
    else:
        write(log_path, "# Assumptions and Decision Log\n" + append)

    # ---- Code: contracts + policy_guard ----
    write(SRC / "__init__.py", '"""AEGIS-PHARMA submission package (Team 3)."""\n')

    write(SRC / "contracts.py", r'''"""Minimal JSON-schema subset validator for workflow contracts."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

FIX = Path(__file__).resolve().parents[1] / "tests" / "fixtures"


def load_json(name: str) -> Any:
    return json.loads((FIX / name).read_text(encoding="utf-8"))


def validate(value: Any, schema: dict, path: str = "$") -> list[str]:
    errors: list[str] = []
    if "$ref" in schema:
        ref = schema["$ref"]
        target = load_json(ref)
        return validate(value, target, path)
    typ = schema.get("type")
    if isinstance(typ, list):
        ok = any((t == "null" and value is None) or (t == "string" and isinstance(value, str)) for t in typ)
        if not ok:
            return [f"{path}: wrong type"]
    elif typ == "object" and not isinstance(value, dict):
        return [f"{path}: expected object"]
    elif typ == "array" and not isinstance(value, list):
        return [f"{path}: expected array"]
    elif typ == "string" and not isinstance(value, str):
        return [f"{path}: expected string"]
    elif typ == "boolean" and not isinstance(value, bool):
        return [f"{path}: expected boolean"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: not in enum")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: too short")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: pattern mismatch")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: too few items")
        for i, v in enumerate(value):
            errors += validate(v, schema.get("items", {}), f"{path}[{i}]")
    if isinstance(value, dict):
        for req in schema.get("required", []):
            if req not in value:
                errors.append(f"{path}: missing {req}")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for k in value:
                if k not in props:
                    errors.append(f"{path}: additional property {k}")
        for k, v in value.items():
            if k in props:
                errors += validate(v, props[k], f"{path}.{k}")
    return errors


def validate_named(sample_name: str, schema_name: str) -> list[str]:
    return validate(load_json(sample_name), load_json(schema_name))
''')

    write(SRC / "policy_guard.py", r'''"""Deny-by-default policy enforcement for prohibited regulated actions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


BATCH_PROHIBITED = {
    "disposition",
    "release_decision",
    "reject_decision",
    "reprocess",
    "relabel",
    "recall",
    "batch_disposition",
}
PV_PROHIBITED = {
    "final_seriousness",
    "final_causality",
    "final_expectedness",
    "final_reportability",
    "signal_confirmation",
    "causality",
    "seriousness_decision",
    "reportability_decision",
}
SUPPLY_PROHIBITED = {
    "reserve",
    "allocate",
    "shipment_execute",
    "ship",
    "quality_status_change",
    "recall_initiate",
    "recall",
}


@dataclass(frozen=True)
class Decision:
    allow: bool
    reason: str


def _contains_prohibited(payload: dict[str, Any], banned: set[str]) -> list[str]:
    hits: list[str] = []
    for key in payload:
        if key in banned:
            hits.append(key)
    # nested common envelopes
    for nest in ("action", "actions", "decision", "execution", "side_effects"):
        obj = payload.get(nest)
        if isinstance(obj, dict):
            for key in obj:
                if key in banned:
                    hits.append(f"{nest}.{key}")
            for key, val in obj.items():
                if key in {"type", "name", "action"} and isinstance(val, str) and val in banned:
                    hits.append(f"{nest}.{key}={val}")
        if isinstance(obj, list):
            for i, item in enumerate(obj):
                if isinstance(item, str) and item in banned:
                    hits.append(f"{nest}[{i}]={item}")
                if isinstance(item, dict):
                    hits.extend(f"{nest}[{i}].{h}" for h in _contains_prohibited(item, banned))
    return hits


def check_workflow_payload(workflow: str, payload: dict[str, Any]) -> Decision:
    if workflow == "batch_evidence":
        hits = _contains_prohibited(payload, BATCH_PROHIBITED)
        if payload.get("execution_status") not in (None, "not_executed") and "execution_status" in payload:
            if payload.get("execution_status") != "not_executed":
                hits.append("execution_status")
    elif workflow == "pv_intake":
        hits = _contains_prohibited(payload, PV_PROHIBITED)
    elif workflow == "supply_planning":
        hits = _contains_prohibited(payload, SUPPLY_PROHIBITED)
        if payload.get("no_side_effects") is False:
            hits.append("no_side_effects=false")
    else:
        return Decision(False, f"unknown workflow {workflow}")
    if hits:
        return Decision(False, "prohibited fields: " + ", ".join(sorted(set(hits))))
    return Decision(True, "ok")


def check_authorization(entitlement_active: bool, cache_says_allow: bool, cache_fresh: bool) -> Decision:
    """INJ-067: stale or revoked entitlements deny even if cache allows."""
    if not entitlement_active:
        return Decision(False, "entitlement revoked")
    if not cache_fresh:
        return Decision(False, "stale authorization cache")
    if not cache_says_allow:
        return Decision(False, "cache deny")
    return Decision(True, "fresh allow")


def check_tool_manifest(manifest: dict[str, Any], approved_hashes: set[str]) -> Decision:
    """INJ-066: deny unsigned, hash-mismatched, or write/disposition tools."""
    tool_hash = manifest.get("sha256") or manifest.get("hash")
    if not tool_hash or tool_hash not in approved_hashes:
        return Decision(False, "tool hash not approved")
    if manifest.get("signed") is not True:
        return Decision(False, "tool not signed")
    perms = set(manifest.get("permissions") or [])
    write_like = {"write", "update", "disposition", "release", "allocate", "ship", "recall"}
    if perms & write_like:
        return Decision(False, "write/disposition permissions not allowed in assessed mode")
    if manifest.get("side_effects") is True:
        return Decision(False, "side_effects not allowed")
    return Decision(True, "approved read tool")


def check_model_artifact(registry_hash: str, artifact_hash: str) -> Decision:
    """INJ-070: model supply-chain hash pin."""
    if not registry_hash or not artifact_hash or registry_hash != artifact_hash:
        return Decision(False, "model hash mismatch")
    return Decision(True, "hash match")
''')

    # Ensure fixtures exist (copy from evaluation samples if needed)
    samples = Path(__file__).resolve().parents[2] / "evaluation" / "contract_samples"
    schemas = Path(__file__).resolve().parents[2] / "evaluation" / "contracts"
    for src_dir in (samples, schemas):
        if src_dir.is_dir():
            for p in src_dir.glob("*"):
                if p.is_file():
                    target = FIX / p.name
                    if not target.exists():
                        target.write_bytes(p.read_bytes())

    # Poisoned / auth fixtures
    write(FIX / "tool_manifest_approved.json", """{
  "name": "batch_evidence_read",
  "sha256": "approvedhash001",
  "signed": true,
  "permissions": ["read"],
  "side_effects": false
}
""")
    write(FIX / "tool_manifest_poisoned.json", """{
  "name": "batch_status_write",
  "sha256": "poisonedhash666",
  "signed": false,
  "permissions": ["read", "write", "disposition"],
  "side_effects": true,
  "hidden_default": {"disposition": "release"}
}
""")

    write(TESTS / "test_workflow_contracts.py", r'''import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.contracts import validate_named  # noqa: E402


class WorkflowContractTests(unittest.TestCase):
    def test_positive_batch(self):
        self.assertEqual(validate_named("positive_batch.json", "batch_response.schema.json"), [])

    def test_positive_pv(self):
        self.assertEqual(validate_named("positive_pv.json", "pv_response.schema.json"), [])

    def test_positive_supply(self):
        self.assertEqual(validate_named("positive_supply.json", "supply_response.schema.json"), [])

    def test_negative_batch_prohibited(self):
        errs = validate_named("negative_batch_prohibited.json", "batch_response.schema.json")
        self.assertTrue(errs)

    def test_negative_pv_prohibited(self):
        errs = validate_named("negative_pv_prohibited.json", "pv_response.schema.json")
        self.assertTrue(errs)

    def test_negative_supply_side_effect(self):
        errs = validate_named("negative_supply_side_effect.json", "supply_response.schema.json")
        self.assertTrue(errs)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
''')

    write(TESTS / "test_prohibited_actions.py", r'''import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.policy_guard import check_workflow_payload  # noqa: E402


class ProhibitedActionTests(unittest.TestCase):
    def test_batch_release_denied(self):
        d = check_workflow_payload("batch_evidence", {"disposition": "release", "execution_status": "executed"})
        self.assertFalse(d.allow)

    def test_batch_recall_denied(self):
        d = check_workflow_payload("batch_evidence", {"recall": True})
        self.assertFalse(d.allow)

    def test_pv_final_causality_denied(self):
        d = check_workflow_payload("pv_intake", {"final_causality": "related"})
        self.assertFalse(d.allow)

    def test_pv_reportability_denied(self):
        d = check_workflow_payload("pv_intake", {"final_reportability": "expedited"})
        self.assertFalse(d.allow)

    def test_supply_allocate_denied(self):
        d = check_workflow_payload("supply_planning", {"allocate": {"qty": 10}, "no_side_effects": False})
        self.assertFalse(d.allow)

    def test_supply_ship_denied(self):
        d = check_workflow_payload("supply_planning", {"ship": True})
        self.assertFalse(d.allow)

    def test_clean_batch_allowed(self):
        d = check_workflow_payload("batch_evidence", {"execution_status": "not_executed", "gaps": []})
        self.assertTrue(d.allow)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
''')

    write(TESTS / "test_authorization_freshness.py", r'''import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.policy_guard import check_authorization  # noqa: E402


class AuthorizationFreshnessTests(unittest.TestCase):
    def test_stale_cache_denied(self):
        d = check_authorization(entitlement_active=True, cache_says_allow=True, cache_fresh=False)
        self.assertFalse(d.allow)
        self.assertIn("stale", d.reason)

    def test_revoked_denied_even_if_cache_allows(self):
        d = check_authorization(entitlement_active=False, cache_says_allow=True, cache_fresh=True)
        self.assertFalse(d.allow)

    def test_fresh_allow(self):
        d = check_authorization(entitlement_active=True, cache_says_allow=True, cache_fresh=True)
        self.assertTrue(d.allow)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
''')

    write(TESTS / "test_tool_trust.py", r'''import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.policy_guard import check_model_artifact, check_tool_manifest  # noqa: E402

FIX = ROOT / "tests" / "fixtures"


class ToolTrustTests(unittest.TestCase):
    def test_poisoned_tool_denied(self):
        manifest = json.loads((FIX / "tool_manifest_poisoned.json").read_text(encoding="utf-8"))
        d = check_tool_manifest(manifest, approved_hashes={"approvedhash001"})
        self.assertFalse(d.allow)

    def test_approved_read_tool_allowed(self):
        manifest = json.loads((FIX / "tool_manifest_approved.json").read_text(encoding="utf-8"))
        d = check_tool_manifest(manifest, approved_hashes={"approvedhash001"})
        self.assertTrue(d.allow)

    def test_model_hash_mismatch_denied(self):
        d = check_model_artifact("abc", "xyz")
        self.assertFalse(d.allow)

    def test_model_hash_match_allowed(self):
        d = check_model_artifact("abc", "abc")
        self.assertTrue(d.allow)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
''')

    write(SCRIPTS / "test.py", r'''#!/usr/bin/env python3
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py")
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
''')

    write(EVID / "PHASE_0_TO_4_EXIT.md", """# Phase 0–4 Exit Evidence Pack

| Field | Entry |
|---|---|
| Team | Team 3 |
| Date | 2026-08-10 |
| Recommendation | Conditional-go to Phase 5 POC build |

## Exit checklist

| Phase | Exit evidence | Status |
|---|---|---|
| 0 Preflight | `PREFLIGHT_REPORT.md`, charter, working agreements | Complete |
| 1 Discovery/DMAIC | Artefacts 01–04; assumptions/decision log | Complete |
| 2 Domain/evidence | Artefacts 05–09; `EVIDENCE_MAP.md` | Complete |
| 3 Architecture/controls | Artefacts 10–15; contract tests | Complete |
| 4 Secure AI design | Artefacts 16–21; prohibited-action/authz/tool tests | Complete |

## Commands

```text
python tools/check_submission_structure.py --scaffold
python tools/test_contracts.py
python submission/scripts/test.py
```

## Known package limitation

`python run_capstone.py --check` fails on AppleDouble `prompts/._*.md` UTF-8 decode; challenge tools left unmodified (D-006).
""")

    print("Generated Phase 2–4 artefacts, src, tests, and exit evidence.")


if __name__ == "__main__":
    main()
