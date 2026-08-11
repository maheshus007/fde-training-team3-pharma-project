# Final plan — Build phase

| Field | Entry |
|---|---|
| Date | 2026-08-11 |
| Status | **GO — start T-001** |
| Method | Spec-Driven Development (implement to spec, test against AC) |
| Driver | `submission/AgenticApp/09_sdd_build/BUILD_SDD.md` |
| Tasks | `submission/AgenticApp/09_sdd_build/TASK_INDEX.md` |
| Product tree | `submission/aegis-sdd/` (SDLC layout) |
| Scoring shims | `submission/src`, `app`, `tests`, `scripts`, `runbooks` |
| Gate | `PLAN_GATE.md` — T-001 only, not unrestricted coding |

Work only under `submission/`. Do not move the product repo outside this tree. Do not invent APIs. If a shape is missing, patch `08_technical_design/` first.

---

## 1. Where we are

```text
DONE   Spec (PRD, FR-A..F, DDD, C4, ADR-AA, SRS)
DONE   Task catalog + AC stubs + BUILD_SDD
DONE   Product scaffold  submission/aegis-sdd/
NOW    Build Wave A — T-001
```

Assurance, DMAIC workshop, defence, `--final` are **after** this phase.

---

## 2. What we are building

Advisory HITL for A / B / C. Humans keep GxP, final PV, reserve-allocate-ship.

| Mode | Inference | Graph |
|---|---|---|
| `assessment` (CI default) | stub | in-memory |
| `ai_disabled` | off | in-memory |
| `cloud` | Azure OpenAI (lazy) | Cosmos Gremlin (lazy) |

Taipy (`apps/web`) talks only to `services/api`. No live Azure/Cosmos in CI.

---

## 3. Where code goes

| Work | Path |
|---|---|
| Product (SDLC image) | `submission/aegis-sdd/packages|services|apps/web` |
| Tests the package runs | `submission/tests` (may import from aegis-sdd) |
| T-001 this sitting | `submission/src/policy_guard.py` + `tests/test_prohibited_actions.py`, then mirror under `aegis-sdd/packages/domain` |

`apps/admin`, production infra, MCP/SAP, nested git: **no**.

---

## 4. Build waves (one task per run)

### Wave A — hygiene + ports

| Task | Done when |
|---|---|
| **T-001** | `supply_options` is the supply workflow; `supply_planning` unknown/deny; reserve/allocate/ship still fail-closed |
| T-002 | `health()` + ErrorEnvelope |
| T-003 | InferencePort stub + empty GraphPort; no `openai` import |
| T-004 | Entitlement + purpose re-check → AEGIS-401 |

### Wave B — graph + ontology (before engines)

| Task | Done when |
|---|---|
| T-005 | CSV ingest; forbidden edge labels rejected |
| T-006 | CQ-1, CQ-2, CQ-6 |
| T-007 | CQ-3 includes PV-1001, **PV-1009**, PV-1014 |
| T-008 | Unit abstain; IDMP non-merge; MedDRA version retained |

T-012a (manifests) may run after T-003.

### Wave C — engines

| Task | Done when |
|---|---|
| T-009 | Batch pack AC-A1..A7 |
| T-010 | PV pack AC-B1..B9 |
| T-011 | Supply pack AC-C1..C5 |

### Wave D — orchestrator + façade

| Task | Done when |
|---|---|
| T-012a | Poisoned/unsigned deny; **only** the eight allowlisted tools |
| T-012b | Kill switch + budgets; optional Azure JSON **after** rules (never SoT) |
| T-012c | Checkpoint + idempotency / 409 |
| T-013 | submit / ack / query / ingest; AC-F1 → 412; **≥1 audit record per submit** |

### Wave E — lazy cloud (optional for assessment ship)

| Task | Done when |
|---|---|
| T-014 | Azure adapter lazy; missing keys / hash mismatch → stub; **no live CI** |
| T-015 | Cosmos adapter lazy; CI stays on memory graph |

### Wave F — UI and `--final` names

| Task | Done when |
|---|---|
| T-016 | Four Taipy pages; no release/allocate/signal; bind `127.0.0.1` |
| T-017 | scripts: setup, run, test, evaluate, reset |
| T-018 | runbooks: SETUP, OPERATIONS, INCIDENT, AI_DISABLED |

---

## 5. How each task is run

1. Open BUILD_SDD + that task in TASK_INDEX (only listed specs).  
2. Unskip or add tests under `submission/tests/` first.  
3. Implement in `aegis-sdd` (T-001: existing `policy_guard` first).  
4. Keep scoring shim importable from `submission/src`.  
5. `python submission/scripts/test.py` exit 0.  
6. Mark AC row pass/fail/deferred in artefact 09.  
7. Stop unless asked to continue.

---

## 6. Build-phase exit

- [ ] T-001..T-013 and T-016..T-018 done or deferred with risk  
- [ ] AC-A1..F2 pass or deferred; AC-F3 keyboard-only  
- [ ] Tests green with **no** Azure env vars  
- [ ] Zero successful prohibited fields  
- [ ] UI only via API façade  
- [ ] Every submit appends audit (AA-NFR-13); FR-X-05 export pack still deferred  

Coverage audit: `BUILD_PHASE_VALIDATION.md`.  

Then: assurance artefacts → proposal → scored artefact sync → `--final`.

---

## 7. Out of this phase

CAPA auto-link · INJ-044 · live cloud in CI · WCAG AA · artefact 28 · BR-01 −14% · Neo4j · Azure AD · repo outside `submission/` · autonomous writes

---

## 8. Start here

**T-001 only.** Canonical `supply_options`. No alias. Then stop for review.
