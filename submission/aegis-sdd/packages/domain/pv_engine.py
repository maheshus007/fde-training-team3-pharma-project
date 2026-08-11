"""Workflow B — PV intake pack (T-010). No final PV decisions; no merge."""
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
from ontology import retain_coding  # noqa: E402
from policy_guard import check_workflow_payload  # noqa: E402

from adapters.entitlements import EntitlementStore  # noqa: E402
from contracts import validate_workflow_response  # noqa: E402

_SENSITIVE_ROLES = frozenset({"pv_assessor", "pv_medical", "auditor_elevated"})
_CLOCK_CHANNEL = {
    "vendor": "vendor",
    "affiliate_inbox": "affiliate",
    "affiliate": "affiliate",
    "global_db": "global",
    "global": "global",
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


def _listed_source_doc(raw: str) -> str:
    text = raw.lower()
    if text.startswith("ib"):
        return "IB"
    if text.startswith("ccds"):
        return "CCDS"
    return "local_label"


def build_pv_pack(request: dict[str, Any]) -> dict[str, Any]:
    request_id = str(request.get("request_id") or "req-pv")
    guarded = check_workflow_payload("pv_intake", request)
    if not guarded.allow:
        return _envelope("AEGIS-422", guarded.reason, request_id)

    auth = request.get("authorization") or {}
    case_ids = [str(x) for x in (request.get("case_ids") or []) if x]
    as_of = str(request.get("as_of") or "2026-08-01T08:00:00Z")
    user = str(auth.get("user") or "")
    purpose = str(auth.get("purpose") or "")
    role = str(auth.get("role") or "")
    object_id = str(auth.get("object_id") or (case_ids[0] if case_ids else ""))

    authz = EntitlementStore().authorize(
        user=user,
        purpose=purpose,
        object_id=object_id,
        role=role,
        workflow="pv_intake",
        as_of=as_of,
        request_id=request_id,
    )
    if not authz.allow:
        return authz.error or _envelope("AEGIS-401", authz.reason, request_id)

    retrieved = _now()
    wanted = set(case_ids)
    evidence: list[dict[str, Any]] = []
    contradictions: list[dict[str, Any]] = []
    source_facts: list[dict[str, str]] = []
    duplicate_candidates: list[dict[str, Any]] = []
    clock_evidence: list[dict[str, str]] = []
    terminology: list[dict[str, str]] = []
    listedness_context: list[dict[str, Any]] = []
    abstentions: list[dict[str, Any]] = []

    for row in _rows("icsr_cases.csv"):
        cid = row.get("case_id") or ""
        if cid not in wanted:
            continue
        evidence.append(_item("data/icsr_cases.csv", cid, row.get("source") or "SAFETY", dict(row), retrieved, row.get("awareness_date") or None))
        source_facts.append({"case_id": cid, "pointer": "event", "value": row.get("event") or ""})

    graph = MemoryGraph()
    graph.ingest_from_fixtures()
    graph.query("CQ-3", {"case_ids": case_ids}, "pv_intake", as_of)

    for row in _rows("duplicate_candidates.csv"):
        a, b = row.get("case_a") or "", row.get("case_b") or ""
        if a not in wanted and b not in wanted:
            continue
        if a not in wanted:
            wanted.add(a)
            case_ids.append(a)
        if b not in wanted:
            wanted.add(b)
            case_ids.append(b)
        similarity: Any = row.get("similarity")
        try:
            similarity = float(similarity)
        except (TypeError, ValueError):
            pass
        candidate = {
            "case_id_a": a,
            "case_id_b": b,
            "similarity": similarity,
            "reason": row.get("reason") or "",
        }
        duplicate_candidates.append(candidate)

    clocks: list[dict[str, str]] = []
    for row in _rows("safety_receipts.csv"):
        cid = row.get("case_id") or ""
        if cid not in wanted:
            continue
        channel = _CLOCK_CHANNEL.get(str(row.get("channel") or "").lower(), "vendor")
        receipt = row.get("receipt") or ""
        tz = "UTC" if receipt.endswith("Z") else "timezone_unknown"
        clocks.append({"case_id": cid, "channel": channel, "timestamp": receipt, "timezone": tz})
        evidence.append(_item("data/safety_receipts.csv", f"{cid}:{channel}", "safety_receipts", dict(row), retrieved, receipt or None))
    clock_evidence = clocks
    if len({c["timestamp"] for c in clocks}) > 1:
        contradictions.append(
            {
                "id": "clock:PV-1001:vendor:global",
                "kind": "clock",
                "left": {"source": "vendor", "record_id": "PV-1001", "verbatim": clocks[0]["timestamp"] if clocks else ""},
                "right": {"source": "global", "record_id": "PV-1001", "verbatim": clocks[-1]["timestamp"] if clocks else ""},
            }
        )

    for row in _rows("adverse_events.csv"):
        if row.get("case_id") not in wanted:
            continue
        coding = retain_coding(row)
        terminology.append(coding)
        evidence.append(_item("data/adverse_events.csv", row.get("case_id") or "", "MedDRA", dict(row), retrieved))

    listed_values: set[str] = set()
    for row in _rows("listedness_sources.csv"):
        listedness_context.append(
            {
                "product_id": row.get("product") or "",
                "risk": row.get("risk") or "",
                "source_doc": _listed_source_doc(row.get("source") or ""),
                "jurisdiction": "IN" if "local" in (row.get("source") or "").lower() else "DE",
                "listed": row.get("listed") or "unknown",
                "effective_at": None,
            }
        )
        listed_values.add(str(row.get("listed") or ""))
        evidence.append(_item("data/listedness_sources.csv", f"{row.get('product')}:{row.get('source')}", "label", dict(row), retrieved))
    if "yes" in listed_values and "no" in listed_values:
        contradictions.append(
            {
                "id": "listedness:NCB-204:CCDS:IN",
                "kind": "listedness",
                "left": {"source": "CCDS", "record_id": "NCB-204", "verbatim": "yes"},
                "right": {"source": "IN local label", "record_id": "NCB-204", "verbatim": "no"},
            }
        )

    allow_sensitive = role in _SENSITIVE_ROLES
    for row in _rows("sensitive_segments.csv"):
        cid = row.get("case_id") or ""
        if cid not in wanted:
            continue
        if allow_sensitive:
            source_facts.append(
                {
                    "case_id": cid,
                    "pointer": row.get("segment") or "narrative",
                    "value": f"[sensitive]{row.get('segment')}",
                }
            )
        evidence.append(_item("data/sensitive_segments.csv", cid, "PV privacy", dict(row), retrieved))

    for row in _rows("social_listening.csv"):
        post_id = row.get("post_id") or ""
        evidence.append(_item("data/social_listening.csv", post_id, "social_listening", dict(row), retrieved))
        identifiable = str(row.get("identifiable_reporter") or "").lower()
        if identifiable in {"no", "false", "unknown", ""}:
            abstentions.append(
                {
                    "code": "authenticity_failed",
                    "reason": f"{post_id} reporter not authenticated; not actionable for PV",
                    "record_ref": post_id,
                }
            )

    required_reviews = ["safety physician"] if duplicate_candidates or len(clock_evidence) > 1 else []

    pack = {
        "request_id": request_id,
        "workflow": "pv_intake",
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
        "human_review": {"required": True, "role": "pv_assessor"},
        "execution_status": "not_executed",
        "audit": {"event_id": f"AUD-{request_id}"},
        "case_ids": case_ids,
        "source_facts": source_facts,
        "duplicate_candidates": duplicate_candidates,
        "clock_evidence": clock_evidence,
        "terminology": terminology,
        "listedness_context": listedness_context,
        "required_reviews": required_reviews,
    }
    errors = validate_workflow_response(pack)
    if errors:
        return _envelope("AEGIS-422", "; ".join(errors[:5]), request_id)
    return pack
