"""Shim — canonical: aegis-sdd/packages/domain/agent_runtime.py."""
from src._canon import load_canon

_mod = load_canon(
    "aegis_sdd_domain_agent_runtime",
    "aegis-sdd/packages/domain/agent_runtime.py",
)
MAX_STEPS = _mod.MAX_STEPS
MAX_TOOL_CALLS = _mod.MAX_TOOL_CALLS
MAX_INFERENCE_CALLS = _mod.MAX_INFERENCE_CALLS
MAX_TOKENS = _mod.MAX_TOKENS
TEMPERATURE = _mod.TEMPERATURE
kill_switch_on = _mod.kill_switch_on
select_inference = _mod.select_inference
BudgetTracker = _mod.BudgetTracker
attach_budget_abstention = _mod.attach_budget_abstention
bounded_suggest = _mod.bounded_suggest
KillSwitchInference = _mod.KillSwitchInference
inference_budget = _mod.inference_budget
