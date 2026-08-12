#!/usr/bin/env python3
"""Taipy console for the AEGIS-PHARMA deterministic support layer.

Optional UI — assessed mode remains stdlib-only via scripts/demo.py.
Run from submission/app:

    python -m pip install --no-deps taipy-gui==4.0.2
    python -m pip install -r requirements-ui.txt
    python taipy_app.py
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from taipy.gui import Gui, notify

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import clinical_protocol  # noqa: E402
import finops  # noqa: E402
import model_gateway  # noqa: E402
import privacy_gates  # noqa: E402
import reliability  # noqa: E402
import security_gates  # noqa: E402
import workflow_batch  # noqa: E402
import workflow_pv  # noqa: E402
import workflow_supply  # noqa: E402

# ---------------------------------------------------------------------------
# Tree helpers (id / label / children) for Taipy <|tree|>
# ---------------------------------------------------------------------------
_EMPTY_TREE = [
    {
        "id": "empty",
        "label": "No result yet — run the workflow",
        "children": [],
    }
]


def _leaf(nid: str, label: str, detail: str = "") -> dict[str, Any]:
    return {"id": nid, "label": label, "children": [], "_detail": detail or label}


def _branch(nid: str, label: str, children: list[dict[str, Any]], detail: str = "") -> dict[str, Any]:
    return {
        "id": nid,
        "label": label,
        "children": children,
        "_detail": detail or label,
    }


def _short(value: Any, limit: int = 72) -> str:
    text = " ".join(str(value).split())
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def _detail_for(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, (str, int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        lines = []
        for key, item in value.items():
            if key.startswith("_"):
                continue
            if isinstance(item, (dict, list)):
                lines.append(f"{key}: ({type(item).__name__}, {len(item)} items)")
            else:
                lines.append(f"{key}: {item}")
        return "\n".join(lines) if lines else "{}"
    if isinstance(value, list):
        if not value:
            return "[]"
        preview = []
        for idx, item in enumerate(value[:12]):
            preview.append(f"[{idx}] {_short(item, 90)}")
        if len(value) > 12:
            preview.append(f"… and {len(value) - 12} more")
        return "\n".join(preview)
    return str(value)


def _from_value(value: Any, nid: str, label: str | None = None) -> dict[str, Any]:
    title = label if label is not None else _short(value, 56)
    if isinstance(value, dict):
        kids = []
        for idx, (key, item) in enumerate(value.items()):
            if key.startswith("_"):
                continue
            kids.append(_from_value(item, f"{nid}.{idx}", str(key)))
        return _branch(nid, title, kids, _detail_for(value))
    if isinstance(value, list):
        if not value:
            return _leaf(nid, f"{title} (empty)", "No items")
        kids = []
        for idx, item in enumerate(value):
            if isinstance(item, dict):
                item_label = (
                    item.get("description")
                    or item.get("option_id")
                    or item.get("record_id")
                    or item.get("source")
                    or item.get("role")
                    or f"Item {idx + 1}"
                )
                kids.append(_from_value(item, f"{nid}.{idx}", _short(item_label, 64)))
            else:
                kids.append(_leaf(f"{nid}.{idx}", _short(item, 64), str(item)))
        return _branch(nid, f"{title} ({len(value)})", kids, _detail_for(value))
    return _leaf(nid, f"{title}: {_short(value, 48)}", f"{title}\n{_detail_for(value)}")


def _index_details(nodes: list[dict[str, Any]], out: dict[str, str] | None = None) -> dict[str, str]:
    store = out if out is not None else {}
    for node in nodes:
        store[node["id"]] = str(node.get("_detail") or node.get("label") or "")
        children = node.get("children") or []
        if children:
            _index_details(children, store)
    return store


def _collect_expand_ids(nodes: list[dict[str, Any]], depth: int = 0, limit: int = 1) -> list[str]:
    ids: list[str] = []
    if depth > limit:
        return ids
    for node in nodes:
        children = node.get("children") or []
        if children:
            ids.append(node["id"])
            ids.extend(_collect_expand_ids(children, depth + 1, limit))
    return ids


def _workflow_tree(result: dict[str, Any], root_label: str) -> tuple[list[dict[str, Any]], dict[str, str], list[str]]:
    preferred = [
        "readiness_state",
        "execution_status",
        "authorization",
        "human_review",
        "approval_required",
        "contradictions",
        "gaps",
        "abstentions",
        "duplicate_candidates",
        "options",
        "evidence",
        "applicable_documents",
        "audit",
        "no_side_effects",
    ]
    children: list[dict[str, Any]] = []
    seen: set[str] = set()
    for key in preferred:
        if key in result:
            children.append(_from_value(result[key], f"n.{key}", key.replace("_", " ")))
            seen.add(key)
    for key, value in result.items():
        if key in seen or key.startswith("_"):
            continue
        children.append(_from_value(value, f"n.{key}", key.replace("_", " ")))

    root = _branch("root", root_label, children, _detail_for({k: result.get(k) for k in ("request_id", "workflow", "as_of", "batch_id") if k in result}))
    tree = [root]
    details = _index_details(tree)
    expanded = ["root"] + _collect_expand_ids(children, depth=0, limit=0)
    return tree, details, expanded


def _gates_tree() -> tuple[list[dict[str, Any]], dict[str, str], list[str]]:
    gateway_kids = []
    for idx, (intended, lang) in enumerate(
        (
            ("batch evidence summarisation", "en"),
            ("case entity extraction", "en"),
            ("case entity extraction", "ar"),
        )
    ):
        model_id, reason = model_gateway.select_model(intended, lang)
        label = model_id or "abstain"
        gateway_kids.append(
            _leaf(
                f"gw.{idx}",
                f"{label} · {intended} / {lang}",
                f"Model: {label}\nIntended use: {intended}\nLanguage: {lang}\n\n{reason}",
            )
        )

    sel = reliability.select_runtime_mode("batch_review")
    runtime = _leaf(
        "rt.0",
        sel.mode.replace("_", " "),
        f"Mode: {sel.mode}\n\n{sel.reason}",
    )

    purpose = security_gates.check_purpose_limitation("NTG-DE", "NTG-IN", "general_review")
    tokens = security_gates.check_token_budget(980_000)
    auth = security_gates.check_live_authorization("contractor_77")
    sec_kids = []
    for idx, (title, decision) in enumerate(
        (
            ("Cross-affiliate (SEC-1)", purpose),
            ("Oversized tokens (SEC-2)", tokens),
            ("contractor_77 live IAM", auth),
        )
    ):
        status = "denied" if not decision.allowed else "allowed"
        sec_kids.append(
            _leaf(
                f"sec.{idx}",
                f"{status} — {title}",
                f"Status: {status}\nGate: {title}\n\n{decision.reason}",
            )
        )

    hold = privacy_gates.check_deletion_against_hold("S-301-044", "DSR-17")
    privacy = _leaf(
        "priv.0",
        f"{hold.action} — DSR-17 / S-301-044",
        f"Action: {hold.action}\nSubject: S-301-044\nRequest: DSR-17\n\n{hold.reason}",
    )

    ctx = clinical_protocol.resolve_protocol_context("S-301-044")
    clinical_kids = [
        _leaf(
            "clin.0",
            f"{ctx.action} · eligibility {ctx.eligibility_decision}",
            (
                f"Site approved: {ctx.site_approved_protocol}\n"
                f"Global current: {ctx.global_current_protocol}\n"
                f"Action: {ctx.action}\n"
                f"Eligibility: {ctx.eligibility_decision}\n\n"
                + "\n".join(f"• {flag}" for flag in ctx.flags)
            ),
        )
    ]

    tree = [
        _branch("g.gateway", "Model gateway", gateway_kids, "Fail-closed model selection against integrity evidence"),
        _branch("g.runtime", "Runtime / outage", [runtime], "INJ-082 / AI-disabled continuity path"),
        _branch("g.security", "Security", sec_kids, "Purpose, token budget, live IAM"),
        _branch("g.privacy", "Privacy · DSR vs hold", [privacy], "Deletion request checked against legal hold"),
        _branch("g.clinical", "Clinical protocol context", clinical_kids, "Site vs global protocol applicability"),
    ]
    details = _index_details(tree)
    expanded = [n["id"] for n in tree]
    return tree, details, expanded


def _lookup_detail(details: dict[str, str], selected: Any, fallback: str) -> str:
    if selected is None or selected == "":
        return fallback
    if isinstance(selected, dict):
        nid = selected.get("id")
        if nid in details:
            return details[nid]
        return selected.get("_detail") or selected.get("label") or fallback
    return details.get(str(selected), fallback)


# ---------------------------------------------------------------------------
# Initial state
# ---------------------------------------------------------------------------
user = "demo_user"
batch_id = "NCB204-B24071"
cases_raw = "PV-1001, PV-1014, PV-1009"
root_lot = "NCS310-S26033"

_sel0 = reliability.select_runtime_mode("batch_review")
_cost0 = finops.cost_per_successful_task("batch_review")

runtime_mode = _sel0.mode.replace("_", " ")
runtime_reason = _sel0.reason
cost_per_task = f"${_cost0.cost_per_successful_task_stated_usd:,.2f}"
human_undercount = "FLAGGED" if _cost0.human_review_undercount_flag else "ok"
human_undercount_class = "metric-value status-warn" if _cost0.human_review_undercount_flag else "metric-value status-ok"
finops_notes = "\n".join(f"• {n}" for n in _cost0.notes) if _cost0.notes else "No notes."

batch_summary = "Awaiting reconciliation"
batch_tree = list(_EMPTY_TREE)
batch_details_map: dict[str, str] = {"empty": "Run Reconcile to explore evidence, contradictions, gaps, and abstentions."}
batch_expanded: list[str] | bool = True
batch_sel = "empty"
batch_detail = batch_details_map["empty"]

pv_summary = "Awaiting PV packet"
pv_tree = list(_EMPTY_TREE)
pv_details_map: dict[str, str] = {"empty": "Build a PV packet to explore clusters, contradictions, and gaps."}
pv_expanded: list[str] | bool = True
pv_sel = "empty"
pv_detail = pv_details_map["empty"]

supply_summary = "Awaiting draft options"
supply_tree = list(_EMPTY_TREE)
supply_details_map: dict[str, str] = {"empty": "Generate draft options to explore scope, gaps, and approval path."}
supply_expanded: list[str] | bool = True
supply_sel = "empty"
supply_detail = supply_details_map["empty"]

gates_tree, gates_details_map, gates_expanded = _gates_tree()
gates_sel = gates_expanded[0] if gates_expanded else None
gates_detail = _lookup_detail(gates_details_map, gates_sel, "Select a gate node")


def _refresh_overview(state) -> None:
    sel = reliability.select_runtime_mode("batch_review")
    cost = finops.cost_per_successful_task("batch_review")
    state.runtime_mode = sel.mode.replace("_", " ")
    state.runtime_reason = sel.reason
    state.cost_per_task = f"${cost.cost_per_successful_task_stated_usd:,.2f}"
    state.human_undercount = "FLAGGED" if cost.human_review_undercount_flag else "ok"
    state.human_undercount_class = (
        "metric-value status-warn" if cost.human_review_undercount_flag else "metric-value status-ok"
    )
    state.finops_notes = "\n".join(f"• {n}" for n in cost.notes) if cost.notes else "No notes."


def on_reconcile_batch(state) -> None:
    bid = (state.batch_id or "").strip()
    if not bid:
        notify(state, "error", "Batch ID is required")
        return
    result = workflow_batch.reconcile_batch(bid, "ui-batch", state.user or "demo_user")
    tree, details, expanded = _workflow_tree(result, f"Batch {bid}")
    state.batch_summary = (
        f"{result.get('readiness_state', 'unknown')} · "
        f"{result.get('execution_status')} · "
        f"{result['human_review']['role']}"
    )
    state.batch_tree = tree
    state.batch_details_map = details
    state.batch_expanded = expanded
    state.batch_sel = "root"
    state.batch_detail = details.get("root", "")
    notify(state, "success", f"Reconciled {bid}")


def on_build_pv(state) -> None:
    case_ids = [c.strip() for c in (state.cases_raw or "").split(",") if c.strip()]
    if not case_ids:
        notify(state, "error", "At least one case ID is required")
        return
    result = workflow_pv.build_pv_response(case_ids, "ui-pv", state.user or "demo_user")
    tree, details, expanded = _workflow_tree(result, f"PV packet ({len(case_ids)} cases)")
    state.pv_summary = f"{result['human_review']['role']} · {', '.join(case_ids)}"
    state.pv_tree = tree
    state.pv_details_map = details
    state.pv_expanded = expanded
    state.pv_sel = "root"
    state.pv_detail = details.get("root", "")
    notify(state, "success", "PV packet built")


def on_generate_supply(state) -> None:
    lot = (state.root_lot or "").strip()
    if not lot:
        notify(state, "error", "Root lot is required")
        return
    result = workflow_supply.build_supply_response(
        "ui-supply", lot, "ui-supply", state.user or "demo_user"
    )
    tree, details, expanded = _workflow_tree(result, f"Supply draft · {lot}")
    side = "draft only" if result.get("no_side_effects") else "CHECK"
    role = result.get("approval_required", {}).get("role", "Supply Governance Board")
    state.supply_summary = f"{side} · approval: {role}"
    state.supply_tree = tree
    state.supply_details_map = details
    state.supply_expanded = expanded
    state.supply_sel = "root"
    state.supply_detail = details.get("root", "")
    notify(state, "success", f"Draft options for {lot}")


def on_batch_select(state) -> None:
    state.batch_detail = _lookup_detail(
        state.batch_details_map, state.batch_sel, "Select a node in the tree"
    )


def on_pv_select(state) -> None:
    state.pv_detail = _lookup_detail(state.pv_details_map, state.pv_sel, "Select a node in the tree")


def on_supply_select(state) -> None:
    state.supply_detail = _lookup_detail(
        state.supply_details_map, state.supply_sel, "Select a node in the tree"
    )


def on_gates_select(state) -> None:
    state.gates_detail = _lookup_detail(
        state.gates_details_map, state.gates_sel, "Select a gate node"
    )


def on_refresh_gates(state) -> None:
    _refresh_overview(state)
    notify(state, "info", "Overview refreshed from live evidence")


def on_recompute_gates(state) -> None:
    tree, details, expanded = _gates_tree()
    state.gates_tree = tree
    state.gates_details_map = details
    state.gates_expanded = expanded
    state.gates_sel = expanded[0] if expanded else None
    state.gates_detail = _lookup_detail(details, state.gates_sel, "Select a gate node")
    _refresh_overview(state)
    notify(state, "success", "Gates recomputed")


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
page_overview = """
<|part|class_name=panel|
<|AEGIS-PHARMA|text|class_name=brand-mark|>
# Evidence Support Console
<|Fail-closed drafts for human review. No disposition, no final PV decision, no stock action.|text|class_name=lede|>
<|Draft support only — humans remain accountable (EU QP / Safety Physician / Supply Governance Board).|text|class_name=notice|>
|>

<|part|class_name=panel|
## Session
Reviewer user id
<|{user}|input|class_name=fullwidth|>

<|layout|columns=1 1 1|gap=16px|
<|part|
<|Runtime mode|text|class_name=metric-label|>
<|{runtime_mode}|text|class_name=metric-value|>
|>
<|part|
<|Cost / successful task|text|class_name=metric-label|>
<|{cost_per_task}|text|class_name=metric-value|>
|>
<|part|
<|Human-review undercount|text|class_name=metric-label|>
<|{human_undercount}|text|class_name={human_undercount_class}|>
|>
|>

**Why this mode**
<|{runtime_reason}|text|>

**FinOps notes**
<|{finops_notes}|text|>

<|Refresh overview|button|on_action=on_refresh_gates|>
|>
"""

page_batch = """
<|part|class_name=panel|
<|WORKFLOW A|text|class_name=brand-mark|>
# Batch reconciliation
GxP evidence reconcile / cite / flag / abstain — never disposition.

Batch ID
<|{batch_id}|input|class_name=fullwidth|>
<|Reconcile batch|button|on_action=on_reconcile_batch|>
|>

<|part|class_name=panel|
### Status
<|{batch_summary}|text|class_name=metric-value|>

<|layout|columns=1 1|gap=18px|
<|
#### Result tree
Click any node to inspect details.
<|{batch_sel}|tree|lov={batch_tree}|expanded={batch_expanded}|value_by_id|filter|height=420px|width=100%|class_name=fullwidth|on_change=on_batch_select|>
|>
<|
#### Selected node
<|{batch_detail}|text|class_name=detail-box|>
|>
|>
|>
"""

page_pv = """
<|part|class_name=panel|
<|WORKFLOW B|text|class_name=brand-mark|>
# PV intake support
Extract / normalize / cluster / cite — no final seriousness, causality, or reportability.

Case IDs (comma-separated)
<|{cases_raw}|input|class_name=fullwidth|>
<|Build PV packet|button|on_action=on_build_pv|>
|>

<|part|class_name=panel|
### Status
<|{pv_summary}|text|class_name=metric-value|>

<|layout|columns=1 1|gap=18px|
<|
#### Result tree
<|{pv_sel}|tree|lov={pv_tree}|expanded={pv_expanded}|value_by_id|filter|height=420px|width=100%|class_name=fullwidth|on_change=on_pv_select|>
|>
<|
#### Selected node
<|{pv_detail}|text|class_name=detail-box|>
|>
|>
|>
"""

page_supply = """
<|part|class_name=panel|
<|WORKFLOW C|text|class_name=brand-mark|>
# Supply draft options
Recall-scope / shortage drafts only — no reserve, allocate, ship, or recall.

Root lot
<|{root_lot}|input|class_name=fullwidth|>
<|Generate draft options|button|on_action=on_generate_supply|>
|>

<|part|class_name=panel|
### Status
<|{supply_summary}|text|class_name=metric-value|>

<|layout|columns=1 1|gap=18px|
<|
#### Result tree
<|{supply_sel}|tree|lov={supply_tree}|expanded={supply_expanded}|value_by_id|filter|height=420px|width=100%|class_name=fullwidth|on_change=on_supply_select|>
|>
<|
#### Selected node
<|{supply_detail}|text|class_name=detail-box|>
|>
|>
|>
"""

page_gates = """
<|part|class_name=panel|
<|ASSURANCE|text|class_name=brand-mark|>
# Gates & live status
Fail-closed checks against challenge evidence. No side effects.

<|Recompute gates|button|on_action=on_recompute_gates|>
|>

<|part|class_name=panel|
<|layout|columns=1 1|gap=18px|
<|
#### Gate tree
<|{gates_sel}|tree|lov={gates_tree}|expanded={gates_expanded}|value_by_id|filter|height=460px|width=100%|class_name=fullwidth|on_change=on_gates_select|>
|>
<|
#### Selected gate
<|{gates_detail}|text|class_name=detail-box|>
|>
|>
|>
"""

pages = {
    "/": "<|navbar|>",
    "overview": page_overview,
    "batch": page_batch,
    "pv": page_pv,
    "supply": page_supply,
    "gates": page_gates,
}

if __name__ == "__main__":
    Gui(pages=pages, css_file="style.css").run(
        title="AEGIS-PHARMA Support Console",
        port=5050,
        dark_mode=False,
        run_browser=True,
        use_reloader=False,
    )
