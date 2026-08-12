# Technical Spec — File Migration Map

**Question this file answers:** Exactly which files move where, and which call sites change?

| Field | Entry |
|---|---|
| Spec ID | MT4 |
| Version / date | 1.0 / 2026-08-12 |
| Correction | V-FIX-02 |

## Source → destination

| From (`submission/src/`) | To |
|---|---|
| `workflow_batch.py` | `aegis/batch/workflow.py` |
| `workflow_pv.py` | `aegis/pv/workflow.py` |
| `workflow_supply.py` | `aegis/supply/workflow.py` |
| `contracts.py` | `aegis/shared/contracts.py` |
| `policy_guard.py` | `aegis/shared/policy_guard.py` |
| `security_gates.py` | `aegis/shared/security_gates.py` |
| `privacy_gates.py` | `aegis/shared/privacy_gates.py` |
| `reliability.py` | `aegis/shared/reliability.py` |
| `finops.py` | `aegis/shared/finops.py` |
| `model_gateway.py` | `aegis/shared/model_gateway.py` |
| `clinical_protocol.py` | `aegis/shared/clinical_protocol.py` |
| `__init__.py` (flat) | replace with `aegis/__init__.py` package docstring |

After move: delete the old flat files. No re-export stubs at old paths.

## Call sites to retarget

| Area | Files |
|---|---|
| App | `submission/app/demo.py`, `submission/app/taipy_app.py` |
| Tests | `test_workflow_contracts.py`, `test_prohibited_actions.py`, `test_authorization_freshness.py`, `test_tool_trust.py` |
| Scripts | `submission/scripts/test.py`, `evaluate.py`, `generate_phase2_to4.py` (`from src.*` blocks) |
| Graders | `schema_grader.py`, `security_grader.py`, `prohibited_action_grader.py`, `test_graders.py` (path + imports) |

## Grep done-when checklist

After migration, these patterns must return **no hits** under `submission/` (except specs/docs mentioning them):

- `import workflow_batch`
- `import workflow_pv`
- `import workflow_supply`
- `from src.policy_guard`
- `from src.contracts`
- `from src.`

Allowed: documentation under `modular-specs/` describing the old paths.
