# Assumptions and Decision Log — Team 3 / Project AEGIS-PHARMA

| Field | Entry |
|---|---|
| Custodian | Product / value lead (Phase 2 custodian: Domain / evidence lead) |
| Version / date | 1.2 / 2026-08-10 |
| Status | Living log for Phases 0–2 and Phase 4 (extend in later phases) |
| Related | `PACKAGE_SCOPE_AND_ASSUMPTIONS.md`; `submission/evidence/PREFLIGHT_REPORT.md`; artefacts 00–09; `EVIDENCE_MAP.md`; artefacts 16–21 |

## How to use

- **Assumption (A-xxx):** belief required to proceed; must cite evidence or explicit absence of evidence; invalidation trigger required (WA-02).
- **Decision (D-xxx):** governed choice with owner, alternatives considered, and evidence.
- Status values: Open | Accepted | Invalidated | Superseded.
- Never silently “clean” challenge contradictions; record resolutions here (WA-03).

---

## Assumptions

| ID | Statement | Owner | Evidence / basis | Invalidation trigger | Status |
|---|---|---|---|---|---|
| A-001 | Failure of `python run_capstone.py --check` with `UnicodeDecodeError` in `tools/verify_package.py` is an environment/package encoding finding on Windows 10 / Python 3.14; Team 3 will not patch challenge tools and may proceed using `--scaffold`, diagnostics and local submission hashes | Build lead | `submission/evidence/PREFLIGHT_REPORT.md`; traceback at `tools/verify_package.py` line 108 | Challenge maintainers ship a UTF-8-safe verifier or identify a participant-owned encoding defect under `submission/` | Accepted |
| A-002 | Percentages in `data/no_ai_baselines.csv` (master_data_repair 38%, rules_workflow 27%, genai_assist 51%) are process-excellence estimates for relative comparison (INJ-003), not audited NovaCura historical performance | Product / value | `data/no_ai_baselines.csv`; `case/INTEGRATED_CASE.md` INJ-003 | Measured fixture baselines contradict relative ordering | Accepted |
| A-003 | Offline synthetic package mode is sufficient to design and demonstrate Workflows A–C without internet, cloud keys or live instructor services | Architecture | `PACKAGE_SCOPE_AND_ASSUMPTIONS.md` | A required public fixture cannot run offline | Accepted |
| A-004 | Board request BR-01 (−14% release lead time, no specification or Quality-authority change, due 2026-11-30) is the binding value constraint for Workflow A benefits claims | Product / value | `data/board_requests.csv` | Superseding board record appears in package (none expected) | Accepted |
| A-005 | Executive AI-use boundaries in `data/ai_use_boundaries.csv` plus case §4 prohibitions are hard gates equivalent to scoring non-negotiables | GxP / quality | `data/ai_use_boundaries.csv`; `requirements/SCORING_MODEL.md` hard gates; INJ-006 | Written board waiver in package evidence (not present) | Accepted |
| A-006 | KPI rows in `data/kpi_conflicts.csv` are simultaneously active incentives; AEGIS must not optimize one by suppressing another’s evidence needs | Product / value | `data/kpi_conflicts.csv`; `case/STAKEHOLDER_PACK.md` deliberate conflicts; INJ-002 | Explicit enterprise priority order issued in challenge data | Accepted |
| A-007 | NCX-101 19-month patent horizon in `data/portfolio_products.csv` creates schedule pressure (INJ-004) but does not authorize prohibited AI actions | Product / value | `data/portfolio_products.csv`; INJ-004; INJ-006 | Portfolio record changes patent_months materially | Accepted |
| A-008 | Baseline diagnostics findings (stale entitlement cache, model hash mismatch, unapproved unit mapping, untrusted knowledge) are real design inputs, not noise to ignore | Security / privacy | `starter/baseline_diagnostics.py` output; INJ-067, INJ-070, INJ-024, INJ-065 | Diagnostics script revised by package maintainers | Accepted |
| A-009 | AI-disabled continuity must cover all three workflows per `data/continuity_requirements.csv` (batch/supply 14-day; PV manual required) | Evaluation / reliability | `data/continuity_requirements.csv`; INJ-082 | Continuity CSV revised | Accepted |
| A-010 | Stakeholder sample ST-01..03 plus `case/STAKEHOLDER_PACK.md` is sufficient to establish Phase 1 RAPID; deeper `decision_rights.csv` tabulation continues in Phase 2+ | Domain / evidence | `data/stakeholders.csv`; `case/STAKEHOLDER_PACK.md`; INJ-074 | Conflict discovered that changes Decide column for Workflow A–C | Open |
| A-011 | Hybrid sequencing (master data + rules first; genai_assist optional) is compatible with participant freedom in `PACKAGE_SCOPE_AND_ASSUMPTIONS.md` | Architecture | Package participant freedom clause; `data/no_ai_baselines.csv` | Evaluation proves inference-free path cannot meet agreed proxies and inference still respects hard gates | Open |
| A-012 | Team 3 workshop roles may be combined in persons provided independent review of hard-gate content remains visible | Product / value | `WORKSHOP_DEPLOYMENT_PLAN.md`; `00_TEAM_CHARTER.md` | Examiner requires named unique persons per role | Accepted |
| A-401 | Every retrieval and inference request carries an explicit purpose code; mismatch with consent/purpose registry yields deny or abstain (INJ-060) | Security / privacy | `data/consents.csv`; artefact 17 | Consent schema cannot express purpose codes in POC fixtures | Accepted |
| A-402 | Workshop POC does not train models on EU trial personal data; secondary-use training exports remain blocked design paths | Security / privacy | INJ-060; `data/data_exports.csv` | Board mandates training export inside AEGIS (would invalidate) | Accepted |
| A-403 | Offline fixtures simulate residency labels; no real cross-border personal-data transfer occurs in the workshop runtime | Architecture | INJ-064; `PACKAGE_SCOPE_AND_ASSUMPTIONS.md` | Live multi-region deployment enabled without residency gates | Accepted |
| A-404 | For EU AI Act narrative, NovaCura is treated as deployer of an internal advisory AI system; Team 3 delivers workshop POC only | GxP / quality | Artefact 19; case §8 | Production deployment changes actor role to provider of GPAI | Accepted |
| A-405 | Primary applicability lens is EU deployer-oriented obligations; other jurisdictions may impose additional duties not fully analysed here | GxP / quality | Artefact 19 §1 | Non-EU go-live without parallel analysis | Accepted |
| A-406 | Provider duties for placing a general-purpose model on the market are out of current POC claim scope | Architecture | Artefact 19 §5 | NovaCura ships a GPAI component externally | Accepted |

---

## Decisions

| ID | Decision | Alternatives considered | Owner | Evidence | Date | Status |
|---|---|---|---|---|---|---|
| D-001 | Limit Phase 1–5 POC scope to the three mandatory workflows (batch evidence reconciliation; PV intake/signal support; supply options/cold-chain recovery) | Broader clinical eligibility automation; full RIM automation | Product / value | `case/INTEGRATED_CASE.md` §4; business case §5 | 2026-08-10 | Accepted |
| D-002 | Keep batch disposition, final PV judgements and allocate/ship/recall outside system capabilities (no write tools) | Advisory with optional supervised write; full automation for BR-01 speed | GxP / quality | `data/ai_use_boundaries.csv`; INJ-006; scoring hard gates | 2026-08-10 | Accepted |
| D-003 | Treat no-AI baselines as first-class competitors; require measured comparison before claiming unique AI value | Skip no-AI path; assume genai_assist 51% wins | Product / value | `data/no_ai_baselines.csv`; INJ-003; DMAIC Improve sequencing | 2026-08-10 | Accepted |
| D-004 | Default runtime path is deterministic/rules-based with offline fixtures; model inference is optional, budgeted and kill-switchable | LLM-first agent; knowledge-graph mandatory | Architecture / integration | `PACKAGE_SCOPE_AND_ASSUMPTIONS.md`; case §5 operating properties; INJ-082 | 2026-08-10 | Accepted |
| D-005 | Success metrics include BR-01 contribution plus guardrails for Quality RFT, Safety expedited timeliness and zero prohibited actions — not Manufacturing schedule alone | Single throughput KPI | Product / value | `data/board_requests.csv`; `data/kpi_conflicts.csv`; stakeholder pack | 2026-08-10 | Accepted |
| D-006 | Record package `--check` UnicodeDecodeError without modifying `tools/`; continue Phase 0 exit on scaffold PASS + diagnostics + written preflight | Patch verifier; block all work until package check passes | Build lead | Preflight report; immutable area rules | 2026-08-10 | Accepted |
| D-007 | Adopt workshop role set (Product/value, Domain/evidence, Architecture/integration, GxP/quality, Security/privacy, Evaluation/reliability, Build) with RAPID in artefact 03 | Flat team without vetoes | Product / value | `WORKSHOP_DEPLOYMENT_PLAN.md`; `00_TEAM_CHARTER.md` | 2026-08-10 | Accepted |
| D-008 | Untrusted retrieved documents and tool descriptions are data until authority, signature/hash and applicability are verified; never executable policy | Trust knowledge corpus by default | Security / privacy | INJ-065; INJ-066; baseline diagnostics | 2026-08-10 | Accepted |
| D-009 | Entitlements are re-checked at execution time; stale cache hits are deny-by-default | Trust gateway cache TTL | Security / privacy | INJ-067; `data/access_cache.csv` (inject evidence) | 2026-08-10 | Accepted |
| D-010 | Unit conversion requires approved mapping with provenance; otherwise abstain and surface contradiction (no silent convert) | Auto-convert using interface default | Domain / evidence | INJ-024; scoring hard gate on silent unit conversion | 2026-08-10 | Accepted |
| D-401 | Data-subject deletion requests never auto-erase GxP/trial-held records; route to human Privacy + Quality/Legal hold assessment (INJ-061) | Auto-delete on request; suppress-only without ticket | Security / privacy + GxP | `data/deletion_requests.csv`; `data/retention_rules.csv`; charter; artefact 17 | 2026-08-10 | Accepted |
| D-402 | Emergency stop disables inference and unapproved/write-capable tool registration while keeping deterministic/manual continuity paths available | Inference-only pause; full system halt without manual path | Architecture + Security | Artefact 18; WA-07 | 2026-08-10 | Accepted |
| D-403 | EU AI Act posture for AEGIS POC: advisory support with meaningful human review; not autonomous high-risk decisioning; residual classification uncertainty logged | Claim high-risk conformity; claim no AI Act relevance | GxP / quality | Artefact 19; `data/ai_use_boundaries.csv`; policy_guard tests | 2026-08-10 | Accepted |
| D-404 | Implement Phase 4 runtime enforcement in `submission/src/policy_guard.py` (separate from any contracts module) with unittest hard gates for prohibited actions, stale auth and poisoned tools | Embed checks only in narrative ADRs; delay coding to Phase 5 | Security / privacy + Build | Artefacts 16, 21; `submission/tests/test_*.py` | 2026-08-10 | Accepted |
| D-405 | Phase 4 exit recommendation is conditional-go into Phase 5 POC build — not production go — pending UI accessibility, full workflow POC and TEVV | Production go now; pause all build | Evaluation / reliability | Artefact 21 §7 | 2026-08-10 | Accepted |

---

## Cross-references

| Artefact | Uses |
|---|---|
| `submission/evidence/PREFLIGHT_REPORT.md` | A-001, A-008, D-006 |
| `submission/artefacts/00_TEAM_CHARTER.md` | D-007, A-012 |
| `submission/artefacts/00_WORKING_AGREEMENTS.md` | WA linkage to A/D process |
| `submission/artefacts/01_BUSINESS_CASE.md` | D-001..D-005, A-002..A-004 |
| `submission/artefacts/02_DMAIC_WORKBOOK.md` | D-003, D-004, A-009 |
| `submission/artefacts/03_STAKEHOLDER_DECISION_RIGHTS.md` | D-002, D-005, A-006, A-010 |
| `submission/artefacts/04_PRODUCT_SERVICE_BLUEPRINT.md` | D-001, D-002, D-004, A-009 |
| `submission/artefacts/16_THREAT_ABUSE_MODEL.md` | D-008, D-009, D-404; A-008 |
| `submission/artefacts/17_PRIVACY_ETHICS.md` | D-401; A-401..A-403 |
| `submission/artefacts/18_RESPONSIBLE_AI_HUMAN_FACTORS.md` | D-402; INJ-071..074 |
| `submission/artefacts/19_EU_AI_ACT_APPLICABILITY.md` | D-403; A-404..A-406 |
| `submission/artefacts/20_ISO42001_GOVERNANCE.md` | K-005; D-004; D-404 |
| `submission/artefacts/21_ASSURANCE_CASE.md` | D-405; C1–C8 evidence chain |

## Change record

| Date | Change | By |
|---|---|---|
| 2026-08-10 | Initial Phase 0–1 assumptions A-001..A-012 and decisions D-001..D-010 | Team 3 |
| 2026-08-10 | Phase 4 append: assumptions A-401..A-406 and decisions D-401..D-405; cross-refs to artefacts 16–21 | Team 3 |

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

---

## Phase 3 architecture and controls (append 2026-08-10)

Phase 3 exit evidence is artefacts `10_C4_ARCHITECTURE.md` through `15_QUALITY_RISK_MANAGEMENT.md`, plus contract tests under `submission/tests/test_workflow_contracts.py` backed by `submission/src/contracts.py`.

### Phase 3 assumptions

| ID | Statement | Owner | Evidence / basis | Invalidation trigger | Status |
|---|---|---|---|---|---|
| A-301 | C4 advisory overlay with read-only brownfield coexistence is sufficient for workshop defence without live LIMS/MES/QMS/safety/IRT write-back | Architecture | `10_C4_ARCHITECTURE.md`; PACKAGE_SCOPE offline mode | Examiner requires live bidirectional adapters | Open |
| A-302 | K-003 (`AI_GXP_BOUNDARY`) and K-010 (`COMPUTERISED_SYSTEM_LIFECYCLE`) apply as synthetic NTG authorities within their effective dates for CSV/CSA framing | GxP / quality | `13_GXP_LIFECYCLE_VALIDATION.md`; knowledge docs | Superseding knowledge document | Accepted |
| A-303 | Executable contract baseline remains `evaluation/contracts/` with offline mirrors in `submission/tests/fixtures/` | Architecture | `12_INTEGRATION_CONTRACTS.md`; A-015 | Schema version bump without dual-run tests | Accepted |

### Phase 3 decisions

| ID | Decision | Alternatives considered | Owner | Evidence | Date | Status |
|---|---|---|---|---|---|---|
| D-301 | Publish completed C4 architecture with kill switch on inference only and mandatory AI-disabled deterministic path for Workflows A–C | Kill entire API on stop; AI-only demo path | Architecture | `10_C4_ARCHITECTURE.md`; ADR-011; INJ-082 | 2026-08-10 | Accepted |
| D-302 | Accept ADR-001..ADR-012 (deterministic-first, replaceable inference, fail-closed prohibited actions, authority-checked retrieval, signed tools, supply no side effects, versioned contracts, offline mode, HITL, budget/stop, kill switch, execution-time authZ) | LLM-first write-capable agent | Architecture | `11_ADR_REGISTER.md` | 2026-08-10 | Accepted |
| D-303 | Enforce versioned I/O via `contracts.py` with `additionalProperties` denial and explicit disposition/causality/side-effect rejection; prove with positive/negative unittest fixtures | Narrative contracts only; soft warnings | Architecture + Build | `12_INTEGRATION_CONTRACTS.md`; `test_workflow_contracts.py` | 2026-08-10 | Accepted |
| D-304 | Apply proportionate CSV/CSA lifecycle: GxP-relevant advisory intended use; high-risk controls denser assurance; unscripted testing for automation bias (INJ-071) | Full IQ/OQ theatre for all UI; treat non-GxP | GxP / quality | `13_GXP_LIFECYCLE_VALIDATION.md`; `14_COMPUTER_SOFTWARE_ASSURANCE.md` | 2026-08-10 | Accepted |
| D-305 | QRM covers three workflows; hazards of automation bias (INJ-071), omitted evidence and unit conversion (INJ-024) controlled fail-closed; residual human skimming conditionally accepted for POC only | Accept automated disposition for BR-01 speed | GxP / quality | `15_QUALITY_RISK_MANAGEMENT.md` | 2026-08-10 | Accepted |

### Phase 3 cross-references

| Artefact | Uses |
|---|---|
| `submission/artefacts/10_C4_ARCHITECTURE.md` | D-301; A-301 |
| `submission/artefacts/11_ADR_REGISTER.md` | D-302; ADR-001..012 |
| `submission/artefacts/12_INTEGRATION_CONTRACTS.md` | D-303; A-303 |
| `submission/artefacts/13_GXP_LIFECYCLE_VALIDATION.md` | D-304; A-302; K-003; K-010 |
| `submission/artefacts/14_COMPUTER_SOFTWARE_ASSURANCE.md` | D-304 |
| `submission/artefacts/15_QUALITY_RISK_MANAGEMENT.md` | D-305; INJ-024; INJ-071 |
| `submission/src/contracts.py` | D-303 |
| `submission/tests/test_workflow_contracts.py` | D-303 |

### Change record

| Date | Change | By |
|---|---|---|
| 2026-08-10 | Phase 3 append: assumptions A-301..A-303 and decisions D-301..D-305; artefacts 10–15 restored/completed; contract tests | Team 3 |

---

## Phase 2 — Domain and evidence model (detailed append)

Complements abbreviated A-013/A-014/D-011/D-012 above. New IDs use the A-20x / D-20x series to avoid colliding with Phase 4 A-40x / D-40x and the short Phase 2–4 block.

### Assumptions

| ID | Statement | Owner | Evidence / basis | Invalidation trigger | Status |
|---|---|---|---|---|---|
| A-201 | Package relational model in `data/RELATIONSHIP_MODEL.csv` plus fixture edge tables (`material_genealogy.csv`, `duplicate_candidates.csv`, logger associations) are sufficient to express Workflow A–C multi-hop evidence without a graph database at POC scale (elaborates A-014) | Architecture / Domain | `RELATIONSHIP_MODEL.csv`; `EVIDENCE_MAP.md` §§3–5; artefact 08 T1–T3 | Exit triggers X-1..X-3 in `08_KNOWLEDGE_GRAPH_DECISION.md` fire | Accepted |
| A-202 | Contextual authority per `case/SOURCE_SYSTEM_FACT_PACK.md` applies: no system is universally authoritative; effective time and role bind every citation | Domain / evidence | Fact pack; INJ-031; INJ-040 | Package introduces a single enterprise SoR declaration (not present) | Accepted |
| A-203 | Sparse controlled vocabularies and IDMP rows in fixtures are representative challenge conditions; production SPOR completeness is out of POC scope | Domain / Regulatory | `controlled_vocabularies.csv`; `idmp_mappings.csv`; INJ-045 | Examiner requires full IDMP/SPOR implementation for pass | Accepted |
| A-204 | Document catalog entries with `availability=intentionally_absent` or `referenced_missing` (e.g. DOC-ECTD-1) are deliberate gaps; absence must be cited, never filled with invented content | Domain / GxP | `document_catalog.csv`; INJ-048 | Missing file appears in package with verified hash | Accepted |
| A-205 | Phase 2 planned test IDs in `09_REQUIREMENTS_TRACEABILITY.md` will be implemented as automated tests during Phase 5; design acceptance does not imply code existence yet | Evaluation / Build | Artefact 09 §§2–6 | Phase 5 gate without named tests | Open |

### Decisions

| ID | Decision | Alternatives considered | Owner | Evidence | Date | Status |
|---|---|---|---|---|---|---|
| D-201 | Treat IDMP / product identity conflicts (RIM NCB-204 vs ERP NCB204-DE; mapping_status ambiguous) as dual-cite stewardship items; never auto-merge in AEGIS | Collapse to single product id via aliases | Domain / Regulatory | INJ-045; `medicinal_products.csv`; `idmp_mappings.csv`; `knowledge/IDMP_MASTER_DATA_GOVERNANCE.md` | 2026-08-10 | Accepted |
| D-202 | Implement LIMS, MES/warehouse, QMS and Safety anti-corruption layers that namespace identifiers, deny undeclared properties and preserve verbatim units/times/statuses per versioned contracts | Shared enterprise canonical model written back to sources | Architecture / Domain | Artefact 05 §5; `api_contract_versions.csv`; LIMS contract source_documents | 2026-08-10 | Accepted |
| D-203 | Bound POC ubiquitous language and aggregates to Workflows A–C plus cross-cutting evidence platform; Research/Clinical contexts remain identity/time suppliers without eligibility or discovery automation | Expand write-path into clinical eligibility or research portfolio AI | Product / Domain | D-001; artefact 05 §2; INJ-014 hard gate | 2026-08-10 | Accepted |
| D-204 | On retention conflicts (INJ-035/061): legal hold and GxP retain suppress automated deletion; DSR remains visible for Legal+Privacy+GxP human co-resolution; AEGIS recommends only (aligned with D-401) | Auto-fulfill DSR; auto-purge AI logs under hold | GxP / Privacy | `retention_rules.csv`; `legal_holds.csv` LH-44; `deletion_requests.csv` DSR-17; artefact 06 §6 | 2026-08-10 | Accepted |
| D-205 | Do not implement a knowledge-graph database for Phase 2–5 POC; use Relational Evidence Register + Versioned Contracts (RER+C), retaining a logical graph shape for optional later migration (elaborates D-011) | Mandatory property-graph runtime; vector-only store without register | Architecture | Artefact 08; INJ-021, INJ-037, INJ-051; INJ-078/083; A-201 | 2026-08-10 | Accepted |
| D-206 | Freeze requirements baseline FR/NFR/GXP/SEC/PRI in `09_REQUIREMENTS_TRACEABILITY.md` with non-waivable hard gates for prohibited actions, silent unit conversion, stale authz allow and evidence fabrication | Soft requirements without test IDs; Product waiver of hard gates | Product / Evaluation | Artefact 09; `ai_use_boundaries.csv`; scoring hard gates | 2026-08-10 | Accepted |
| D-207 | Adopt `EVIDENCE_MAP.md` as the Phase 2 master inject-to-evidence index for defence; package `inject_evidence_map.csv` remains the immutable challenge catalogue | Maintain only informal notes outside submission | Domain / evidence | `EVIDENCE_MAP.md`; `data/inject_evidence_map.csv` | 2026-08-10 | Accepted |

### Cross-references (Phase 2)

| Artefact | Uses |
|---|---|
| `submission/artefacts/05_DDD_CONTEXT_MAP.md` | D-201..D-203, A-202; INJ-005/021/045 |
| `submission/artefacts/06_DATA_GOVERNANCE_INTEGRITY.md` | D-204, D-010, A-202, A-204; INJ-018/024/029..036 |
| `submission/artefacts/07_ONTOLOGY_SEMANTIC_LAYER.md` | D-201, D-205, A-203; INJ-039/040/045 |
| `submission/artefacts/08_KNOWLEDGE_GRAPH_DECISION.md` | D-205, D-011, A-201, A-014; INJ-021/037/051/058 |
| `submission/artefacts/09_REQUIREMENTS_TRACEABILITY.md` | D-206, A-205 |
| `submission/artefacts/EVIDENCE_MAP.md` | D-207; full INJ-001..084 register |

### Change record

| Date | Change | By |
|---|---|---|
| 2026-08-10 | Phase 2 detailed append: assumptions A-201..A-205 and decisions D-201..D-207; artefacts 05–09 and EVIDENCE_MAP completed under `submission/` | Team 3 |
