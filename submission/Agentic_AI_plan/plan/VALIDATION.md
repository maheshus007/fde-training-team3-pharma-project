# Validation Report — Spec-Driven Agentic Plan

| Field | Value |
|---|---|
| Subject | Spec-Driven Agentic Plan for AEGIS-PHARMA |
| Date | 2026-08-12 |
| Validator | Team 3 architecture review (agent-assisted) |
| Status | **Accepted with mandatory corrections** |
| Corrected plan | [`AGENTIC_PLAN.md`](AGENTIC_PLAN.md) |

## Method

Checked the draft plan against:

- Spec-Driven Development rules (one question per file; progressive ambiguity reduction)
- Binding evidence: `data/ai_use_boundaries.csv`, `data/tool_catalog.csv`, INJ-006/024/066/067/070/080/082
- Package contracts: `evaluation/contracts/*_response.schema.json` (`additionalProperties: false`)
- Existing controls: `submission/src/policy_guard.py`, `reliability.py`, `model_gateway.py`, `trajectory_grader.py`
- Eval suite S08 (`submission/evaluation/datasets/S08_agent_path_tool_authorization.json`)
- Workspace rule: work only under `submission/`; no autonomous regulated actions

## Findings

### Pass

| ID | Finding |
|---|---|
| V-OK-01 | Assist-only stance matches AI-use boundaries (reconcile/cite/flag/abstain; extract/normalize/cluster/cite; generate options). |
| V-OK-02 | Deterministic-first + kill switch matches ADR-001, ADR-002, ADR-011 and INJ-082. |
| V-OK-03 | Tool deny list matches INJ-066 and `check_tool_manifest`. |
| V-OK-04 | Trajectory bound ≤ 25 and `execution_status: not_executed` match `trajectory_grader.py`. |
| V-OK-05 | Offline mock adapter matches ADR-008 (no live cloud in assessed mode). |
| V-OK-06 | Modular monolith prerequisite is sound (workflows already have no code interdependency). |
| V-OK-07 | Spec layering (PRD → features → technical → architecture → tasks) follows the Spec-Driven framework. |

### Mandatory corrections (applied in AGENTIC_PLAN.md and technical specs)

| ID | Severity | Finding | Correction |
|---|---|---|---|
| V-FIX-01 | **Critical** | Draft plan put `trajectory` / `agent_annotations` on the core workflow response. Package schemas set `additionalProperties: false`, so those fields would fail assessed contract validation. | Use a **run envelope**: `core` = schema-valid workflow payload; `agent` = trajectory + annotations beside (not inside) `core`. Validate `core` against package contracts unchanged. |
| V-FIX-02 | High | `draft_supply_option` catalog row says "create draft only". Ambiguous whether that writes to SoR. | Spec: in-memory draft option objects only; never reserve/allocate/ship; `no_side_effects: true` on supply `core`. |
| V-FIX-03 | Medium | Original plan listed "write specs" as T-002 after code tasks started conceptually overlapping. | Specs authored in this folder now; T-002 is **review/sign-off** of specs; implementation starts T-003. |
| V-FIX-04 | Medium | ADR numbering: modular cut and agent layer both need ADRs. | ADR-013 = modular monolith; ADR-014 = assist-only agent envelope. |

### Residual risks (accepted)

| ID | Risk | Mitigation |
|---|---|---|
| V-RISK-01 | Novel tool permission aliases may evade string checks | Keep deny-by-default; extend `WRITE_LIKE_PERMISSIONS` via tests |
| V-RISK-02 | Automation bias if UI over-emphasizes annotations | Forced human_review acknowledgements (INJ-071); `authoritative: false` required |
| V-RISK-03 | Modular cut not yet in code | T-001 blocks agent package work |

## Verdict

The plan is **valid to implement** after applying V-FIX-01..04. Do not implement agent fields on package-contract response objects.
