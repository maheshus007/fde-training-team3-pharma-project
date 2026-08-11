# ADR-AA-019 — LangGraph as agent orchestrator

- **Status:** accepted (product agent runtime); assessment remains runnable without the package  
- **Decision:** FR-D orchestration is a **LangGraph** `StateGraph` (`tools` → `infer` → end). Nodes call allowlisted read tools and `InferencePort` (Azure OpenAI in `cloud`). Domain engines stay the source of truth.  
- **Not chosen:** free ReAct `create_react_agent` (unbounded tools / SoR risk).  
- **Guardrails:** signed manifests; max 20 steps; kill switch skips infer; pack not mutated by the graph; `additionalProperties` still false on workflow JSON.  
- **Assessment:** if `langgraph` is absent, submit falls back to rules + stub. CI must not require Azure.  
