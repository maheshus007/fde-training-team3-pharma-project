# PRD — AEGIS AgenticApp

| Field | Entry |
|---|---|
| Status | Stable for scope; metrics Unknown marked |
| Prompt | `03_prd_vision.md` |
| One question this file answers | What problem are we solving, for whom, and what does success look like? |

## 1. Users / personas

| Persona | Job |
|---|---|
| QP / QA reviewer | Assess batch-review readiness evidence completeness |
| PV case assessor | Intake, duplicate/clock/listedness packaging for human decision |
| Supply planner | Rank draft options under quality/MA/ethics constraints |
| Security / Quality auditor | Inspect provenance, authZ, prohibited-action proofs |
| Build / evaluation engineer | Run offline tests, export evidence |

## 2. Goals

1. Surface contradictions/gaps with citeable provenance for A/B/C.  
2. Enforce ontology/semantic rules (units, MedDRA version, IDMP ambiguity, time/jurisdiction).  
3. Provide multi-hop evidence paths via offline KG without fabricating links.  
4. Orchestrate tools under budgets/checkpoints with HITL.  
5. Preserve AI-disabled continuity.

## 3. Success metrics

| Metric | Target | Baseline |
|---|---|---|
| Prohibited-action success rate | **0** | Tests exist (expand) |
| Schema-valid responses | 100% of assessed runs | Contract tests |
| Correct abstention on unapproved unit map (INJ-024) | Pass | Fixture-based |
| Genealogy conflict recall (INJ-021) | Both MES + WM facts visible | Fixture-based |
| AI-disabled parity on core detections | Pass | To implement |
| BR-01 −14% contribution | Track | **Unknown** |
| Reviewer time saved | Track | **Unknown** |

## 4. In scope (this version)

1. Workflow A — batch evidence pack, conflicts, gaps, readiness (no disposition)  
2. Workflow B — PV intake support, duplicates, clocks, listedness provenance (no finals)  
3. Workflow C — draft supply options, cold-chain flags, constraints (`no_side_effects`)  
4. Ontology + semantic layer services  
5. Offline evidence knowledge graph (read/query; no regulated write edges)  
6. Agentic orchestrator (signed tools, authZ, budgets, checkpoints)  
7. HITL workbench (`submission/app`) with forced evidence viewing  
8. Offline deterministic mode + kill switch for inference  
9. Audit/evidence export  

## 5. Out of scope (this version)

- Autonomous batch release/reject/reprocess/relabel/recall  
- Quality-status change by the system  
- Final seriousness/causality/expectedness/reportability/signal confirmation  
- Reserve/allocate/ship/recall initiation  
- Clinical eligibility determination  
- Autonomous formulation or specification change (INJ-006)  
- Cloud-**only** runtime with **no** assessment/mock adapters (package hard gate)  
- Committing Azure secrets or live connection strings  
- Full enterprise master-data remediation programme  
- Neo4j (Cosmos Gremlin is the product graph — ADR-AA-018)  
- Training models on EU personal trial data (INJ-060)  

## 6. Constraints & non-goals

- Package offline synthetic mode; work only under `submission/`  
- Fail-closed contracts (`additionalProperties: false`)  
- D-002 / INJ-006 hard gates  
- Sync AgenticApp designs into scored artefacts  

## 7. Open questions

1. Exact token/step budgets for agent (provisional numbers in ADR).  
2. Azure OpenAI deployment name / API version / pinned model hash.  
3. Cosmos database/graph names and partition key for Gremlin vertices.  
4. Whether Taipy must launch in assessment mode or JSON export suffices for `--final`.

## Spec hygiene

- No APIs, DB schemas, wireframes, or folder trees in this PRD.  
- Values preferred over adjectives; Unknown labeled.
