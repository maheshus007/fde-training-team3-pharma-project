"""LangGraph agent runtime (FR-D). Rules packs stay source of truth; LLM never writes SoR."""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, TypedDict

_WORKER = Path(__file__).resolve().parent
_AEGIS = _WORKER.parents[1]
_DOMAIN = _AEGIS / "packages" / "domain"
_INTEGRATION = _AEGIS / "services" / "integration"
_SUBMISSION = _AEGIS.parent
_SRC = _SUBMISSION / "src"

for path in (_DOMAIN, _INTEGRATION, _SRC, _SUBMISSION):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from agent_runtime import (  # noqa: E402
    MAX_STEPS,
    MAX_TOOL_CALLS,
    BudgetTracker,
    bounded_suggest,
    kill_switch_on,
    select_inference,
)
from conflict_priority import notes_payload  # noqa: E402
from cosmos_gremlin import select_graph  # noqa: E402
from tool_catalog import ALLOWED_TOOL_NAMES, evaluate_manifest  # noqa: E402

WORKFLOW_TOOLS = {
    "batch_evidence": (
        "traverse_evidence_path",
        "find_conflicts",
        "assess_readiness",
        "get_provenance",
        "request_human_review",
    ),
    "pv_intake": (
        "propose_duplicate_candidates",
        "find_conflicts",
        "request_human_review",
    ),
    "supply_options": (
        "enumerate_draft_options",
        "find_conflicts",
        "request_human_review",
    ),
}


class AgentState(TypedDict):
    request: dict[str, Any]
    pack: dict[str, Any]
    steps: int
    tool_calls: int
    inference_used: bool
    tool_trace: list[str]
    termination: str
    suggestions: list[Any]


def langgraph_available() -> bool:
    try:
        import langgraph  # noqa: F401
        from langgraph.graph import END, START, StateGraph  # noqa: F401
    except Exception:
        return False
    return True


def _deny_unknown_tool(name: str) -> None:
    if name not in ALLOWED_TOOL_NAMES:
        raise ValueError(f"tool name not in approved catalog: {name}")


def _run_tool(name: str, request: dict[str, Any], pack: dict[str, Any]) -> str:
    _deny_unknown_tool(name)
    workflow = str(request.get("workflow") or "")
    if name == "find_conflicts":
        ids = [str(item.get("id")) for item in (pack.get("contradictions") or []) if item.get("id")]
        return f"find_conflicts:{len(ids)}"
    if name == "assess_readiness":
        return f"assess_readiness:{pack.get('readiness_state')}"
    if name == "get_provenance":
        n = len(pack.get("evidence") or [])
        return f"get_provenance:{n}"
    if name == "request_human_review":
        required = bool((pack.get("human_review") or {}).get("required"))
        return f"request_human_review:required={required}"
    if name == "propose_duplicate_candidates":
        n = len(pack.get("duplicate_candidates") or [])
        return f"propose_duplicate_candidates:{n}"
    if name == "enumerate_draft_options":
        n = len(pack.get("options") or [])
        return f"enumerate_draft_options:{n}:no_side_effects"
    if name in {"traverse_evidence_path", "resolve_concept"}:
        cq = "CQ-1" if workflow == "batch_evidence" else "CQ-6" if workflow == "supply_options" else "CQ-3"
        purpose = str((request.get("authorization") or {}).get("purpose") or "")
        as_of = str(request.get("as_of") or "2026-08-01T08:00:00Z")
        params: dict[str, Any]
        if cq == "CQ-1":
            params = {"batch_id": str(request.get("batch_id") or "")}
        elif cq == "CQ-6":
            params = {"shipment_id": str(request.get("event_id") or "")}
        else:
            params = {"case_ids": list(request.get("case_ids") or [])}
        result = select_graph().query(cq, params, purpose, as_of)
        return f"{name}:{cq}:paths={len(result.get('paths') or [])}"
    return f"{name}:noop"


def _node_tools(state: AgentState) -> dict[str, Any]:
    request = state["request"]
    pack = state["pack"]
    tools = WORKFLOW_TOOLS.get(str(request.get("workflow") or ""), ())
    trace = list(state.get("tool_trace") or [])
    calls = int(state.get("tool_calls") or 0)
    steps = int(state.get("steps") or 0) + 1
    for name in tools:
        if calls >= MAX_TOOL_CALLS or steps >= MAX_STEPS:
            return {
                "steps": steps,
                "tool_calls": calls,
                "tool_trace": trace,
                "termination": "budget",
            }
        trace.append(_run_tool(name, request, pack))
        calls += 1
        steps += 1
    return {
        "steps": steps,
        "tool_calls": calls,
        "tool_trace": trace,
        "termination": state.get("termination") or "tools_done",
    }


def _node_infer(state: AgentState) -> dict[str, Any]:
    request = state["request"]
    pack = state["pack"]
    if kill_switch_on(request) or str(os.environ.get("AEGIS_RUNTIME_MODE", "assessment")).lower() == "ai_disabled":
        return {"inference_used": False, "termination": "kill_switch", "suggestions": []}
    if state.get("termination") == "budget":
        return {}
    tracker = BudgetTracker()
    tracker.steps = int(state.get("steps") or 0)
    tracker.tool_calls = int(state.get("tool_calls") or 0)
    port = select_inference(request)
    out = bounded_suggest(port, "conflict_notes", notes_payload(pack), tracker, request)
    return {
        "inference_used": bool(out.get("used")),
        "suggestions": list(out.get("suggestions") or []),
        "steps": int(state.get("steps") or 0) + 1,
        "termination": "completed",
    }


def _route_after_tools(state: AgentState) -> str:
    if state.get("termination") == "budget":
        return "end"
    return "infer"


def build_graph() -> Any:
    from langgraph.graph import END, START, StateGraph

    graph = StateGraph(AgentState)
    graph.add_node("tools", _node_tools)
    graph.add_node("infer", _node_infer)
    graph.add_edge(START, "tools")
    graph.add_conditional_edges("tools", _route_after_tools, {"infer": "infer", "end": END})
    graph.add_edge("infer", END)
    return graph.compile()


def run_langgraph(request: dict[str, Any], pack: dict[str, Any], tracker: BudgetTracker) -> dict[str, Any]:
    """Execute allowlisted tools + optional Azure JSON. Does not mutate the workflow pack."""
    fallback = {
        "framework": "rules",
        "inference_used": False,
        "tool_trace": [],
        "termination": "langgraph_unavailable",
        "steps": tracker.steps,
        "tool_calls": tracker.tool_calls,
        "suggestions": [],
    }
    if not langgraph_available():
        port = select_inference(request)
        out = bounded_suggest(port, "conflict_notes", notes_payload(pack), tracker, request)
        fallback["termination"] = "completed"
        fallback["inference_used"] = bool(out.get("used"))
        fallback["suggestions"] = list(out.get("suggestions") or [])
        return fallback
    manifest = {
        "name": "batch_evidence_read",
        "sha256": "approvedhash001",
        "signed": True,
        "permissions": ["read"],
        "side_effects": False,
    }
    trusted = evaluate_manifest(manifest)
    if not trusted["allow"]:
        return {
            "framework": "langgraph",
            "inference_used": False,
            "tool_trace": [],
            "termination": "manifest_denied",
            "steps": tracker.steps,
            "tool_calls": tracker.tool_calls,
            "suggestions": [],
        }
    app = build_graph()
    result = app.invoke(
        {
            "request": request,
            "pack": pack,
            "steps": 0,
            "tool_calls": 0,
            "inference_used": False,
            "tool_trace": [],
            "termination": "",
            "suggestions": [],
        },
        {"recursion_limit": MAX_STEPS},
    )
    tracker.steps = int(result.get("steps") or tracker.steps)
    tracker.tool_calls = int(result.get("tool_calls") or tracker.tool_calls)
    return {
        "framework": "langgraph",
        "inference_used": bool(result.get("inference_used")),
        "tool_trace": list(result.get("tool_trace") or []),
        "termination": str(result.get("termination") or "completed"),
        "steps": tracker.steps,
        "tool_calls": tracker.tool_calls,
        "suggestions": list(result.get("suggestions") or []),
    }
