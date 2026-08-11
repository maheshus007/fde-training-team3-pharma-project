"""Taipy HITL workbench (T-016). Calls service.py only. Bind 127.0.0.1."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

_WEB = Path(__file__).resolve().parent
_AEGIS = _WEB.parents[1]
_SUBMISSION = _AEGIS.parent
_SRC = _SUBMISSION / "src"
for path in (_SRC, _SUBMISSION):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from src import service  # noqa: E402

HOST = "127.0.0.1"
PORT = int(os.environ.get("AEGIS_TAIPY_PORT") or "5000")

EVIDENCE_COLS = ["record_id", "source", "authority", "retrieved_at"]
CONFLICT_COLS = [
    "priority_label",
    "kind",
    "id",
    "left_source",
    "left_verbatim",
    "right_source",
    "right_verbatim",
    "advisory_note",
    "note_source",
]
GAP_COLS = ["id", "kind", "record_ref", "note"]
ABSTAIN_COLS = ["code", "reason", "record_ref"]
DUP_COLS = ["case_id_a", "case_id_b", "similarity", "reason"]
CLOCK_COLS = ["case_id", "channel", "timestamp", "timezone"]
LISTED_COLS = ["product_id", "source_doc", "jurisdiction", "listed", "risk"]
OPTION_COLS = ["option_id", "status", "summary", "constraint_ids"]
CONSTRAINT_COLS = ["constraint_id", "channel", "note"]
HOLD_COLS = ["batch_id_or_lot", "status"]

kill_switch = False
rules_banner = "Advisory workbench. Kill switch = rules only (no Azure narrative)."
batch_pack_json = ""
pv_pack_json = ""
supply_pack_json = ""
review_pack_json = ""
review_request_id = ""
viewed_conflict_ids = ""
ack_status = "Ack disabled until every conflict id is marked viewed."
selected_conflicts: list[str] = []
conflict_id_lov: list[str] = []

batch_banner = "Load a batch pack to see evidence, then readiness."
pv_banner = "Load a PV pack to see the case cluster. No final PV decision in this UI."
supply_banner = "Load draft supply options. No reserve / allocate / ship."
review_banner = "Load a workflow first. Conflicts must be viewed before acknowledgement."

batch_meta = ""
pv_meta = ""
supply_meta = ""
review_meta = ""

batch_evidence: dict[str, list[str]] = {c: [] for c in EVIDENCE_COLS}
batch_conflicts: dict[str, list[str]] = {c: [] for c in CONFLICT_COLS}
batch_gaps: dict[str, list[str]] = {c: [] for c in GAP_COLS}
batch_abstentions: dict[str, list[str]] = {c: [] for c in ABSTAIN_COLS}

pv_evidence: dict[str, list[str]] = {c: [] for c in EVIDENCE_COLS}
pv_conflicts: dict[str, list[str]] = {c: [] for c in CONFLICT_COLS}
pv_duplicates: dict[str, list[str]] = {c: [] for c in DUP_COLS}
pv_clocks: dict[str, list[str]] = {c: [] for c in CLOCK_COLS}
pv_listedness: dict[str, list[str]] = {c: [] for c in LISTED_COLS}

supply_evidence: dict[str, list[str]] = {c: [] for c in EVIDENCE_COLS}
supply_conflicts: dict[str, list[str]] = {c: [] for c in CONFLICT_COLS}
supply_constraints: dict[str, list[str]] = {c: [] for c in CONSTRAINT_COLS}
supply_options: dict[str, list[str]] = {c: [] for c in OPTION_COLS}
supply_holds: dict[str, list[str]] = {c: [] for c in HOLD_COLS}

review_conflicts: dict[str, list[str]] = {c: [] for c in CONFLICT_COLS}


def _cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=True)
    return str(value)


def as_table(rows: list[dict[str, Any]] | None, columns: list[str]) -> dict[str, list[str]]:
    data = {column: [] for column in columns}
    for row in rows or []:
        for column in columns:
            data[column].append(_cell(row.get(column)))
    return data


def flatten_conflicts(items: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item in items or []:
        left = item.get("left") or {}
        right = item.get("right") or {}
        out.append(
            {
                "priority_label": item.get("priority_label") or "",
                "kind": item.get("kind") or "",
                "id": item.get("id") or "",
                "left_source": left.get("source") or "",
                "left_verbatim": left.get("verbatim") or "",
                "right_source": right.get("source") or "",
                "right_verbatim": right.get("verbatim") or "",
                "advisory_note": item.get("advisory_note") or "",
                "note_source": item.get("note_source") or "",
            }
        )
    out.sort(key=lambda row: (str(row.get("priority_label") or "P9"), str(row.get("id") or "")))
    return out


def flatten_evidence(items: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    return [
        {
            "record_id": item.get("record_id") or "",
            "source": item.get("source") or "",
            "authority": item.get("authority") or "",
            "retrieved_at": item.get("retrieved_at") or "",
        }
        for item in (items or [])
    ]


def flatten_options(items: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item in items or []:
        ids = item.get("constraint_ids") or []
        out.append(
            {
                "option_id": item.get("option_id") or "",
                "status": item.get("status") or "draft",
                "summary": item.get("summary") or "",
                "constraint_ids": ", ".join(str(i) for i in ids) if isinstance(ids, list) else _cell(ids),
            }
        )
    return out


def conflict_ids_from_pack(pack: dict[str, Any]) -> list[str]:
    return [str(item.get("id")) for item in (pack.get("contradictions") or []) if item.get("id")]


def ack_enabled(pack: dict[str, Any] | None, viewed_raw: str) -> bool:
    if not pack or "error" in pack:
        return False
    needed = set(conflict_ids_from_pack(pack))
    viewed = {part.strip() for part in str(viewed_raw or "").split(",") if part.strip()}
    return needed.issubset(viewed)


def _error_banner(pack: dict[str, Any]) -> str:
    err = pack.get("error") or {}
    return f"Blocked: {err.get('code') or 'error'} — {err.get('message') or pack}"


def _meta(pack: dict[str, Any]) -> str:
    hr = pack.get("human_review") or {}
    return (
        f"request {pack.get('request_id') or '—'} · workflow {pack.get('workflow') or '—'} · "
        f"execution {pack.get('execution_status') or '—'} · human review required={hr.get('required')} "
        f"({hr.get('role') or 'reviewer'})"
    )


def _submit(request: dict[str, Any], state: Any | None = None) -> dict[str, Any]:
    switched = bool(getattr(state, "kill_switch", kill_switch) if state is not None else kill_switch)
    if switched:
        request = dict(request)
        request["kill_switch"] = True
    return service.submit_workflow(request)


def _sync_review(state: Any, pack: dict[str, Any]) -> None:
    state.review_pack_json = json.dumps(pack, indent=2)
    state.review_request_id = str(pack.get("request_id") or "")
    ids = conflict_ids_from_pack(pack)
    state.conflict_id_lov = ids
    state.selected_conflicts = []
    state.viewed_conflict_ids = ""
    state.review_conflicts = as_table(flatten_conflicts(pack.get("contradictions")), CONFLICT_COLS)
    if "error" in pack:
        state.review_banner = _error_banner(pack)
        state.review_meta = ""
        state.ack_status = "Ack disabled — pack error."
        return
    n = len(ids)
    state.review_banner = (
        f"{n} conflict(s) must be marked viewed before acknowledgement. No release / allocate / ship."
        if n
        else "No conflicts on this pack. Acknowledgement still records the human review."
    )
    state.review_meta = _meta(pack)
    state.ack_status = "Ack disabled until every conflict id is marked viewed." if n else "No conflicts — ack allowed."


def on_kill_switch(state: Any) -> None:
    if state.kill_switch:
        state.rules_banner = "KILL SWITCH ON — rules-only path. Azure inference skipped."
    else:
        state.rules_banner = "Advisory workbench. Kill switch = rules only (no Azure narrative)."


def submit_batch(state: Any) -> None:
    pack = _submit(
        {
            "request_id": "UI-BATCH-1",
            "idempotency_key": "idem-ui-batch-01",
            "as_of": "2026-08-01T08:00:00Z",
            "workflow": "batch_evidence",
            "batch_id": "NCB204-B24071",
            "authorization": {
                "user": "qp_eu_1",
                "purpose": "batch_review_readiness",
                "object_id": "NCB204-B24071",
                "role": "qualified_person",
            },
        },
        state,
    )
    state.batch_pack_json = json.dumps(pack, indent=2)
    if "error" in pack:
        state.batch_banner = _error_banner(pack)
        state.batch_meta = ""
        _sync_review(state, pack)
        return
    readiness = pack.get("readiness_state") or "unknown"
    state.batch_banner = (
        f"Readiness: {readiness}. Advisory only — QP decides outside this system. No disposition action here."
    )
    state.batch_meta = f"Batch {pack.get('batch_id') or ''} · {_meta(pack)}"
    state.batch_evidence = as_table(flatten_evidence(pack.get("evidence")), EVIDENCE_COLS)
    state.batch_conflicts = as_table(flatten_conflicts(pack.get("contradictions")), CONFLICT_COLS)
    state.batch_gaps = as_table(list(pack.get("gaps") or []), GAP_COLS)
    state.batch_abstentions = as_table(list(pack.get("abstentions") or []), ABSTAIN_COLS)
    _sync_review(state, pack)


def submit_pv(state: Any) -> None:
    pack = _submit(
        {
            "request_id": "UI-PV-1",
            "idempotency_key": "idem-ui-pv-01",
            "as_of": "2026-08-01T08:00:00Z",
            "workflow": "pv_intake",
            "case_ids": ["PV-1001", "PV-1009", "PV-1014"],
            "authorization": {
                "user": "pv_assessor_1",
                "purpose": "pv_intake",
                "object_id": "PV-1001",
                "role": "pv_assessor",
            },
        },
        state,
    )
    state.pv_pack_json = json.dumps(pack, indent=2)
    if "error" in pack:
        state.pv_banner = _error_banner(pack)
        state.pv_meta = ""
        _sync_review(state, pack)
        return
    cases = ", ".join(str(c) for c in (pack.get("case_ids") or []))
    state.pv_banner = (
        f"PV intake cluster ({cases}). Duplicate candidates and listedness are advisory. "
        "Safety physician retains seriousness, reportability, and related judgements."
    )
    state.pv_meta = _meta(pack)
    state.pv_evidence = as_table(flatten_evidence(pack.get("evidence")), EVIDENCE_COLS)
    state.pv_conflicts = as_table(flatten_conflicts(pack.get("contradictions")), CONFLICT_COLS)
    state.pv_duplicates = as_table(list(pack.get("duplicate_candidates") or []), DUP_COLS)
    state.pv_clocks = as_table(list(pack.get("clock_evidence") or []), CLOCK_COLS)
    state.pv_listedness = as_table(list(pack.get("listedness_context") or []), LISTED_COLS)
    _sync_review(state, pack)


def submit_supply(state: Any) -> None:
    pack = _submit(
        {
            "request_id": "UI-SUPPLY-1",
            "idempotency_key": "idem-ui-supply-01",
            "as_of": "2026-08-01T08:00:00Z",
            "workflow": "supply_options",
            "event_id": "SH-901",
            "authorization": {
                "user": "supply_planner_1",
                "purpose": "supply_options",
                "object_id": "SH-901",
                "role": "supply_planner",
            },
        },
        state,
    )
    state.supply_pack_json = json.dumps(pack, indent=2)
    if "error" in pack:
        state.supply_banner = _error_banner(pack)
        state.supply_meta = ""
        _sync_review(state, pack)
        return
    side = pack.get("no_side_effects")
    state.supply_banner = (
        f"Shipment {pack.get('event_id') or ''} · drafts only · no_side_effects={side}. "
        "No reserve, allocate, or ship in this UI."
    )
    state.supply_meta = _meta(pack)
    state.supply_evidence = as_table(flatten_evidence(pack.get("evidence")), EVIDENCE_COLS)
    state.supply_conflicts = as_table(flatten_conflicts(pack.get("contradictions")), CONFLICT_COLS)
    state.supply_constraints = as_table(list(pack.get("constraints") or []), CONSTRAINT_COLS)
    state.supply_options = as_table(flatten_options(pack.get("options")), OPTION_COLS)
    state.supply_holds = as_table(list(pack.get("quality_holds") or []), HOLD_COLS)
    _sync_review(state, pack)


def on_selected_conflicts(state: Any) -> None:
    selected = state.selected_conflicts or []
    if isinstance(selected, str):
        state.viewed_conflict_ids = selected
        return
    state.viewed_conflict_ids = ",".join(str(item) for item in selected)


def acknowledge_review(state: Any) -> None:
    try:
        pack = json.loads(state.review_pack_json or "{}")
    except json.JSONDecodeError:
        pack = {}
    viewed = str(state.viewed_conflict_ids or "")
    if state.selected_conflicts:
        on_selected_conflicts(state)
        viewed = str(state.viewed_conflict_ids or "")
    if not ack_enabled(pack, viewed):
        state.ack_status = "Ack blocked: mark every conflict id as viewed first (INJ-071)."
        return
    out = service.ack_human_review(
        {
            "request_id": state.review_request_id,
            "user": "qp_eu_1",
            "viewed_conflict_ids": conflict_ids_from_pack(pack),
            "ack": True,
        }
    )
    if "error" in out:
        err = out.get("error") or {}
        state.ack_status = f"Ack failed: {err.get('code')} — {err.get('message')}"
        return
    state.ack_status = "Human review acknowledged. Pack remains advisory (not_executed)."


PAGE_ROOT = """
# AEGIS-PHARMA reviewer workbench
Advisory only — engines + LangGraph. Humans decide. No release, reject, allocate, reserve, or ship.
<|{rules_banner}|text|>
<|{kill_switch}|toggle|label=Kill switch (rules only)|on_change=on_kill_switch|>
<|navbar|>
<|content|>
"""

PAGE_BATCH = """
# Batch evidence (QP)
<|{rules_banner}|text|>
<|{kill_switch}|toggle|label=Kill switch (rules only)|on_change=on_kill_switch|>
<|Load batch pack|button|on_action=submit_batch|id=btn-batch|>
<|{batch_banner}|text|>
<|{batch_meta}|text|>

## 1. Evidence
<|{batch_evidence}|table|rebuild|width=100%|>

## 2. Conflicts (priority first; advisory notes are not evidence)
<|{batch_conflicts}|table|rebuild|width=100%|>

## 3. Gaps
<|{batch_gaps}|table|rebuild|width=100%|>

## 4. Abstentions
<|{batch_abstentions}|table|rebuild|width=100%|>

<|expandable|title=Technical pack (JSON)|expanded=False|
<|{batch_pack_json}|text|>
|>
"""

PAGE_PV = """
# PV intake
<|{rules_banner}|text|>
<|Load PV pack|button|on_action=submit_pv|id=btn-pv|>
<|{pv_banner}|text|>
<|{pv_meta}|text|>

## 1. Evidence
<|{pv_evidence}|table|rebuild|width=100%|>

## 2. Duplicate candidates (advisory)
<|{pv_duplicates}|table|rebuild|width=100%|>

## 3. Clock evidence
<|{pv_clocks}|table|rebuild|width=100%|>

## 4. Listedness context
<|{pv_listedness}|table|rebuild|width=100%|>

## 5. Conflicts (priority + advisory note)
<|{pv_conflicts}|table|rebuild|width=100%|>

<|expandable|title=Technical pack (JSON)|expanded=False|
<|{pv_pack_json}|text|>
|>
"""

PAGE_SUPPLY = """
# Supply options (drafts only)
<|{rules_banner}|text|>
<|Load supply drafts|button|on_action=submit_supply|id=btn-supply|>
<|{supply_banner}|text|>
<|{supply_meta}|text|>

## 1. Constraints (shown before options)
<|{supply_constraints}|table|rebuild|width=100%|>

## 2. Quality holds
<|{supply_holds}|table|rebuild|width=100%|>

## 3. Draft options
<|{supply_options}|table|rebuild|width=100%|>

## 4. Evidence
<|{supply_evidence}|table|rebuild|width=100%|>

## 5. Conflicts (priority + advisory note)
<|{supply_conflicts}|table|rebuild|width=100%|>

<|expandable|title=Technical pack (JSON)|expanded=False|
<|{supply_pack_json}|text|>
|>
"""

PAGE_REVIEW = """
# Human review
<|{review_banner}|text|>
<|{review_meta}|text|>

## Conflicts to view (highest priority first)
<|{review_conflicts}|table|rebuild|width=100%|>

Mark every conflict id as viewed (selector) or type them comma-separated.
<|{selected_conflicts}|selector|lov={conflict_id_lov}|multiple|label=Viewed conflict ids|on_change=on_selected_conflicts|>
<|{viewed_conflict_ids}|input|label=Viewed conflict ids (comma-separated)|>
<|Acknowledge review|button|on_action=acknowledge_review|id=btn-ack|>
<|{ack_status}|text|>

<|expandable|title=Technical pack (JSON)|expanded=False|
<|{review_pack_json}|text|>
|>
"""

PAGES = {
    "/": PAGE_ROOT,
    "batch": PAGE_BATCH,
    "pv": PAGE_PV,
    "supply": PAGE_SUPPLY,
    "review": PAGE_REVIEW,
}


def create_gui() -> Any:
    from taipy.gui import Gui  # lazy — assessment tests do not require Taipy installed

    return Gui(pages=PAGES)


def prepare_runtime() -> str:
    """Load local .env for UI process only. Never print secrets."""
    env_path = _AEGIS / ".env"
    if env_path.is_file():
        for raw in env_path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
    prefix = "AZURE" + "_OPEN" + "AI_"
    has_live_llm = all(str(os.environ.get(prefix + part) or "").strip() for part in ("ENDPOINT", "API_KEY", "DEPLOYMENT"))
    kill = str(os.environ.get("AEGIS_KILL_SWITCH") or "").strip().lower() in {"1", "true", "yes", "on"}
    if has_live_llm and not kill:
        os.environ["AEGIS_RUNTIME_MODE"] = "cloud"
        os.environ["AEGIS_ALLOW_LIVE_INFERENCE"] = "true"
    mode = str(os.environ.get("AEGIS_RUNTIME_MODE") or "assessment")
    live = str(os.environ.get("AEGIS_ALLOW_LIVE_INFERENCE") or "").lower() in {"1", "true", "yes", "on"}
    print(f"HITL runtime={mode} conflict_notes={'llm' if (has_live_llm and live and not kill) else 'rules-templates'}")
    return mode


def run() -> None:
    """Prefer `python .../main.py` so Gui is built at module scope for Taipy bindings."""
    prepare_runtime()
    create_gui().run(host=HOST, port=PORT, use_reloader=False, title="AEGIS HITL")


if __name__ == "__main__":
    from taipy.gui import Gui

    prepare_runtime()
    Gui(pages=PAGES).run(host=HOST, port=PORT, use_reloader=False, title="AEGIS HITL")
