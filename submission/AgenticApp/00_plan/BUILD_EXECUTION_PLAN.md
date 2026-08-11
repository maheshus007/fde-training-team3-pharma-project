# Build phase — execution plan

| Field | Entry |
|---|---|
| Date | 2026-08-11 |
| Now | **SDD build complete (T-001..T-018)** |
| Spec | `09_sdd_build/BUILD_SDD.md` + current row in `TASK_INDEX.md` |
| What / why | `BUILD_PHASE_PLAN.md` |
| Coverage | `BUILD_PHASE_VALIDATION.md` |

One task per sitting. Load only that task’s spec list. After each sitting: `python submission/scripts/test.py` then **stop**.

Work under `submission/` only. Product code → `aegis-sdd/` (after T-001, re-export from `src`). No live Azure/Cosmos. No invented APIs.

---

## Per-sitting ritual

1. Read BUILD_SDD §4–6 and the **one** TASK_INDEX unit.  
2. Tests first (`submission/tests/`).  
3. Implement.  
4. Run `python submission/scripts/test.py` (no Azure env).  
5. Update artefact 09 AC row: pass / fail / deferred.  
6. Fill `aegis-sdd/templates/ai-change-record.md` for that task.  
7. Stop unless told to continue.

---

## Sitting order

### Sitting 1 — T-001 (start here)

| | |
|---|---|
| Goal | Canonical `supply_options` |
| Files | `submission/src/policy_guard.py`, `submission/tests/test_prohibited_actions.py`; mirror `aegis-sdd/packages/domain` |
| Specs | MODULE_LAYERING rule 4; ADR-AA-012 |
| Lock | `supply_planning` = unknown (deny). No alias. |
| Done | Reserve/allocate/ship denied on `supply_options`; suite green |

### Sitting 2 — T-002

Health + ErrorEnvelope. `aegis-sdd/services/api` + shim `src/service.py`. Unskip `test_ac_platform` health.

### Sitting 3 — T-003

InferencePort stub + empty GraphPort. `services/integration`. No `openai` import. Unskip stub import test.

### Sitting 4 — T-004

Entitlement + purpose → AEGIS-401. Can run same day as T-002 (depends T-002 only).

---

### Sitting 5 — T-005  **(create the knowledge graph)**

Ingest challenge CSVs into memory graph. Forbidden edge labels raise. `ingest_graph` edge_count > 0.

### Sitting 6 — T-006

CQ-1, CQ-2, CQ-6 on GraphPort. Unskip `test_ac_graph` E1–E3.

### Sitting 7 — T-007

CQ-3: PV-1001, **PV-1009**, PV-1014. No merge.

### Sitting 8 — T-008

Ontology: unit abstain, IDMP non-merge, MedDRA version. Unskip `test_ac_ontology`.

**Optional parallel after sitting 3:** T-012a (signed manifests).

**Gate:** CQ-1/3/6 green before claiming the KG (architecture O-1).

---

### Sitting 9 — T-009

Engine A — batch pack AC-A1..A7. Unskip `test_ac_batch`.

### Sitting 10 — T-010

Engine B — PV pack AC-B1..B9. Unskip `test_ac_pv`.

### Sitting 11 — T-011

Engine C — supply pack AC-C1..C5. Unskip `test_ac_supply`.

---

### Sitting 12 — T-012a

Eight allowlisted tools only; poisoned/unsigned deny.

### Sitting 13 — T-012b

Kill switch + budgets. Optional Azure JSON **after** rules; never SoT. Abstain on budget (not AEGIS-429).

### Sitting 14 — T-012c

Checkpoints + idempotency / 409.

### Sitting 15 — T-013

Façade: submit / ack / query / ingest / health. AC-F1 → 412. **≥1 audit record per submit.** Unskip remaining submit AC tests.

---

### Sitting 16 — T-014 (optional for assessment ship)

Lazy Azure OpenAI. Missing keys / hash mismatch → stub. **No live CI.**

### Sitting 17 — T-015 (optional for assessment ship)

Lazy Cosmos Gremlin. CI stays on memory graph.

---

### Sitting 18 — T-016

Taipy four pages in `aegis-sdd/apps/web` → shim `submission/app`. No release/allocate/signal. Bind `127.0.0.1`.

### Sitting 19 — T-017

scripts: setup, run, test, evaluate, reset.

### Sitting 20 — T-018

runbooks: SETUP, OPERATIONS, INCIDENT, AI_DISABLED.

---

## Sequence (copy)

```text
1     T-001     supply_options          STOP
2     T-002     health
3     T-003     ports empty
4     T-004     authz + purpose
5     T-005     KG ingest (create graph)
6-8   T-006 T-007 T-008   CQ + ontology
9-11  T-009 T-010 T-011   engines A B C
12-14 T-012a/b/c          agent loop
15    T-013     service + audit + HITL ack
16-17 T-014 T-015         lazy cloud (optional)
18-20 T-016 T-017 T-018   UI scripts runbooks
```

T-004 may follow T-002 without waiting for T-003. T-008 may follow T-003 in parallel with T-005. T-009 waits for T-004 + T-006 + T-008.

---

## Do not do during build sittings

Live Azure/Cosmos calls · engines before CQ tests · Taipy before T-013 · repo outside `submission/` · MCP/SAP · admin app · CAPA auto-link · invent error codes

---

## Build complete when

`python submission/scripts/test.py` exit 0, no Azure env, AC-A1..F2 pass or deferred, prohibited successes = 0, Taipy (or JSON packs) only via façade.

Then stop build. Assurance / defence are a later phase.
