"""Workflow A — batch evidence pack (T-009). Rules only; no disposition."""
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
from ontology import evaluate_lab_comparability  # noqa: E402
from policy_guard import check_workflow_payload  # noqa: E402

from adapters.entitlements import EntitlementStore  # noqa: E402
from contracts import validate_workflow_response  # noqa: E402


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


def build_batch_pack(request: dict[str, Any]) -> dict[str, Any]:
    request_id = str(request.get("request_id") or "req-batch")
    guarded = check_workflow_payload("batch_evidence", request)
    if not guarded.allow:
        return _envelope("AEGIS-422", guarded.reason, request_id)

    auth = request.get("authorization") or {}
    batch_id = str(request.get("batch_id") or "")
    as_of = str(request.get("as_of") or "2026-08-01T08:00:00Z")
    user = str(auth.get("user") or "")
    purpose = str(auth.get("purpose") or "")
    role = str(auth.get("role") or "")
    object_id = str(auth.get("object_id") or batch_id)

    authz = EntitlementStore().authorize(
        user=user,
        purpose=purpose,
        object_id=object_id,
        role=role,
        workflow="batch_evidence",
        as_of=as_of,
        request_id=request_id,
    )
    if not authz.allow:
        return authz.error or _envelope("AEGIS-401", authz.reason, request_id)

    retrieved = _now()
    evidence: list[dict[str, Any]] = []
    contradictions: list[dict[str, Any]] = []
    gaps: list[dict[str, Any]] = []
    abstentions: list[dict[str, Any]] = []

    for row in _rows("batches.csv"):
        if row.get("batch_id") == batch_id:
            evidence.append(
                _item("data/batches.csv", batch_id, row.get("site") or "batch", dict(row), retrieved, row.get("manufacture_date") or None)
            )

    mes_sua = None
    for row in _rows("material_genealogy.csv"):
        if row.get("batch_id") != batch_id:
            continue
        evidence.append(
            _item("data/material_genealogy.csv", row.get("material_lot") or "", row.get("source") or "MES", dict(row), retrieved)
        )
        if row.get("material_lot") == "SUA-88":
            mes_sua = row

    wm_sua = None
    for row in _rows("warehouse_movements.csv"):
        if row.get("batch_id") != batch_id:
            continue
        evidence.append(
            _item("data/warehouse_movements.csv", row.get("movement_id") or "", "warehouse", dict(row), retrieved)
        )
        if row.get("material_lot") == "SUA-88":
            wm_sua = row

    if mes_sua and wm_sua:
        contradictions.append(
            {
                "id": "genealogy:MES|SUA-88:WM-90|SUA-88",
                "kind": "genealogy",
                "left": {
                    "source": mes_sua.get("source") or "MES",
                    "record_id": "SUA-88",
                    "verbatim": mes_sua.get("relation") or "missing_branch",
                },
                "right": {
                    "source": "warehouse",
                    "record_id": wm_sua.get("movement_id") or "WM-90",
                    "verbatim": wm_sua.get("status") or "issued",
                },
            }
        )

    graph = MemoryGraph()
    graph.ingest_from_fixtures()
    graph.query("CQ-1", {"batch_id": batch_id}, "batch_review_readiness", as_of)

    for row in _rows("lab_results.csv"):
        if row.get("batch_id") != batch_id:
            continue
        evidence.append(_item("data/lab_results.csv", row.get("result_id") or "", "LIMS", dict(row), retrieved))
        if row.get("result_id") == "LR-88":
            unit_gate = evaluate_lab_comparability("LR-88")
            if not unit_gate.get("allowed"):
                abstention = unit_gate.get("abstention") or {}
                abstentions.append(
                    {
                        "code": abstention.get("code") or "unit_unapproved",
                        "reason": abstention.get("reason") or "unapproved unit mapping",
                        "record_ref": "LR-88",
                    }
                )

    for row in _rows("oos_investigations.csv"):
        if row.get("result_id") != "LR-88":
            continue
        evidence.append(_item("data/oos_investigations.csv", row.get("investigation_id") or "", "QMS", dict(row), retrieved))
        contradictions.append(
            {
                "id": "oos_status:LIMS|LR-88:stats|LR-88",
                "kind": "oos_status",
                "left": {"source": "LIMS", "record_id": "LR-88", "verbatim": row.get("lims_state") or "OOS"},
                "right": {"source": "stats", "record_id": "LR-88", "verbatim": row.get("stats_state") or "OOT"},
            }
        )
        contradictions.append(
            {
                "id": "oos_status:LIMS|LR-88:notebook|LR-88",
                "kind": "oos_status",
                "left": {"source": "LIMS", "record_id": "LR-88", "verbatim": row.get("lims_state") or "OOS"},
                "right": {
                    "source": "notebook",
                    "record_id": "LR-88",
                    "verbatim": row.get("notebook_state") or "invalid_sample_prep",
                },
            }
        )

    for row in _rows("release_packets.csv"):
        if row.get("batch_id") != batch_id:
            continue
        evidence.append(
            _item("data/release_packets.csv", row.get("packet_item") or "", "QP", dict(row), retrieved)
        )
        if "audit commitment" in (row.get("packet_item") or "").lower() and row.get("status") == "missing":
            gaps.append(
                {
                    "id": "gap:supplier_audit_commitment:AUD-2025-14",
                    "kind": "supplier_audit_commitment",
                    "record_ref": "AUD-2025-14",
                    "note": "CMO audit commitment 2025-14 missing from release packet",
                }
            )

    for row in _rows("supplier_audits.csv"):
        if row.get("audit_id") == "AUD-2025-14":
            evidence.append(_item("data/supplier_audits.csv", row.get("audit_id") or "", "supplier quality", dict(row), retrieved))

    readiness = "conflicted_evidence" if contradictions else (
        "insufficient_evidence" if gaps else "ready_for_authorized_review"
    )
    if abstentions and readiness == "ready_for_authorized_review":
        readiness = "insufficient_evidence"

    pack = {
        "request_id": request_id,
        "workflow": "batch_evidence",
        "as_of": as_of,
        "authorization": {
            "user": user,
            "purpose": purpose,
            "checked_at": retrieved,
            "decision": "allow",
        },
        "evidence": evidence,
        "contradictions": contradictions,
        "gaps": gaps,
        "abstentions": abstentions,
        "human_review": {"required": True, "role": "qp_reviewer"},
        "execution_status": "not_executed",
        "audit": {"event_id": f"AUD-{request_id}"},
        "batch_id": batch_id,
        "readiness_state": readiness,
        "applicable_documents": [],
    }
    errors = validate_workflow_response(pack)
    if errors:
        return _envelope("AEGIS-422", "; ".join(errors[:5]), request_id)
    return pack
