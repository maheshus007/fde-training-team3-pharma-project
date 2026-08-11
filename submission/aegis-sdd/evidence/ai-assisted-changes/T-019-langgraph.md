# AI change record — LangGraph orchestrator

| Field | Entry |
|---|---|
| Specs | FR-D; ADR-AA-019; ADR-AA-005/009/016 |
| Files | `services/worker/langgraph_orchestrator.py`; `src/orchestrator/langgraph_agent.py`; `services/api/service.py`; tests |
| Decision | LangGraph StateGraph is the agent framework. Azure OpenAI remains InferencePort. Engines remain SoT. No free ReAct. |
| Tests | assessment suite + LangGraph node when package installed |
