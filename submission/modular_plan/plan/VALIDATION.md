# Validation Report — Modular Monolith Plan

| Field | Value |
|---|---|
| Subject | Modular monolith restructure for AEGIS-PHARMA |
| Date | 2026-08-12 |
| Validator | Team 3 architecture review (agent-assisted) |
| Status | **Accepted with mandatory corrections** |
| Corrected plan | [`MODULAR_PLAN.md`](MODULAR_PLAN.md) |
| Source draft | Cursor plan `modular_monolith_restructure` |

## Method

Checked the draft against:

- Spec-Driven Development rules (one question per file; progressive ambiguity reduction)
- Current code: flat `submission/src/*.py` (12 modules); workflows have **no** cross-imports
- Call sites: `demo.py`, `taipy_app.py`, tests (`from src.*`), graders (`sys.path` + bare/`src` imports), scripts
- Project AGENTS.md: no backward-compat shims; simplest working structure
- Workspace rule: work only under `submission/`
- Alignment with agentic track [`../../specs/plan/AGENTIC_PLAN.md`](../../specs/plan/AGENTIC_PLAN.md) (ADR-013 vs ADR-014)

## Findings

### Pass

| ID | Finding |
|---|---|
| V-OK-01 | Modular monolith (single process) matches offline POC and ADR-008; microservices would be unjustified. |
| V-OK-02 | Natural cut is correct: batch / PV / supply are independent today; shared gates are cross-cutting. |
| V-OK-03 | Keeping public function signatures preserves contract/fixture stability. |
| V-OK-04 | AST boundary test is the right enforcement (structure without rules is just folders). |
| V-OK-05 | No import shims aligns with AGENTS.md (“remove obsolete paths”). |
| V-OK-06 | Scope stays under `submission/`; challenge package untouched. |
| V-OK-07 | Out-of-scope items (dashboard rewrite, business-logic rewrite) are appropriate. |

### Mandatory corrections (applied in MODULAR_PLAN.md and specs)

| ID | Severity | Finding | Correction |
|---|---|---|---|
| V-FIX-01 | High | Draft diagram lets app import workflows directly as the primary path; agentic architecture requires a composition root. | Prefer `aegis.runtime` as composition root; app may call `runtime` (preferred) or public package exports only during migration tasks, then converge on runtime. |
| V-FIX-02 | High | Graders/scripts insert `submission/src` and import bare `contracts` / `from src.policy_guard`. Move will break them unless every call site is retargeted. | Explicit migration map + dedicated tasks for tests, app, scripts, and graders. |
| V-FIX-03 | High | Agentic specs already assume `aegis.agents`. Creating agents in the modular cut mixes tracks. | This track creates `shared`, `batch`, `pv`, `supply`, `runtime` only. **Do not** add `agents/` here. |
| V-FIX-04 | Medium | `clinical_protocol` is clinical-specific but listed in shared. | Keep in `shared` for POC (demo-only utility); document as shared utility, not a fourth workflow. |
| V-FIX-05 | Medium | Draft “wire app” and “retarget imports” overlapped. | Split into ordered tasks: move → runtime → app → tests → scripts/graders → boundary test → ADR → verify. |
| V-FIX-06 | Low | ADR-013 must not collide with agentic ADR-014. | Modular track owns **ADR-013**; agentic track owns **ADR-014**. |

### Residual risks (accepted)

| ID | Risk | Mitigation |
|---|---|---|
| V-RISK-01 | Missed `from src.*` in `generate_phase2_to4.py` | Include generator in import grep done-when checklist |
| V-RISK-02 | Taipy optional; may be broken if not installed | Keep import updates; verify with `demo.py` + unittest path |
| V-RISK-03 | Someone implements agents before modular cut finishes | README sequencing; agentic T-001 depends on this track |

## Verdict

The modular plan is **valid to implement** after V-FIX-01..06. Current repo is still a flat monolith; independence of workflows makes the cut low-risk if call sites are fully retargeted.
