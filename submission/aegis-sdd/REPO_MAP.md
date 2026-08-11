# Repository map

Image SDLC folders → AEGIS meaning. Specs stay in `submission/AgenticApp/`; this tree is the **product**.

| Folder | AEGIS use | Scoring shim |
|---|---|---|
| `docs/product` | Pointers to PRD / features | — |
| `docs/architecture` | Pointers to C4 / SRS | — |
| `docs/adr` | Pointers to ADR-AA-* | — |
| `plans/active` | Build waves | `../AgenticApp/00_plan/IMPLEMENTATION_PLAN.md` |
| `apps/web` | Taipy HITL (FR-F) | `submission/app` |
| `apps/admin` | **Out of scope** (no second UI) | — |
| `services/api` | `service.py` façade | `submission/src/service.py` |
| `services/worker` | Orchestrator | `submission/src/agent/` |
| `services/integration` | Inference/Graph adapters | `submission/src/adapters/` |
| `packages/domain` | policy_guard, ontology, engines | `submission/src/` |
| `packages/contracts` | Schema validation | `submission/src/contracts.py` |
| `packages/config` | Runtime mode env | — |
| `packages/observability` | Audit append | `submission/evidence` |
| `tests/*` | Unit/contract/integration | `submission/tests` (runner) |
| `quality/gates` | `test.py` exit 0 without Azure | `submission/scripts/test.py` |
| `security/policies` | Fail-closed, purpose-bind | ADR-AA + policy_guard |
| `security/secrets` | Empty; never commit keys | — |
| `infra/environments/local` | Assessment | default |
| `infra/environments/assessment` | CI / `--final` | default |
| `infra/environments/dev\|staging\|production` | **Placeholders only** — not this POC | — |
| `deploy/*` | Out of MVP (no Docker required) | — |
| `ops/runbooks` | SETUP / OPERATIONS / INCIDENT / AI_DISABLED | `submission/runbooks` |
| `evidence/*` | Inspection packs | `submission/evidence` |
| `templates/*` | Change / ADR / test / threat stubs | — |
| `workshop/*` | Parent capstone is the workshop | `submission/` |
| `.cursor/` | Product rules (optional) | parent `.cursor/rules` |

T-001 still patches existing `submission/src/policy_guard.py`, then domain package mirrors it.
