# Feature — Shared Kernel

**Question this file answers:** What belongs in `aegis.shared`?

| Field | Entry |
|---|---|
| Feature ID | MF2 |
| Version / date | 1.0 / 2026-08-12 |

## Actor

All workflows and runtime (consumers of shared).

## Contents (move from flat src)

| Module | Role |
|---|---|
| `contracts.py` | Schema load/validate; prohibited field helper |
| `policy_guard.py` | Deny prohibited actions, tool/model trust, auth freshness |
| `security_gates.py` | Purpose limitation, token budget, live auth probes |
| `privacy_gates.py` | Deletion vs hold |
| `reliability.py` | Runtime mode selection (AI-disabled default) |
| `finops.py` | Cost-per-task reporting |
| `model_gateway.py` | Fail-closed model selection |
| `clinical_protocol.py` | Demo clinical context utility (not a workflow) |

## Rules

- Shared must not import `aegis.batch`, `aegis.pv`, `aegis.supply`, or `aegis.runtime`.
- Shared must not contain workflow-specific response builders.
- Later tool_registry (agentic) may be added to shared in the agentic track — not here.

## Acceptance criteria

- [ ] All listed modules live under `aegis/shared/`
- [ ] Boundary test fails if shared imports a workflow package
