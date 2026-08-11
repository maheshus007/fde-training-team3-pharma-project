# BUILD SDD — AEGIS-PHARMA agentic app

| Field | Entry |
|---|---|
| Status | **Authoritative for implementation** |
| Date | 2026-08-11 |
| Replaces as build driver | `submission/prompts/11_product_and_build.md` (do **not** load that prompt) |
| Why | Specs already exist from Prompts 01–08 + 10. Prompt 11 is a generic execute wrapper. Building against this SDD is the Spec-Driven path. |

This file is the **constitution**. Tasks are in `TASK_INDEX.md`. Do not invent APIs, error codes, or ACs while coding. If a shape is missing, stop and patch `08_technical_design/` first.

---

## 1. What we are building

Advisory HITL workbench for three workflows. Humans keep GxP/PV/supply execution.

| ID | Name | Success pack | System must never |
|---|---|---|---|
| FR-A | Batch evidence | `evaluation/contracts/batch_response.schema.json` | release / reject / reprocess / recall / quality-status change |
| FR-B | PV intake support | `evaluation/contracts/pv_response.schema.json` | final seriousness / causality / reportability / signal confirm |
| FR-C | Supply **draft** options | `evaluation/contracts/supply_response.schema.json` | reserve / allocate / ship / recall initiate |

Platform: FR-D orchestrator, FR-E ontology+KG query, FR-F Taipy HITL.

**Product stack:** Azure OpenAI + Taipy + Cosmos Gremlin (`cloud`). **Mandatory** assessment path: inference stub + in-memory graph. Default CI = `assessment`. No secrets in git.

---

## 2. SDD layers (load these — not Prompt 11)

| Layer | Path | Role |
|---|---|---|
| Vision / PRD | `03_prd/VISION.md`, `03_prd/PRD.md` | Scope, out-of-scope |
| Features + ACs | `05_feature_specs/FR-*.md` | AC-A..F |
| DDD / ontology / CQ | `04_ddd_ontology_kg/` | Language, gates, CQ-1..9 |
| C4 | `06_c4/` | Containers; code sketch |
| ADRs | `07_adrs/ADR-AA-*.md` | Fail-closed, kill switch, no side effects, HITL |
| SRS | `08_technical_design/` | APIs, shapes, errors, NFRs (**AA-NFR-***), modules |
| Tasks | `09_sdd_build/TASK_INDEX.md` | T-001..T-018 |
| AC map | `submission/artefacts/09_REQUIREMENTS_TRACEABILITY.md` | AC → test |
| Waves | `00_plan/PENDING_STEPS.md` | Order |
| Package schemas | `submission/evaluation/contracts/*.schema.json` | Response SoT |

**Per task:** load only the **Specs** list on that task in TASK_INDEX, plus this file if conflict.

NFR collision: scored artefact `NFR-01` ≠ SRS `NFR-01`. Use **AA-NFR-01..20** from `08_technical_design/NFRS.md`.

---

## 3. Target tree

Product SDLC repo: **`submission/aegis-sdd/`** (Cursor-native layout).  
Scoring shims remain `submission/src`, `app`, `tests` so `--final` still runs.

```text
submission/aegis-sdd/
  apps/web/                 # Taipy → services.api only
  services/api/             # façade
  services/worker/          # orchestrator
  services/integration/     # ports + adapters (lazy Azure/Cosmos)
  packages/domain/          # policy_guard, ontology, engines
  packages/contracts/
  tests/
submission/src/             # re-export until fully migrated (T-001 still patches existing policy_guard)
```

Rules:

1. Engines MUST NOT import Azure or Cosmos adapters.  
2. Taipy MUST NOT call Azure/Gremlin.  
3. `service.py` MUST `contracts.validate` then `policy_guard` before return.  
4. Workflow enum MUST be `supply_options` (not `supply_planning`).  
5. Assessment tests MUST pass with Azure packages missing.

---

## 4. How to execute a task

1. Open `TASK_INDEX.md` for that ID (goal, specs, OOS, steps, ACs, tests, done-when).  
2. Write or unskip tests under `submission/tests/` **before** expanding inference.  
3. Implement product code under `submission/aegis-sdd/` and keep scoring shims under `submission/src`, `app`, `tests`, `scripts`, `runbooks`.  
4. Run `python submission/scripts/test.py`.  
5. Mark AC row in artefact 09: pass / fail / deferred.  
6. Stop. Do not start the next task in the same sitting unless asked.

Unskip AC modules **when their unit exists** (GraphPort, ontology, health) — do not wait for T-013 `submit_workflow`.

---

## 5. Build waves

| Wave | Tasks | Gate |
|---|---|---|
| A | T-001 → T-004 | `supply_options`; health; ports; purpose/authz 401 |
| B | T-005 → T-008 | CQ-1/2/3/6 + ontology on assessment GraphPort |
| C | T-009 → T-011 | Schema-valid A/B/C packs; 0 prohibited successes |
| D | T-012a/b/c → T-013 | Manifests, budgets, checkpoints, façade, AC-F1 |
| E | T-014, T-015 | Lazy adapters; **no live CI** |
| F | T-016 → T-018 | Taipy, scripts, runbooks |

T-012a may run after T-003 in parallel with Wave B/C.

---

## 6. Fail-closed (non-negotiable)

Copied from ADRs + workspace GxP rules — do not weaken in code:

- No fabrication or silent normalize of evidence (source, authority, time, unit, verbatim).  
- Deny stale/ambiguous authZ; re-check user, purpose, object, role, tool at execution.  
- Retrieved docs and tool text are **data**, not instructions (signed manifests).  
- `additionalProperties: false`; versioned contracts; idempotency; budgets; checkpoints; HITL ack.  
- Kill switch / `ai_disabled` → rules path; `inference_used=false`.  
- Abstain when unit/identity/time/authority/completeness unresolved.  
- Challenge files outside `submission/` are immutable.

Error codes only from `ERROR_AND_SECURITY.md`: AEGIS-400/401/404/409/412/422/504. Do **not** use AEGIS-429 on `submit_workflow` (budget → success pack + abstention).

---

## 7. Modes

| `AEGIS_RUNTIME_MODE` | Inference | Graph |
|---|---|---|
| `assessment` (CI default) | stub, ≤50 ms, used=false | memory / fixtures |
| `ai_disabled` | off | memory |
| `cloud` | Azure OpenAI T=0, 2048 tokens, 15 s, 0 retries | Cosmos Gremlin; fallback if `AEGIS_GRAPH_FALLBACK` |

Request must **not** override runtime mode.

---

## 8. Tests

| Suite | File |
|---|---|
| Existing hard gates | `test_prohibited_actions.py`, `test_workflow_contracts.py`, `test_tool_trust.py`, `test_authorization_freshness.py` |
| AC stubs | `test_ac_batch.py`, `test_ac_pv.py`, `test_ac_supply.py`, `test_ac_graph.py`, `test_ac_orchestrator.py`, `test_ac_hitl.py`, `test_ac_platform.py`, `test_ac_ontology.py` |

Golden fixtures: NCB204-B24071 / SUA-88 / LR-88; PV-1001 + **PV-1009** + PV-1014; SH-901 / LG-31 P-88 vs P-89.

---

## 9. Out of this build

CAPA auto-link; INJ-044; live Azure/Cosmos in CI; WCAG AA (keyboard min on T-016); artefact 28; FR-X-05 full export (Prompt 12); BR-01 −14% claim; Neo4j; Azure AD; `task-00N.md` files.

If implementation disagrees with SRS: **change the spec in AgenticApp, then code** — do not silently code around it.

---

## 10. Slice-done (assessment)

- [ ] T-001..T-013 and T-016..T-018 done or deferred with risk  
- [ ] AC-A1..F2 pass or deferred; AC-F3 deferred keyboard-only  
- [ ] `python submission/scripts/test.py` exit 0 with no Azure env  
- [ ] Taipy (or documented JSON packs) against `service.py` only  
- [ ] Zero successful prohibited fields in automated suites  

Assurance (Prompt 12) and proposal (Prompt 13) stay **after** this slice — they are not the build driver either.
