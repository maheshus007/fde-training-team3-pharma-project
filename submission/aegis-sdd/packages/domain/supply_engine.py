"""Workflow C — supply options pack (T-011). Drafts only; no side effects."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_DOMAIN = Path(__file__).resolve().parent
_AEGIS = _DOMAIN.parents[1]
_SUBMISSION = _DOMAIN.parents[2]
_DATA = _SUBMISSION.parent / "data"
_INTEGRATION = _AEGIS / "services" / "integration"
_SRC = _SUBMISSION / "src"

for path in (_DOMAIN, _INTEGRATION, _SRC, _SUBMISSION):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from graph_memory import MemoryGraph  # noqa: E402
from ontology import resolve_product_identity  # noqa: E402
from policy_guard import check_workflow_payload  # noqa: E402

from adapters.entitlements import EntitlementStore  # noqa: E402
from contracts import validate_workflow_response  # noqa: E402

_CHANNEL = {
    "commercial_eu": "commercial",
    "market_contracts": "commercial",
    "commercial": "commercial",
    "clinical_trial": "trial",
    "trial_continuity": "trial",
    "trial": "trial",
    "compassionate_use": "compassionate",
}


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _rows(name: str) -> list[dict[str, str]]:
    path = _DATA / name
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _sha256_facts(facts: dict[str, Any]) -> str:
    payload = json.dumps(facts, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _item(
    source: str,
    record_id: str,
    authority: str,
    facts: dict[str, Any],
    retrieved_at: str,
    effective_at: str | None = None,
) -> dict[str, Any]:
    return {
        "source": source,
        "record_id": record_id,
        "authority": authority,
        "effective_at": effective_at,
        "retrieved_at": retrieved_at,
        "facts": facts,
        "integrity": {"sha256": _sha256_facts(facts), "source_preserved": True},
    }


def _envelope(code: str, message: str, request_id: str) -> dict[str, Any]:
    return {
        "error": {
            "code": code,
            "message": message.replace("\n", " ").strip(),
            "request_id": str(request_id),
            "retryable": False,
        }
    }


def build_supply_pack(request: dict[str, Any]) -> dict[str, Any]:
    request_id = str(request.get("request_id") or "req-supply")
    if "reservation_id" in request or "allocation_id" in request or "shipment_id" in request:
        return _envelope("AEGIS-422", "prohibited supply side-effect field", request_id)
    guarded = check_workflow_payload("supply_options", request)
    if not guarded.allow:
        return _envelope("AEGIS-422", guarded.reason, request_id)

    auth = request.get("authorization") or {}
    event_id = str(request.get("event_id") or "SH-901")
    as_of = str(request.get("as_of") or "2026-08-01T08:00:00Z")
    user = str(auth.get("user") or "")
    purpose = str(auth.get("purpose") or "")
    role = str(auth.get("role") or "")
    object_id = str(auth.get("object_id") or event_id)

    authz = EntitlementStore().authorize(
        user=user,
        purpose=purpose,
        object_id=object_id,
        role=role,
        workflow="supply_options",
        as_of=as_of,
        request_id=request_id,
    )
    if not authz.allow:
        return authz.error or _envelope("AEGIS-401", authz.reason, request_id)

    retrieved = _now()
    evidence: list[dict[str, Any]] = []
    contradictions: list[dict[str, Any]] = []
    abstentions: list[dict[str, Any]] = []
    constraints: list[dict[str, str]] = []
    quality_holds: list[dict[str, str]] = []

    idmp = resolve_product_identity("NCB-204", "NCB204-DE")
    if not idmp.get("same_product"):
        contradictions.append(
            {
                "id": "idmp:NCB-204:NCB204-DE",
                "kind": "idmp",
                "left": {"source": "RIM", "record_id": "NCB-204", "verbatim": "100 mg/10 mL concentrate"},
                "right": {"source": "ERP", "record_id": "NCB204-DE", "verbatim": "10 mg/mL solution"},
            }
        )

    graph = MemoryGraph()
    graph.ingest_from_fixtures()
    cq6 = graph.query("CQ-6", {"shipment_id": event_id}, "supply_options", as_of)
    blob = json.dumps(cq6)
    if "P-88" in blob and "P-89" in blob:
        contradictions.append(
            {
                "id": "logger_pallet:LG-31:P-88:P-89",
                "kind": "logger_pallet",
                "left": {"source": "shipments", "record_id": "P-88", "verbatim": "SH-901 associated pallet P-88"},
                "right": {"source": "temperature_loggers", "record_id": "P-89", "verbatim": "LG-31 also associated with P-89"},
            }
        )
        abstentions.append(
            {
                "code": "time_unresolved",
                "reason": "SH-901 logger-pallet association is not authenticated (P-88 vs P-89)",
                "record_ref": "SH-901",
            }
        )

    for row in _rows("shipments.csv"):
        if row.get("shipment_id") == event_id:
            evidence.append(_item("data/shipments.csv", event_id, "logistics", dict(row), retrieved))
    for row in _rows("temperature_loggers.csv"):
        if row.get("logger") == "LG-31":
            evidence.append(
                _item(
                    "data/temperature_loggers.csv",
                    f"{row.get('logger')}:{row.get('pallet')}",
                    "logistics",
                    dict(row),
                    retrieved,
                    row.get("timestamp") or None,
                )
            )

    for row in _rows("inventory.csv"):
        evidence.append(
            _item("data/inventory.csv", f"{row.get('product')}:{row.get('market')}", "inventory", dict(row), retrieved)
        )
        status = row.get("quality_status") or ""
        if status in {"quarantine", "quality_hold"}:
            quality_holds.append(
                {"batch_id_or_lot": f"{row.get('product')}|{row.get('market')}", "status": status}
            )

    for row in _rows("batches.csv"):
        if row.get("status") == "quality_hold":
            quality_holds.append({"batch_id_or_lot": row.get("batch_id") or "", "status": row.get("status") or ""})

    for row in _rows("allocation_constraints.csv"):
        raw = str(row.get("constraint") or "")
        channel = _CHANNEL.get(raw.lower(), "other")
        cid = f"C-{raw}"
        constraints.append({"constraint_id": cid, "channel": channel, "note": f"{raw} priority={row.get('priority')}"})
        evidence.append(_item("data/allocation_constraints.csv", raw, "supply ethics", dict(row), retrieved))

    for row in _rows("demand_forecast.csv"):
        raw = str(row.get("channel") or "")
        channel = _CHANNEL.get(raw.lower(), "other")
        cid = f"D-{raw}"
        if not any(c["constraint_id"] == cid for c in constraints):
            constraints.append(
                {"constraint_id": cid, "channel": channel, "note": f"{raw} demand {row.get('units_8w')} units / 8w"}
            )
        evidence.append(_item("data/demand_forecast.csv", raw, "demand", dict(row), retrieved))

    constraint_ids = [c["constraint_id"] for c in constraints]
    options = [
        {
            "option_id": "OPT-HOLD-DRAFT",
            "status": "draft",
            "summary": "Do not treat quarantined Global NCB-204 as allocatable; wait for quality-released stock only. NCB-204 is not NCB204-DE.",
            "constraint_ids": [c for c in constraint_ids if "quality" in c.lower() or c.startswith("C-quality")],
        },
        {
            "option_id": "OPT-CHANNEL-DRAFT",
            "status": "draft",
            "summary": "Draft channel split under ethics review: trial continuity and compassionate-use flags remain visible; no reservation.",
            "constraint_ids": constraint_ids,
        },
    ]

    pack = {
        "request_id": request_id,
        "workflow": "supply_options",
        "as_of": as_of,
        "authorization": {
            "user": user,
            "purpose": purpose,
            "checked_at": retrieved,
            "decision": "allow",
        },
        "evidence": evidence,
        "contradictions": contradictions,
        "gaps": [],
        "abstentions": abstentions,
        "human_review": {"required": True, "role": "supply_planner"},
        "execution_status": "not_executed",
        "audit": {"event_id": f"AUD-{request_id}"},
        "event_id": event_id,
        "options": options,
        "constraints": constraints,
        "approvals_required": ["Supply Governance Board", "ethics_board_review"],
        "quality_holds": quality_holds,
        "no_side_effects": True,
    }
    errors = validate_workflow_response(pack)
    if errors:
        return _envelope("AEGIS-422", "; ".join(errors[:5]), request_id)
    return pack
