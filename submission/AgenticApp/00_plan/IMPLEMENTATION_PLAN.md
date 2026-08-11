# Implementation plan — AEGIS-PHARMA (SDD-driven)

| Field | Entry |
|---|---|
| Date | 2026-08-11 |
| Driver | `submission/AgenticApp/09_sdd_build/BUILD_SDD.md` |
| Tasks | `submission/AgenticApp/09_sdd_build/TASK_INDEX.md` |
| Specs | `submission/AgenticApp/` (PRD → features → C4 → ADR → SRS) |
| Code | Product: `submission/aegis-sdd/`. Shims: `submission/src`, `app`, `tests`, `scripts`, `runbooks` |
| CI mode | `assessment` (no Azure / Cosmos keys) |

Build against the SDD pack already produced (Prompts 01–08, 10). Load **BUILD_SDD + the current task’s spec list only**. Do not invent APIs, error codes, or ACs. Work only under `submission/`. Challenge evidence is immutable.

---

## Status

```text
DONE     Discovery / SCQA / PRD / DDD / ontology / KG
DONE     Feature specs FR-A..F
DONE     C4 + ADR-AA-* (architecture review: conditional, mapped to tasks)
DONE     SRS (08_technical_design)
DONE     Task catalog T-001..T-018 + AC stubs + BUILD_SDD
NEXT     After slice: Prompt 09 DMAIC / assurance artefacts / sync / `--final`
LATER    Full Lean/DMAIC workshop (artefact 02) — does not block T-001
LATER    Assurance artefacts 13–25  (after assessment slice is green)
LATER    Defence artefacts 26–30 + artefact sync + --final
```

---

## What the app is

Advisory HITL for three workflows. Humans keep execution.

| Workflow | Pack | Never |
|---|---|---|
| A batch evidence | `batch_response.schema.json` | disposition / recall / quality-status change |
| B PV intake support | `pv_response.schema.json` | final PV / signal confirmation |
| C supply **draft** options | `supply_response.schema.json` | reserve / allocate / ship |

Stack: Azure OpenAI + Taipy + Cosmos Gremlin (`cloud`). Assessment: stub inference + in-memory graph. Taipy talks only to `service.py`.

---

## Wave A — hygiene + ports (now)

| # | Task | Done when |
|---|---|---|
| 1 | **T-001** | `policy_guard` knows `supply_options`; `supply_planning` is unknown/deny |
| 2 | T-002 | `health()` + ErrorEnvelope; AA-NFR-12 |
| 3 | T-003 | InferencePort stub + empty GraphPort; no `openai` at import |
| 4 | T-004 | Fresh entitlement + purpose bind; stale/mismatch → AEGIS-401 |

## Wave B — graph + ontology (Measure-first)

| # | Task | Done when |
|---|---|---|
| 5 | T-005 | Fixture ingest; forbidden Gremlin labels rejected |
| 6 | T-006 | CQ-1, CQ-2, CQ-6 on GraphPort (`test_ac_graph`) |
| 7 | T-007 | CQ-3 includes PV-1001, **PV-1009**, PV-1014 |
| 8 | T-008 | Unit abstain, IDMP non-merge, MedDRA version kept |

T-012a (signed manifests) may run after T-003 in parallel.

## Wave C — engines

| # | Task | Done when |
|---|---|---|
| 9 | T-009 | Batch pack AC-A1..A7 |
| 10 | T-010 | PV pack AC-B1..B9 |
| 11 | T-011 | Supply pack AC-C1..C5; no IDMP silent merge |

## Wave D — orchestrator + façade

| # | Task | Done when |
|---|---|---|
| 12 | T-012a | Poisoned / unsigned tools denied |
| 13 | T-012b | Kill switch + budgets (abstain on submit, not AEGIS-429) |
| 14 | T-012c | Checkpoint resume + idempotency / 409 |
| 15 | T-013 | `submit_workflow` / ack / query / ingest; AC-F1 → 412 |

## Wave E — cloud adapters (lazy; live blocked)

| # | Task | Done when |
|---|---|---|
| 16 | T-014 | Azure adapter lazy; missing keys / hash mismatch → stub. **No live CI** |
| 17 | T-015 | Cosmos adapter lazy; CI stays on memory graph |

Assessment can ship without live T-014/T-015.

## Wave F — UI and `--final` names

| # | Task | Done when |
|---|---|---|
| 18 | T-016 | Four Taipy pages; no release/allocate/signal; bind `127.0.0.1` |
| 19 | T-017 | scripts: setup, run, test, evaluate, reset |
| 20 | T-018 | runbooks: SETUP, OPERATIONS, INCIDENT, AI_DISABLED |

---

## Slice exit (assessment)

- Non-blocked tasks done or deferred with risk  
- Artefact 09 AC rows: pass / fail / deferred (none silent)  
- `python submission/scripts/test.py` exit 0 without Azure env  
- Zero successful prohibited fields  
- UI (or documented JSON packs) only via `service.py`

---

## After the slice (not build)

| Stage | What |
|---|---|
| Lean/DMAIC (Prompt 09) | Finish artefact 02 DOWNTIME; optional anytime before assurance |
| Assurance | Artefacts 13–25; AC-F3 WCAG; export; threat |
| Proposal / defence | Artefacts 26–30; AgenticApp → scored artefact sync; `--final` |

---

## Out of build

CAPA auto-link · INJ-044 · live Azure/Cosmos in CI · WCAG AA (keyboard min on T-016) · artefact 28 during build · BR-01 −14% · Neo4j · Azure AD · autonomous GxP/PV/supply writes

---

## Execute next

**T-001 only**, then stop for review.

```text
NOW     T-001  supply_options in policy_guard
THEN    T-002 → T-008
THEN    T-009 → T-011  and  T-012a/b/c
THEN    T-013 → T-016 → T-017 → T-018
OPT     T-014 / T-015 lazy adapters
THEN    assurance → proposal → sync → --final
```
