# services/worker

Agent orchestrator: **LangGraph** StateGraph (`langgraph_orchestrator.py`) over signed tools, budgets, checkpoints, kill switch.

- Assessment: graph still runs if `langgraph` is installed; Azure is not called (`used=false`).
- Cloud: infer node uses Azure OpenAI via `InferencePort` (never source of truth).
- Missing `langgraph`: falls back to rules + stub suggest.

