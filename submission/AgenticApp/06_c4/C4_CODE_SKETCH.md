# C4 Level 4 — Code Sketch (riskiest paths)

| Module (planned) | Responsibility |
|---|---|
| `submission/src/policy_guard.py` | Exists — deny prohibited / stale / poisoned |
| `submission/src/contracts.py` | Exists — schema + additionalProperties |
| `submission/src/ontology.py` | Resolve concepts / policies |
| `submission/src/ports/inference.py` | InferencePort |
| `submission/src/adapters/azure_openai.py` | Azure OpenAI (`cloud`) |
| `submission/src/adapters/inference_stub.py` | Assessment / kill switch |
| `submission/src/ports/graph.py` | GraphPort |
| `submission/src/adapters/cosmos_gremlin.py` | Cosmos Gremlin (`cloud`) |
| `submission/src/adapters/graph_memory.py` | Assessment graph |
| `submission/src/engines/batch.py` | FR-A |
| `submission/src/engines/pv.py` | FR-B |
| `submission/src/engines/supply.py` | FR-C |
| `submission/src/agent/orchestrator.py` | FR-D |
| `submission/app/` (Taipy) | FR-F workbench |

Riskiest path: AgentPlanner → ToolDispatcher → KgQuery/Engine → PolicyGuard → SchemaValidator → AuditLogger.
