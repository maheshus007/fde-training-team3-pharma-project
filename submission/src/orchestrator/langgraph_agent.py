"""Shim — canonical: aegis-sdd/services/worker/langgraph_orchestrator.py."""
from src._canon import load_canon

_mod = load_canon(
    "aegis_sdd_langgraph_orchestrator",
    "aegis-sdd/services/worker/langgraph_orchestrator.py",
)
run_langgraph = _mod.run_langgraph
langgraph_available = _mod.langgraph_available
ALLOWED_TOOL_NAMES = _mod.ALLOWED_TOOL_NAMES
WORKFLOW_TOOLS = _mod.WORKFLOW_TOOLS
