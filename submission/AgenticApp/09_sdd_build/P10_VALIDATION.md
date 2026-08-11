# Prompt 10 validation (blindspot audit)

| Field | Entry |
|---|---|
| Date | 2026-08-11 |
| First-pass verdict | **CONDITIONAL** — AC-A..F stubs exist, but entry/exit criteria and test-first sequencing had unmarked gaps |
| After this audit | Gaps below are **labeled and closed in catalog/stubs** (no feature code). Prompt 11 may start at T-001 |

## Prompt 10 Produce coverage

| Section | Required | First pass | After audit |
|---|---|---|---|
| A Task index / order | Ordered + Lean first | `TASK_INDEX.md` T-001..T-018 | Paths qualified; T-012 split a/b/c; Measure-first unskip gates |
| A AC→test in artefact 09 | Every in-scope AC or deferral | AC-A1..F3 only | + CQ-4/5/7/8/9, scored TEST-* aliases, NFR/GXP/SEC/PRI deferrals |
| B Task units (7 fields) | Goal/specs/OOS/steps/AC/tests/done | T-006 missing steps; specs were relative | Specs under `submission/AgenticApp/…`; T-006 steps added |
| C Task→FR→AC | Matrix | Missing | Added in TASK_INDEX |
| Lean notes in artefact 02 | Four questions | Present, incomplete must-fix list | T-002/T-004 purpose/INJ-070 added |
| Test stubs | `submission/tests/` | 6 files; no platform/ontology | `test_ac_platform.py`, `test_ac_ontology.py` |
| No `task-00N.md` tree | Forbidden | Honored | Honored |
| No feature code | Forbidden | Honored (`src/` unchanged) | Honored |
| Artefact 28 | Optional / Stage 7 | Correctly not created | Unchanged |

## Exit criteria

| Criterion | First pass | After audit |
|---|---|---|
| Architecture review conditional mapped to tasks | Partial (O-1, O-2, credentials). **O-3 sync, O-4 KG artefact, O-5 BR-01** unmarked | Mapped: O-3 → T-018/P12; O-4 → no-task; O-5 → no-task |
| Prompt 09 structural reopen `cleared` in artefacts 10/11 | **Fail** — `cleared-assumed` only in TASK_INDEX; **10/11 silent** | Recorded `cleared` in artefacts 10 and 11 |
| Full Prompt 09 DMAIC workshop | Pending (allowed: “do not re-run full P09”) | Still pending; not a structural reopen |
| Tasks cover governed slice A–F | Engines+ports+UI yes | Same + explicit deferrals |
| Every in-scope AC → test or deferral | AC-A..F yes; CQ-4/5/7/8/9 and scored TEST-* no | Closed in artefact 09 |
| Specs exist | Relative paths would 404 for Prompt 11 agent | Qualified |
| Lean first | T-001..008 before engines | Stub skipUnless no longer waits on T-013 façade for CQ |
| Blocked tasks explicit | T-014/015 live, CAPA, INJ-044 | + PUB-09–15, WCAG AA, FR-X-05 export, GXP-04/05, PRI-04/05 |
| One task ≈ one sitting | **T-009 (7 ACs) and T-012 (5 ACs) mega** | T-012 split a/b/c; T-009 kept as one engine with AC checklist (do not further split schema+conflicts) |
| No task-tree files | Pass | Pass |
| artefact 02 complete | Thin P10 notes only; full P09 incomplete | Honest: P10 lens complete; P09 full register still later |

## Blindspots found

| ID | Blindspot | Severity | Disposition |
|---|---|---|---|
| B-10-01 | Prompt 09 reopen gate not in artefacts `10`/`11` | Critical (entry/exit) | Appended `cleared` records |
| B-10-02 | EXECUTION_LOG claimed Prompt 10 **PASS** | Major (overclaim) | CONDITIONAL → closed after audit |
| B-10-03 | AC stubs `skipUnless submit_workflow` — CQ/ontology cannot go green until T-013 | Critical (Measure-first inverted) | Graph/ontology/platform skip on their modules |
| B-10-04 | T-002 cites `tests/test_ac_platform.py` — file missing | Major | Stub created |
| B-10-05 | T-008 has no test file (CQ-5 / unit_unapproved) | Major | `test_ac_ontology.py` |
| B-10-06 | CQ-4/5/7/8/9 not in artefact 09 AC table | Major | Mapped or deferred |
| B-10-07 | Scored artefact TEST-A-01.. vs AgenticApp AC-A1 dual IDs | Major (scoring confusion) | Alias table in artefact 09 |
| B-10-08 | AgenticApp NFR-01..20 collide with artefact 09 NFR-01..08 | Critical naming | Prefix **AA-NFR** in maps; do not merge IDs |
| B-10-09 | Specs listed as `08_technical_design/…` (path does not exist at repo root) | Major (Prompt 11 404) | Prefix `submission/AgenticApp/` |
| B-10-10 | T-006 missing implementation steps | Minor | Added |
| B-10-11 | Produce C Task→FR→AC missing | Major | Table in TASK_INDEX |
| B-10-12 | T-012 mega-task | Major | Split T-012a/b/c |
| B-10-13 | Purpose mismatch (BR-D5 / PRI-01) not a named test | Major | T-004 + `test_ac_d2` / platform purpose case |
| B-10-14 | INJ-070 hash pin only in existing tool_trust; T-014 tests omitted from 09 | Major | Mapped existing + T-014 stub note |
| B-10-15 | FR-X-05 audit export, GXP-04 INJ-031, GXP-05 legal hold, PRI-04/05, SEC-04/05 unmarked | Major | Explicit deferral (Prompt 12 / out of MVP) |
| B-10-16 | AC-F2 smoke gated on `ack_human_review` | Minor | Gate on `app/main.py` |
| B-10-17 | `FINAL_REVIEW_PLAN.md` still says `09_sdd_build/tasks/` | Minor | Corrected to TASK_INDEX |
| B-10-18 | DMAIC must-fix omitted T-002 health and T-014 hash-fallback | Minor | Patched |
| B-10-19 | `supply_planning` still in `policy_guard` | Info | Correct — T-001 is first Prompt 11 task; P10 must not implement |
| B-10-20 | Architecture O-3/O-4/O-5 not tasked | Minor | Mapped no-task / P12 |

## In-scope AC completeness (Prompt 05 FR-A..F)

| AC | Stub case | Gap after first pass |
|---|---|---|
| AC-A1..A7 | `test_ac_batch.py` | None (assertions still `fail` until T-009) |
| AC-B1..B9 | `test_ac_pv.py` | None |
| AC-C1..C5 | `test_ac_supply.py` | None |
| AC-D1..D5 | `test_ac_orchestrator.py` + existing trust/authz | Purpose-bind was implicit |
| AC-E1..E5 | `test_ac_graph.py` | Skip gate too late |
| AC-F1..F3 | `test_ac_hitl.py` | F3 deferred; F2 skip wrong |

## What Prompt 11 must not forget

1. T-001 first: `policy_guard` `supply_planning` → `supply_options` (unknown alias deny).  
2. Unskip AC modules **per task**, not after T-013 only.  
3. Never live-call Azure/Cosmos in CI (AA-NFR-09).  
4. Do not create `task-00N.md`.  
5. Do not claim BR-01 −14% (O-5).
