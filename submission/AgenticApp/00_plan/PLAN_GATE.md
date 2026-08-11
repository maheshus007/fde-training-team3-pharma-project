# Plan gate — ready to build?

| Field | Entry |
|---|---|
| Date | 2026-08-11 |
| Verdict | **GO for T-001 only.** Not GO for unrestricted full-app coding. |
| Driver | `09_sdd_build/BUILD_SDD.md` + `00_plan/IMPLEMENTATION_PLAN.md` |

---

## Entry checklist

| Gate | Result | Evidence |
|---|---|---|
| Spec layers 1–3 (PRD, features, C4, ADR, SRS) | **PASS** | `AgenticApp/03`–`08` |
| ACs mapped to tests or deferral | **PASS** | artefact 09 Prompt 10 section |
| Architecture review not `fail` | **PASS** | **conditional**; O-1..O-5 mapped |
| Structural reopen | **PASS** | artefacts 10/11 `cleared` |
| T-001 specs exist on disk | **PASS** | MODULE_LAYERING rule 4; ADR-AA-012; `policy_guard.py`; `test_prohibited_actions.py` |
| Package schemas | **PASS** | `evaluation/contracts/` (repo root) + `submission/tests/fixtures/` fallback |
| Blocked items labeled | **PASS** | live Azure/Cosmos, CAPA, INJ-044, WCAG AA |
| Open ambiguities that would invent APIs on T-001 | **PASS** after lock below | alias handling |

T-001 lock (closes TASK_INDEX “or”): **canonical only.** `supply_options` gets supply prohibited rules. `supply_planning` → unknown workflow (deny). No silent alias.

---

## Why not “full build GO”

| Item | Effect |
|---|---|
| O-1 CQ-1/3/6 not green | Do not accept ADR-AA-015 until Wave B |
| O-3 artefact sync | Later; not T-001 |
| Full DMAIC (Prompt 09 workshop) | Not a code blocker |
| Engines / Taipy / Azure | After Wave A–B |
| `policy_guard` still `supply_planning` | **Expected** — that *is* T-001 |

---

Product SDLC tree: `submission/aegis-sdd/` (scaffold). T-001 still patches `submission/src/policy_guard.py` so existing tests keep running.

## T-001 scope (start now)

Change `check_workflow_payload` + supply cases in `test_prohibited_actions.py` to `supply_options`. Do not touch engines, Azure, or `generate_phase2_to4.py` in this sitting.

Done when: reserve/allocate/ship denied on `supply_options`; `python submission/scripts/test.py` still exit 0.

---

## Residual (labeled, not unmarked)

Azure deployment name · CAPA auto-link · INJ-044 · WCAG AA · PUB-09–15 · BR-01 % · no MCP/SAP.
