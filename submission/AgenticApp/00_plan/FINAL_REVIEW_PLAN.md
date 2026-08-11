# Final review plan — AEGIS AgenticApp

| Field | Entry |
|---|---|
| Date | 2026-08-11 |
| Verdict | **Ready to build.** Plan: `IMPLEMENTATION_PLAN.md`. Driver: `09_sdd_build/BUILD_SDD.md`. |
| Product stack | Azure OpenAI + Taipy + Cosmos Gremlin (`cloud`); stub + in-memory/RER (`assessment`) |

---

## 1. Are we good to start development?

**Yes — SDD build, Wave A.** Do not invent APIs; follow BUILD_SDD + TASK_INDEX.

| You can start now | You must not start yet |
|---|---|
| T-001 `supply_options` then T-002..T-008 | Engines A/B/C before GraphPort CQ tests |
| Assessment stubs (inference + memory graph) | Live Azure / Cosmos in CI |
| CQ-1/3/6 tests against GraphPort | Treating cloud as the only runtime |

---

## 2. Is SDD complete?

**Spec layers are done. Code is the remaining SDD layer.**

```text
DONE     Vision/PRD          03_prd/
DONE     Feature specs       05_feature_specs/ FR-A..F
DONE     Architecture (C4)   06_c4/
DONE     ADRs                07_adrs/
DONE     Technical design    08_technical_design/
DONE     Task catalog + SDD  09_sdd_build/BUILD_SDD.md + TASK_INDEX.md
NEXT     Implementation      submission/src, app, tests   (IMPLEMENTATION_PLAN.md)
LATER    DMAIC complete      artefact 02
LATER    Assurance/defence   artefacts 13–30
```

Also incomplete for scoring: sync AgenticApp → `submission/artefacts/`; empty `submission/app`, `evaluation`, `runbooks`; `--final` still FAIL.

---

## 3. What is already decided (do not re-litigate)

### Capability
Advisory Workflows A/B/C: batch evidence, PV intake support, supply **draft** options. Humans keep disposition, final PV, allocate/ship/recall, eligibility, formulation/spec.

### Product stack (2026-08-11)

| Layer | Product (`cloud`) | Assessment (default CI) |
|---|---|---|
| LLM | Azure OpenAI structured JSON | Inference stub |
| UI | Taipy | Taipy + mocks or JSON export |
| Graph | Cosmos DB Gremlin API | In-memory/RER `GraphPort` |
| Core | Python engines + `policy_guard` + JSON contracts | Same |

`AEGIS_RUNTIME_MODE=assessment|cloud|ai_disabled`. Default **`assessment`**. No secrets in git.

### Domain
DDD v2.0 + ontology/semantic + CQ-1..9. Graph is citeable evidence, not SoR. Forbidden Gremlin labels: reservation/allocation/shipment/disposition/signal_confirmed.

---

## 4. Conditions still open (architecture review)

| ID | Condition |
|---|---|
| O-1 | CQ-1/3/6 green on **assessment GraphPort** before claiming KG |
| O-2 | `supply_planning` → `supply_options` in policy_guard/tests |
| O-3 | Sync working tree into scored artefacts |
| O-4 | Update artefact 08 KG decision to dual-path (not silent D-205 delete) |
| O-5 | Do not claim BR-01 −14% (Unknown) |

---

## 5. Recommended sequence (final plan)

### Phase A — Finish SDD (before feature coding) — ~1–2 days

**Prompt 08** → `submission/AgenticApp/08_technical_design/`:

1. Runtime mode + env var names (no secret values)
2. Workflow request/response envelopes (reuse `evaluation/contracts/`)
3. InferencePort / GraphPort interfaces and error codes
4. Cosmos Gremlin vertex/edge labels + provenance properties
5. Taipy page map (batch / PV / supply / review ack) — no disposition buttons
6. NFRs: budgets, latency, kill switch, idempotency
7. Module layout matching C4_CODE_SKETCH
8. Traceability FR/AC → test IDs

**Prompt 10** → single catalog `09_sdd_build/TASK_INDEX.md` (Prompt 10 forbids `task-00N.md` files).

**Gate:** SRS review. Then code.

### Phase B — SDD build (`IMPLEMENTATION_PLAN.md`) — tests first

Order:

1. ADR-AA-012 naming fix  
2. Ports + assessment adapters (stub LLM, in-memory graph)  
3. CSV ingest → GraphPort (CQ-1, CQ-3 incl. PV-1009, CQ-6)  
4. Engine A (INJ-021, 023, 024, 028) → B → C  
5. Orchestrator + policy_guard on every tool result  
6. Taipy workbench (forced evidence view)  
7. Cloud adapters: Azure OpenAI, Cosmos Gremlin (optional demo)  
8. Scripts: setup / run / test / evaluate / reset  
9. Runbooks: SETUP, OPERATIONS, INCIDENT, AI_DISABLED  

### Phase C — Scoring wrap

- Prompt 09 DMAIC complete  
- Sync artefacts 01, 04–12, 08 KG decision  
- Artefacts 22–30, evaluation results, manifest, hashes  
- `python tools/check_submission_structure.py --final`

---

## 6. Definition of done (POC)

- Three workflows return schema-valid packs; prohibited fields fail closed  
- Taipy: cannot ack readiness without viewing conflicts  
- `assessment` mode: no Azure keys; tests green  
- `cloud` mode: documented env vars; structured LLM output still policy-checked  
- Cosmos/Gremlin (or memory port) cites paths; no forbidden write edges  
- Kill switch: LLM off, rules + review still work  
- `--final` structural check pass path is in sight (app, runbooks, scripts, artefacts 22–30)

---

## 7. Review checklist (for you)

- [ ] Accept dual-mode (`cloud` + mandatory `assessment`)  
- [ ] Confirm Azure OpenAI / Taipy / Cosmos Gremlin as product  
- [ ] Confirm **do not code engines until Prompt 08 SRS exists**  
- [ ] Confirm first code after SRS: ports + CQ tests, not UI chrome  
- [ ] Confirm no secrets committed  

If those boxes are OK, next action is **execute Prompt 08**, not a Taipy/Azure spike.
