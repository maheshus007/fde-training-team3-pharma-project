# Prompt 10 — Implementation task index

> Prompt 10 forbids a `tasks/task-00N.md` tree. This **single** index is the working catalog. Execute in order per `BUILD_SDD.md` / `00_plan/IMPLEMENTATION_PLAN.md`.

| Field | Entry |
|---|---|
| Status | Ready for SDD build (after P10_VALIDATION) |
| Architecture review | **conditional** — O-1 → T-006/T-007; O-2 → T-001; O-3 → T-018/Prompt 12; O-4 no-task; O-5 no-task (do not claim BR-01 %); credentials → T-014/015 live blocked |
| Prompt 09 structural reopen | **cleared** in artefacts `10`/`11` (2026-08-11). Full Prompt 09 DMAIC workshop still pending — not a C4/ADR reopen |
| Specs root | `submission/AgenticApp/` unless path starts with `submission/src`, `submission/tests`, `submission/artefacts`, `submission/evaluation` |
| NFR IDs | Use **AA-NFR-01..20** for `08_technical_design/NFRS.md`. Do not confuse with scored artefact 09 `NFR-01..08` |

## Execution order

| ID | Goal | Depends | Status |
|---|---|---|---|
| T-001 | Canonical `supply_options` in policy_guard + tests | — | **done** |
| T-002 | `service.health` + ErrorEnvelope helper | T-001 | **done** |
| T-003 | InferencePort + GraphPort + assessment stubs | T-002 | **done** |
| T-004 | Entitlement + purpose re-check (fixture) | T-002 | **done** |
| T-005 | In-memory graph ingest from CSVs | T-003 | **done** |
| T-006 | CQ-1, CQ-2, CQ-6 on GraphPort | T-005 | **done** |
| T-007 | CQ-3 (PV-1001/1009/1014) | T-005 | **done** |
| T-008 | Ontology gates (unit / IDMP / MedDRA version retain) | T-003 | **done** |
| T-009 | Engine A batch pack | T-004, T-006, T-008 | **done** |
| T-010 | Engine B PV pack | T-004, T-007, T-008 | **done** |
| T-011 | Engine C supply pack | T-004, T-006, T-008 | **done** |
| T-012a | Signed tool manifests (poisoned/unsigned deny) | T-003 | **done** |
| T-012b | Kill switch + step/tool/token budgets | T-003 | **done** |
| T-012c | Checkpoints + idempotency | T-012a, T-012b | **done** |
| T-013 | `service.py` submit / ack / query / ingest | T-009..T-011, T-012c | **done** |
| T-014 | Azure OpenAI adapter (lazy) + hash pin | T-003 | **done**; live call **blocked** on keys |
| T-015 | Cosmos Gremlin adapter (lazy) | T-005 | **done**; live call **blocked** on keys |
| T-016 | Taipy four pages | T-013 | **done** |
| T-017 | scripts setup/run/test/evaluate/reset | T-013 | **done** |
| T-018 | Runbook stubs SETUP/OPERATIONS/INCIDENT/AI_DISABLED | T-017 | **done** |

**Blocked (not handed to agent as guesswork):**

| ID | Block | Notes |
|---|---|---|
| T-014 live | Azure env | Assessment stub in T-003 is the shippable path |
| T-015 live | Cosmos env | Memory port is shippable |
| CAPA auto-link | open-blocked FR-A | no task |
| INJ-044 | PRD out of scope | no task |
| PUB-09–15 extra contracts | after assessment slice | no task in this slice |
| FR-X-05 inspection export pack | Prompt 12 | T-018 audit files only |
| GXP-04 INJ-031 validation-state | Prompt 12 unless fixture already in T-009 pack | no silent “validated” assumption |
| GXP-05 / PRI-03 legal hold delete | out of MVP | no delete API |
| PRI-04 residency / PRI-05 INJ-060 secondary use | flag-only if fixture present; no training pipeline | no task to build a trainer |
| SEC-04 exfil / SEC-05 OT allowlist | Prompt 12 threat | T-012a data-not-instructions already |

**Deferred with risk:** AC-F3 WCAG AA → T-016 keyboard-only; revisit Prompt 12.

## Task → FR → AC (Produce C)

| Task | FR | AC / control | Contract |
|---|---|---|---|
| T-001 | FR-C / FR-D | AC-C3, BR-D4, ADR-AA-012 | `policy_guard` + supply schema |
| T-002 | infra | AA-NFR-12 | ErrorEnvelope |
| T-003 | FR-D / FR-E | AC-D4 stub | InferencePort / GraphPort |
| T-004 | FR-D / FR-X-01 | AC-D2, CQ-9, BR-D5 purpose, PRI-01 | entitlements fixtures |
| T-005 | FR-E | AC-E4 | Graph ingest |
| T-006 | FR-E | AC-E1, E2, E3 (CQ-1/2/6) | `query_graph` / GraphPort |
| T-007 | FR-E / FR-B | AC-E5, AC-B2 graph layer | CQ-3 |
| T-008 | FR-E / FR-A / FR-B | AC-A3 gate, AC-B7 field, CQ-5 | `ontology.py` |
| T-009 | FR-A | AC-A1..A7 | `batch_response.schema.json` |
| T-010 | FR-B | AC-B1..B9; CQ-4 via AC-B4 | `pv_response.schema.json` |
| T-011 | FR-C | AC-C1..C5; CQ-7 via AC-C5 | `supply_response.schema.json` |
| T-012a | FR-D | AC-D1, CQ-8 | signed manifests |
| T-012b | FR-D | AC-D4; AA-NFR-03..07,14 | budgets / kill switch |
| T-012c | FR-D | AC-D3, AC-D5; AA-NFR-08 | checkpoint / idempotency |
| T-013 | FR-A..F façade | all submit ACs; AC-F1 | SRS §ops |
| T-014 | FR-D | AC-D4 cloud; INJ-070; AA-NFR-02,05..07,18 | Azure adapter lazy |
| T-015 | FR-E | AC-E4; fallback AA-NFR graph | Cosmos lazy |
| T-016 | FR-F | AC-F1, F2; F3 keyboard deferred AA | Taipy |
| T-017 | platform | AA-NFR-09,16 | scripts |
| T-018 | continuity | AC-A5/B6/C4 docs | runbooks |

---

## Task units

Each build run loads **only** the specs listed. Prefix relative design files with `submission/AgenticApp/`.

### T-001 — supply_options enum

1. **Goal:** policy_guard and prohibited tests use `supply_options`, not `supply_planning`.  
2. **Specs:** `submission/AgenticApp/08_technical_design/MODULE_LAYERING.md` rule 4; ADR-AA-012; `submission/src/policy_guard.py`; `submission/tests/test_prohibited_actions.py`.  
3. **Out of scope:** engines, Azure.  
4. **Steps:** replace workflow string; keep alias deny for `supply_planning` as unknown **or** map alias→canonical then apply supply rules (prefer canonical only).  
5. **ACs:** AC-C3, BR-D4.  
6. **Tests:** update existing prohibited supply tests to `supply_options`.  
7. **Done when:** those tests fail closed on reserve/allocate/ship; `supply_options` is a known workflow.

### T-002 — health + error envelope

1. **Goal:** `service.health()` and `make_error(code, message, request_id)` exist.  
2. **Specs:** `submission/AgenticApp/08_technical_design/SRS_API_CONTRACTS.md` §3; ERROR_AND_SECURITY; AA-NFR-12.  
3. **Out of scope:** submit_workflow engines.  
4. **Steps:** add `submission/src/service.py` with health; envelope additionalProperties false conceptually.  
5. **ACs:** AA-NFR-12.  
6. **Tests:** `submission/tests/test_ac_platform.py` health ≤ 200 ms; envelope keys only `error`.  
7. **Done when:** health returns mode=assessment, inference=stub, graph=memory (or unknown until T-003).

### T-003 — ports + stubs

1. **Goal:** InferencePort stub (≤50 ms, used=false); GraphPort protocol + empty memory graph.  
2. **Specs:** SRS_API_CONTRACTS §4–5; MODULE_LAYERING; ADR-AA-002/016.  
3. **Out of scope:** Azure/Cosmos imports.  
4. **Steps:** `submission/src/ports/inference.py`, `ports/graph.py`, `adapters/inference_stub.py`, `adapters/graph_memory.py` (empty). Lazy Azure module file may exist but must not import SDK at import time.  
5. **ACs:** AC-D4 kill-switch path (stub). AA-NFR-18 retries not in stub.  
6. **Tests:** `test_ac_platform.py` stub returns used false; importing `src.service` does not import `openai`.  
7. **Done when:** assessment path has no Azure dependency.

### T-004 — entitlements + purpose

1. **Goal:** execution-time re-check of user, purpose, object, role from fixtures.  
2. **Specs:** DATA_MODEL §8; `policy_guard.check_authorization_records`; FR-D AC-D2; ERROR AEGIS-401; SRS purpose enum.  
3. **Out of scope:** Azure AD.  
4. **Steps:** `adapters/entitlements.py` read users + stale cache; deny purpose mismatch (batch purpose on PV object).  
5. **ACs:** AC-D2; CQ-9; BR-D5; PRI-01.  
6. **Tests:** existing stale/revoked; add purpose-mismatch deny in `test_ac_platform.py`.  
7. **Done when:** revoked/stale/purpose-mismatch → AEGIS-401.

### T-005 — graph ingest

1. **Goal:** rebuild in-memory graph from challenge CSVs (read-only).  
2. **Specs:** DATA_MODEL vertices/edges; INTERNAL_OBJECT_SHAPES; ADR-AA-015/018 assessment port.  
3. **Out of scope:** Cosmos. Forbidden addE labels must raise.  
4. **Steps:** ingest genealogy, lab, icsr duplicates, shipments/loggers, idmp mappings.  
5. **ACs:** AC-E4.  
6. **Tests:** ingest_graph edge_count > 0; forbidden label rejected.  
7. **Done when:** deterministic rebuild from fixtures.

### T-006 — CQ-1, CQ-2, CQ-6

1. **Goal:** Graph queries for genealogy, unit map, cold-chain association.  
2. **Specs:** `submission/AgenticApp/08_technical_design/INTERNAL_OBJECT_SHAPES.md` §6; COMPETENCY_QUESTIONS; FR-E AC-E1, E2, E3.  
3. **Out of scope:** engines wrapping CQ into workflow packs.  
4. **Steps:** implement GraphPort `query` for CQ-1/2/6; unskip `test_ac_graph` on MemoryGraph (do **not** wait for `service.query_graph`).  
5. **ACs:** AC-E1, AC-E2, AC-E3.  
6. **Tests:** `submission/tests/test_ac_graph.py`.  
7. **Done when:** SUA-88 conflict, LR-88 abstain, SH-901 P-88 vs P-89 visible.

### T-007 — CQ-3 duplicates

1. **Goal:** duplicate candidate edges for PV-1001, PV-1009, PV-1014.  
2. **Specs:** FR-B AC-B2; INTERNAL_OBJECT_SHAPES §4.  
3. **Out of scope:** auto-merge.  
4. **ACs:** AC-E5, AC-B2 (graph layer).  
5. **Tests:** all three case ids appear in candidate pairs.  
6. **Done when:** no merge field emitted.

### T-008 — ontology gates

1. **Goal:** unit conversion abstain; IDMP non-merge; MedDRA version retained on structures.  
2. **Specs:** ONTOLOGY.md; SEMANTIC_LAYER; ADR-AA-011/013/014; FR-A BR-A3.  
3. **Out of scope:** OWL/RDF.  
4. **Steps:** `submission/src/ontology.py` — refuse unapproved unit maps; IDMP exact→alias→stop (no merge); retain MedDRA version on coding structs. Unskip `test_ac_ontology.py` when module imports.  
5. **ACs:** AC-A3 (gate), AC-B7 (version field exists), CQ-5.  
6. **Tests:** `submission/tests/test_ac_ontology.py` — unapproved map → `unit_unapproved`; CQ-5 NCB-204 ≠ NCB204-DE.  
7. **Done when:** `submission/src/ontology.py` used by engines.

### T-009 — engine A

1. **Goal:** batch_evidence success JSON for NCB204-B24071.  
2. **Specs:** FR-A entire; INTERNAL_OBJECT_SHAPES §2–3; batch_response.schema.json; STATE_TRANSITIONS readiness.  
3. **Out of scope:** disposition UI; inference required.  
4. **ACs:** AC-A1..A7.  
5. **Tests:** `tests/test_ac_batch.py`.  
6. **Done when:** schema valid; conflicted_evidence; unit abstain; OOS contradiction; QP gap; prohibited field rejected (reuse T-001).

### T-010 — engine B

1. **Goal:** pv_intake pack.  
2. **Specs:** FR-B; INTERNAL_OBJECT_SHAPES §4; pv_response.schema.json.  
3. **Out of scope:** final PV fields; INJ-044.  
4. **ACs:** AC-B1..B9.  
5. **Tests:** `tests/test_ac_pv.py`.  
6. **Done when:** schema valid; candidates+clocks+listedness+MedDRA; no merge; sensitive omit; social abstain; final_reportability rejected.

### T-011 — engine C

1. **Goal:** supply_options draft pack for SH-901 / shortage.  
2. **Specs:** FR-C; INTERNAL_OBJECT_SHAPES §5; `submission/evaluation/contracts/supply_response.schema.json`; ADR-AA-006. T-008 IDMP gate required so options do not silently merge NCB-204 / NCB204-DE.  
3. **Out of scope:** reservations.  
4. **ACs:** AC-C1..C5.  
5. **Tests:** `tests/test_ac_supply.py`.  
6. **Done when:** no_side_effects true; drafts only; association conflict; channel constraints; reservation_id rejected.

### T-012a — signed manifests

1. **Goal:** only signed/approved tools execute; poisoned/unsigned denied.  
2. **Specs:** FR-D; INTERNAL_OBJECT_SHAPES §7; ADR-AA-005; CQ-8.  
3. **Out of scope:** SoR writes; budgets.  
4. **Steps:** load approved manifest hash; treat retrieved tool text as data.  
5. **ACs:** AC-D1; CQ-8.  
6. **Tests:** `test_ac_orchestrator.test_ac_d1` + existing `test_tool_trust.py`.  
7. **Done when:** poisoned/unsigned deny.

### T-012b — kill switch + budgets

1. **Goal:** kill switch forces stub; step/tool/token caps enforced.  
2. **Specs:** ADR-AA-002/009/016; AA-NFR-03..07,14.  
3. **Out of scope:** Azure live calls.  
4. **Steps:** env kill switch; stop run with abstention (not AEGIS-429 on submit).  
5. **ACs:** AC-D4.  
6. **Tests:** `test_ac_d4_kill_switch`.  
7. **Done when:** kill_switch → inference used=false; over-budget → abstain, pack still schema-valid.

### T-012c — checkpoints + idempotency

1. **Goal:** resume and idempotency keys are replay-safe (no side effects exist).  
2. **Specs:** INTERNAL_OBJECT_SHAPES §8–9; AA-NFR-08; AC-D3/D5.  
3. **Out of scope:** SoR writes.  
4. **Steps:** store checkpoint; same key+hash replay; different hash → AEGIS-409.  
5. **ACs:** AC-D3, AC-D5.  
6. **Tests:** `test_ac_d3_checkpoint_resume`, `test_ac_d5_idempotency`.  
7. **Done when:** resume idempotent; 409 on payload mismatch.

### T-013 — service façade

1. **Goal:** submit_workflow / ack_human_review / query_graph / ingest_graph / health; validate+policy_guard before return.  
2. **Specs:** SRS_API_CONTRACTS; MODULE_LAYERING rules 2–3; ERROR envelope.  
3. **Out of scope:** Taipy; HTTP optional skip.  
4. **ACs:** all submit ACs via this entry; AC-F1 ack 412.  
5. **Tests:** integration via service; additionalProperties on success. Unskip batch/pv/supply AC classes when `submit_workflow` exists.  
6. **Done when:** Taipy can be bound to service only.

### T-014 — Azure OpenAI adapter

1. **Goal:** InferencePort cloud adapter, lazy import, T=0, 2048 tokens, timeout 15 s, 0 retries; INJ-070 hash pin.  
2. **Specs:** ADR-AA-016; SRS §4; ERROR model pin (`AZURE_OPENAI_MODEL_HASH`).  
3. **Out of scope:** making inference the source of truth.  
4. **ACs:** AC-D4; AA-NFR-02,05..07,18; SEC-03 / INJ-070.  
5. **Tests:** missing keys → stub; hash mismatch → stub; **no live network in CI**. Existing `test_tool_trust` model-hash cases remain.  
6. **Done when:** assessment tests pass without `openai` installed. Live demo optional/blocked.

### T-015 — Cosmos Gremlin adapter

1. **Goal:** GraphPort cloud adapter, lazy import, same CQ results as memory.  
2. **Specs:** ADR-AA-018; DATA_MODEL; AEGIS_GRAPH_FALLBACK.  
3. **Out of scope:** forbidden write edges.  
4. **ACs:** AC-E4; fallback.  
5. **Tests:** no `gremlinpython` in assessment; fallback flag.  
6. **Done when:** CI uses memory port only.

### T-016 — Taipy HITL

1. **Goal:** four pages; no release/allocate/signal buttons; ack disabled until conflicts viewed.  
2. **Specs:** FR-F; SRS §6; ADR-AA-017; AA-NFR-19 bind 127.0.0.1.  
3. **Out of scope:** WCAG AA.  
4. **ACs:** AC-F1, AC-F2, AC-F3 (keyboard assumed; WCAG AA deferred).  
5. **Tests:** `test_ac_f2` unskips when `submission/app/main.py` exists; no release/allocate/signal button labels; ack guard on service.  
6. **Done when:** `submission/app/main.py` runs against assessment service.

### T-017 — scripts

1. **Goal:** setup, run, test, evaluate, reset matching `--final` name patterns.  
2. **Specs:** DEPLOYMENT_NOTES; REPO_EXECUTION; AA-NFR-09.  
3. **Out of scope:** Docker.  
4. **ACs:** AA-NFR-09,16 (not scored artefact NFR-09).  
5. **Tests:** reset deletes only evidence idempotency/checkpoints/audit.  
6. **Done when:** filenames contain setup, run, test, evaluate, reset.

### T-018 — runbooks

1. **Goal:** four runbook files for `--final`.  
2. **Specs:** DEFINITION_OF_DONE; continuity CSV; AI_DISABLED.  
3. **Out of scope:** full artefact 25/28 rewrite.  
4. **ACs:** continuity AC-A5/B6/C4 (docs + T-009..011 ai_disabled).  
5. **Tests:** none (doc).  
6. **Done when:** SETUP, OPERATIONS, INCIDENT, AI_DISABLED exist under `submission/runbooks/`.

---

## Specs to load by default (every task)

Never load all 30 artefacts. Always allowed: `submission/AgenticApp/08_technical_design/P08_VALIDATION.md` and `submission/AgenticApp/09_sdd_build/P10_VALIDATION.md` if conflict.

Lean: T-001..T-008 are Measure-first / must-fix-before-engines. T-012a may proceed in parallel with engines (manifests do not need packs). T-014/015 live calls are Model-waste if done before T-009. Audit: `P10_VALIDATION.md`.
