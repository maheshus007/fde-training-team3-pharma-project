# AgenticApp Pipeline Execution Plan

> Team 3 working plan. Pipeline outputs live under `submission/AgenticApp/`. Scored capstone artefacts remain under `submission/artefacts/`. Challenge evidence is immutable.

| Field | Entry |
|---|---|
| Goal | End-to-end **agentic** AEGIS app for Workflows A/B/C, with **ontology + semantic layer + knowledge graph**, built via **Spec-Driven Development (SDD)** |
| Method | Execute `submission/prompts/01` → `07` (through ADR), then `08`–`11` for SDD build |
| Mental model | AI FDE: SCQA → DDD → Ontology/Semantic/KG → C4 → SRS/HLD/LLD → ADR → Deliver & Evaluate |
| Status | **Steps 0–7 executed** — architecture review conditional-go to Prompt 08 |
| Date | 2026-08-10 |

---

## 0. Governing decisions (read first)

### 0.1 Folder policy (resolves prompt-mapping conflict)

`submission/prompts/PROMPT_MAPPING.md` forbids parallel artefact trees for **scoring**. This plan treats `submission/AgenticApp/` as:

| Role | Rule |
|---|---|
| **Working pipeline SoT** | All prompt *runs* write here first (deep, structured, SDD-ready) |
| **Scored sync** | After each step gate, promote/merge into `submission/artefacts/NN_*.md` via `_sync/` notes |
| **Implementation** | Code stays in package scaffold: `submission/src`, `app`, `tests`, `evaluation`, `runbooks`, `scripts` |
| **Never** | Do not write outside `submission/`; do not mutate `case/`, `data/`, `knowledge/`, `evaluation/` (package), `templates/` |

Update note to add to `PROMPT_MAPPING.md` when executing: *AgenticApp is the SDD working tree; artefacts remain the scored deliverables.*

### 0.2 Ontology + KG stance (revisits D-205)

Existing `08_KNOWLEDGE_GRAPH_DECISION.md` chose **D-205: no graph DB** (Relational Evidence Register + Contracts).

For AgenticApp the plan is a **controlled supersession**, not silent contradiction:

| Layer | Decision for AgenticApp | Continuity / scoring |
|---|---|---|
| **Ontology** | First-class: concepts, relations, constraints, competency questions (CQ-1..7+) | Maps to artefact `07` |
| **Semantic layer** | Canonical meaning, units, MedDRA/IDMP policies, purpose/access contracts | Maps to artefact `07` |
| **Knowledge graph** | Product: **Azure Cosmos DB Gremlin**; assessment: in-memory/RER `GraphPort`; provenance on every node/edge | ADR-AA-015/018; D-205 kept as assessment fallback |
| **LLM / UI** | Product: **Azure OpenAI** + **Taipy**; assessment: stub LLM + Taipy/mocks | ADR-AA-016/017; no secrets in ZIP |

**Revisit trigger ADR (required in Prompt 07):** `ADR-KG-001` — Accept offline evidence KG for multi-hop citeable paths; RER remains fallback; no write edges for disposition/allocate.

### 0.3 What “agentic end-to-end” means here

Allowed:

- Multi-step orchestrator with **budgets, checkpoints, signed tools, execution-time authZ**
- Tools: load evidence, query ontology/KG, reconcile, cite, abstain, draft options, request human review
- Optional inference adapter behind kill switch

Forbidden (hard gate):

- Autonomous batch disposition, final PV decisions, allocate/ship/recall, clinical eligibility
- Treating untrusted docs/tool text as instructions
- Silent unit conversion or irreversible case merge

### 0.4 SDD layering (how coding will be driven)

```text
Vision/PRD (P03) → Feature Specs (P05) → C4 (P06) → ADR (P07)
    → Technical Design / SRS contracts (P08) → Tasks (P10) → Code+Tests (P11)
```

Nothing material is invented at coding time. Agents retrieve only the feature + contracts + ADR cited by each task.

---

## 1. Pipeline map (image ↔ prompts ↔ AgenticApp)

| Image stage | DMAIC | Team prompt | AgenticApp output folder | Promote to scored artefact |
|---|---|---|---|---|
| Inputs (context, workflow, constraints, evidence, stakeholders) | Define/Measure | `01_discovery.md` | `01_discovery/` | Feeds 01, 03, 06 start |
| **SCQA** | Define | `02_scqa_minto.md` | `02_scqa/` | `01_BUSINESS_CASE.md` |
| PRD / Vision (SDD) | Define | `03_prd_vision.md` | `03_prd/` | `04_PRODUCT_SERVICE_BLUEPRINT.md` (+ 01, 03) |
| **DDD** + Gen AI boundaries | Analyze | `04_ddd.md` | `04_ddd_ontology_kg/` | `05_DDD_CONTEXT_MAP.md` |
| **Ontology / Semantic / KG** | Analyze→Improve | *inside Prompt 04* (+ dedicated KG pack) | `04_ddd_ontology_kg/` | `07`, `08` (supersede D-205 carefully) |
| Feature specs (SDD FRD) | Improve | `05_feature_specs.md` | `05_feature_specs/` | `09_REQUIREMENTS_TRACEABILITY.md` |
| **C4** | Improve | `06_c4.md` | `06_c4/` | `10_C4_ARCHITECTURE.md` |
| **ADR** | Control | `07_adrs.md` | `07_adrs/` | `11_ADR_REGISTER.md` |
| SRS / HLD / LLD contracts | Improve | `08_technical_design.md` | `08_technical_design/` | `12_INTEGRATION_CONTRACTS.md` + eval contracts |
| Build (after ADR gate) | Control/Deliver | `09`→`11` | `09_sdd_build/` + `submission/src|app|tests` | 22–30 later |

**Scope of “through ADR” execution:** complete folders `01`–`07` with gates; stop for architecture review; then continue `08`+ for SDD build.

---

## 2. Target folder tree

```text
submission/AgenticApp/
  00_PIPELINE_EXECUTION_PLAN.md          ← this file
  00_plan/
    EXECUTION_LOG.md                     ← step status, owners, dates
    ASSUMPTIONS.md                       ← pipeline-local assumptions (sync to artefacts log)
    REUSE_FROM_PHASE0_4.md               ← what we inherit vs rewrite
  01_discovery/
    DISCOVERY_REGISTER.md
    AI_FDE_INPUT_SUFFICIENCY.md
    EVIDENCE_ACQUISITION_BACKLOG.md
  02_scqa/
    SCQA_NARRATIVE.md
    MINTO_PYRAMID.md
    FRAMING_HANDOFF.md
  03_prd/
    VISION.md
    PRD.md
  04_ddd_ontology_kg/
    DDD_CONTEXT_MAP.md
    GEN_AI_BOUNDARIES.md
    ONTOLOGY.md
    SEMANTIC_LAYER.md
    KNOWLEDGE_GRAPH_DESIGN.md            ← includes D-205 supersession proposal
    COMPETENCY_QUESTIONS.md
  05_feature_specs/
    FEATURE_INDEX.md
    FR-A-batch-evidence.md
    FR-B-pv-intake.md
    FR-C-supply-options.md
    FR-D-agent-orchestrator.md
    FR-E-ontology-kg-query.md
    FR-F-hitl-workbench.md
  06_c4/
    C4_CONTEXT.md
    C4_CONTAINERS.md
    C4_COMPONENTS.md
    C4_CODE_SKETCH.md
    ADR_CANDIDATES.md
  07_adrs/
    ADR_INDEX.md
    ADR-001_....md … (one file per ADR)
    ARCHITECTURE_REVIEW.md
  08_technical_design/                   ← after ADR gate
    SRS_API_CONTRACTS.md
    DATA_MODEL_AND_KG_SCHEMA.md
    NFRS.md
    ERROR_AND_SECURITY.md
  09_sdd_build/                          ← after technical design
    TASK_INDEX.md
    tasks/
  _sync/
    SYNC_01_to_artefacts.md
    ...
```

---

## 3. Reuse strategy (do not throw away Phase 0–4)

| Existing asset | Action |
|---|---|
| `artefacts/01`–`21`, EVIDENCE_MAP, assumptions log | **Reuse as evidence inputs** to prompts; deepen in AgenticApp; sync deltas back |
| `src/contracts.py`, `policy_guard.py`, 35 tests | Keep as hard-gate core; agent/KG must call them |
| D-205 (no KG DB) | **Supersede with ADR** for offline evidence KG + RER fallback — document options/consequences |
| `supply_planning` vs `supply_options` naming split | Fix in Prompt 08 / early build task |
| `generate_phase2_to4.py` | **Do not re-run** without guards (overwrites deepened artefacts) |

`00_plan/REUSE_FROM_PHASE0_4.md` must list file→section citations before Prompt 02 starts.

---

## 4. Step-by-step execution (through ADR)

### Step 0 — Bootstrap (0.5 day)

**Do:**

1. Create `EXECUTION_LOG.md`, `ASSUMPTIONS.md`, `REUSE_FROM_PHASE0_4.md`
2. Patch `PROMPT_MAPPING.md` with AgenticApp working-tree exception
3. Record pivot: ontology+KG required for AgenticApp; scoring still needs artefact sync

**Exit:** folders exist; reuse inventory complete; no architecture invented yet.

---

### Step 1 — Prompt 01 Discovery → `01_discovery/`

**Run:** `submission/prompts/01_discovery.md` + package control #1/#2  
**Cursor:** `00_qualify_problem`, `01_map_evidence`

**Produce (required by prompt):**

- Repo/source-system map  
- Entities, IDs, timestamp semantics  
- Evidence ownership/authority  
- Conflicts/gaps (preserve inject contradictions)  
- Stakeholder decisions  
- Constraints register  
- Current-state workflow sketch  
- Fact/derivation/assumption/question register  
- Top 10 investigation hypotheses  
- AI FDE input sufficiency + framing mode (`decision-ready` | `hypothesis`)  
- Evidence acquisition backlog  
- Early Lean waste signals  

**Reuse seed:** `PREFLIGHT_REPORT`, `EVIDENCE_MAP`, case packs, `SOURCE_SYSTEM_FACT_PACK`, baseline diagnostics.

**Exit gate:** framing mode declared; SoT/trust gaps explicit; **no** target architecture.

**Sync:** feed `artefacts/01`, `03`; thin notes into `02_DMAIC`.

---

### Step 2 — Prompt 02 SCQA → `02_scqa/`

**Run:** `02_scqa_minto.md` + package #1

**Produce:**

- Narrative class matching Prompt 01  
- Full SCQA (Situation → Complication → Question → Answer)  
- Minto pyramid (governing answer + MECE supports)  
- Framing handoff (metrics, exclusions, open questions)

**Governing Answer target (to validate, not pre-bake):**  
Bounded advisory agentic system for A/B/C with ontology+KG for citeable multi-hop evidence — **without** transferring QP/PV/Supply execution authority.

**Exit gate:** one bounded decision question; Answer capability-level (not vendor/model lock).

**Sync:** `01_BUSINESS_CASE.md` SCQA sections.

---

### Step 3 — Prompt 03 PRD/Vision (SDD) → `03_prd/`

**Run:** `03_prd_vision.md`

**Produce:** `VISION.md`, `PRD.md` with users, goals, metrics, **in/out scope**, constraints, open questions.

**In-scope (recommended):**

1. Batch evidence reconciliation + abstention  
2. PV intake/duplicate/clock/listedness support  
3. Supply draft options (no side effects)  
4. Ontology + semantic contracts  
5. Offline evidence KG query/traversal with provenance  
6. Agentic orchestrator (budgeted tools + HITL)  
7. Offline + AI-disabled continuity  

**Out-of-scope:** autonomous disposition/PV finals/allocate-ship-recall; cloud-only runtime; clinical eligibility; full enterprise master-data cleanup.

**Exit gate:** PRD in/out locked (or explicitly provisional); no APIs/schemas yet.

**Sync:** `04_PRODUCT_SERVICE_BLUEPRINT.md`, complete `01`/`03`.

---

### Step 4 — Prompt 04 DDD + Ontology + Semantic + KG → `04_ddd_ontology_kg/`

**Run:** `04_ddd.md` (owns artefacts 05, 07, 08 per mapping)

**Produce in order:**

1. `DDD_CONTEXT_MAP.md` — subdomains, ubiquitous language, contexts, context map, aggregates/invariants, event storming  
2. `GEN_AI_BOUNDARIES.md` — rules vs AI vs RAG vs agents vs HITL; audit; eval vocabulary  
3. `ONTOLOGY.md` — concepts/relations/constraints; align CQ-1..7 from existing artefact 07; extend for agent tool intents  
4. `SEMANTIC_LAYER.md` — canonical metrics/policies/access; MedDRA version; IDMP ambiguity; units; time/jurisdiction  
5. `KNOWLEDGE_GRAPH_DESIGN.md` — node/edge types, provenance schema, query patterns for A/B/C, security/temporal filters, **D-205 supersession proposal + RER fallback**  
6. `COMPETENCY_QUESTIONS.md` — CQ → SPARQL/Cypher-or-SQL-edge queries → fixture proof plan  

**Exit gate:** artifact status `stable|provisional`; rules/AI/HITL explicit; domain not organized by CSV filenames.

**Sync:** `05`, `06`, `07`, `08` (update decision), start `09`.

---

### Step 5 — Prompt 05 Feature Specs (SDD) → `05_feature_specs/`

**Run:** `05_feature_specs.md` + package #3 + `02_build_tests_first` mindset

**Minimum feature files:**

| ID | Feature | Context |
|---|---|---|
| FR-A | Batch evidence pack / conflicts / readiness | Manufacturing+Quality |
| FR-B | PV intake / duplicates / clocks / listedness | Safety |
| FR-C | Supply options / cold-chain / constraints | Supply |
| FR-D | Agentic orchestrator (budget, checkpoint, tools) | Platform |
| FR-E | Ontology/KG query & path citation | Platform |
| FR-F | HITL workbench (forced evidence view) | Platform |

Each file: actors, preconditions, happy path, exceptions, BRs, ACs, AI/HITL boundaries, ambiguities.

**Exit gate:** FEATURE_INDEX complete; ACs binary/testable; no API schemas yet.

**Sync:** expand `09_REQUIREMENTS_TRACEABILITY.md` (replace TEST-* theatre with real AC IDs).

---

### Step 6 — Prompt 06 C4 → `06_c4/`

**Run:** `06_c4.md`

**Required containers (recommended map):**

| Container | Role |
|---|---|
| Advisory API / CLI | Request envelope, authZ, budgets |
| Deterministic reconciliation engine | Workflow A/B/C rules |
| Ontology/semantic service | Concept resolve, unit/MedDRA/IDMP policy |
| Evidence KG store (offline) | Multi-hop paths with provenance |
| Agent runtime | Tool loop; never bypasses policy_guard |
| Inference adapter | Optional; kill switch |
| Policy guard + contract validator | Fail-closed |
| HITL workbench (`submission/app`) | Human review |
| Audit/evidence export | Append-only |

Also: degraded/offline view; prohibited write paths; `ADR_CANDIDATES.md`.

**Exit gate:** map matches DDD + features; provisional if DDD provisional.

**Sync:** `10_C4_ARCHITECTURE.md`; structure hints for `12`.

---

### Step 7 — Prompt 07 ADRs → `07_adrs/`  ★ pipeline stop for “through ADR”

**Run:** `07_adrs.md` + package #5 review

**Mandatory ADR themes (≥10 for scoring alignment):**

1. Deterministic-first + optional inference  
2. Offline evidence KG adopted (supersede D-205) + RER fallback  
3. Ontology/semantic as policy before retrieval  
4. Fail-closed contracts / `additionalProperties: false`  
5. Execution-time entitlement re-check  
6. Signed tool manifests only  
7. Agent budgets / stop / checkpoints  
8. No supply side effects  
9. HITL mandatory for readiness/options  
10. Kill switch isolates inference, not advisory continuity  
11. Identity/IDMP non-merge without stewardship  
12. Unit conversion only if approved mapping  

Plus: `ADR_INDEX.md`, `ARCHITECTURE_REVIEW.md` with `pass|conditional|fail`.

**Exit gate:** review `pass` or `conditional` with named conditions → may start Prompt 08.  
**If `fail`:** loop to Prompt 06/07 — do not code.

**Sync:** full `11_ADR_REGISTER.md`.

---

## 5. After ADR — SDD path to the agentic app (planned, not in “through ADR” stop)

| Step | Prompt | Output | Implementation target |
|---|---|---|---|
| 8 | `08_technical_design.md` | SRS APIs, KG schema, NFRs, errors | `08_technical_design/` + `evaluation` contracts under submission |
| 9 | `09_lean_dmaic.md` | Complete DMAIC Control plan | artefact `02`; feed 22–24 |
| 10 | `10_implementation_tasks.md` | Numbered tasks | `09_sdd_build/tasks/` |
| 11 | `11_product_and_build.md` | Code + tests | `submission/src`, `app`, `tests` |
| 12–13 | assurance + defence | Gates, runbooks, pitch | artefacts 13–30 |

**Build order inside Prompt 11 (tests first):**

1. Fix `supply_options` naming  
2. Evidence loader + ontology resolve  
3. KG edge ingest from CSV relationships (read-only)  
4. Engine A (INJ-021, INJ-024) → B → C  
5. Agent orchestrator calling engines/KG (policy_guard on every tool result)  
6. Thin workbench UI  
7. Scripts setup/run/test/evaluate/reset + AI_DISABLED runbook  

---

## 6. Quality gates (every step)

| Gate | Check |
|---|---|
| Evidence | Every material claim cites `case/`/`data/`/`knowledge/`/`source_documents/` or prior AgenticApp file |
| Classification | Fact vs derivation vs assumption vs question labeled |
| GxP | No prompt output authorizes prohibited actions |
| SDD | Layer does not invent later-layer content (PRD≠APIs; Features≠schemas; C4≠ADR rationale) |
| Sync | `_sync/SYNC_NN_to_artefacts.md` lists what changed in scored files |
| Tests-before-inference | No model-dependent path until ACs exist for that feature |

---

## 7. Effort estimate

| Block | Calendar (1–2 builders) |
|---|---|
| Steps 0–3 (Discovery→PRD) | 1–2 days |
| Step 4 (DDD+Ontology+KG) | 1–2 days |
| Steps 5–7 (Features→C4→ADR) | 2–3 days |
| **Subtotal through ADR** | **~5–7 days** |
| Steps 8–11 (SRS→working POC) | 5–8 days (Phase 5 budget) |
| Assurance + defence artefacts | 3–5 days |

---

## 8. Risks

| Risk | Mitigation |
|---|---|
| Parallel tree vs scoring | Sync discipline; artefacts remain scored SoT for `--final` |
| KG vs D-205 examiner challenge | Explicit ADR supersession + RER fallback + offline-only |
| Over-agency | FR-D budgets; policy_guard; contracts deny side effects |
| Rewriting strong Phase 0–4 docs | Reuse inventory; only deepen deltas |
| Generator overwrite | Ban unguarded `generate_phase2_to4.py` |
| Scope explosion (all 84 injects) | PRD out-of-scope; prove control themes + PUB fixtures |

---

## 9. Immediate next actions

1. Fill `00_plan/REUSE_FROM_PHASE0_4.md` and `EXECUTION_LOG.md`  
2. Execute **Prompt 01** → write `01_discovery/*`  
3. Gate → Prompt 02 SCQA → … through Prompt 07 ADR review  
4. Only after `ARCHITECTURE_REVIEW=pass|conditional`, run Prompt 08 and SDD build  

---

## 10. Success definition (pipeline through ADR)

- [ ] `01`–`07` folders complete with entry/exit criteria met  
- [ ] SCQA Answer clearly states agentic+ontology+KG advisory scope  
- [ ] Ontology + semantic layer + KG design with provenance and CQ proofs planned  
- [ ] Feature specs cover A/B/C + orchestrator + KG + HITL  
- [ ] C4 shows KG and agent containers without write-back to SoR  
- [ ] ≥10 ADRs including KG supersession of D-205  
- [ ] Architecture review recorded  
- [ ] Sync notes prepared for artefacts 01, 04–11  

When those boxes are checked, the repo is ready for **SDD technical design and agentic app implementation** under `submission/src` + `submission/app`.
