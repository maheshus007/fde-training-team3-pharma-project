"""Evidence fidelity grader — provenance fields and no fabricated-empty citations."""
from __future__ import annotations

from typing import Any


REQUIRED_EVIDENCE_KEYS = ("source", "record_id", "authority")


def grade_evidence(payload: dict[str, Any]) -> dict[str, Any]:
    """Pass when evidence items include source/record_id/authority and contradictions are lists."""
    issues: list[str] = []
    evidence = payload.get("evidence")
    if not isinstance(evidence, list):
        return {
            "grader": "evidence",
            "result": "fail",
            "gate": "evidence_shape",
            "detail": "evidence must be an array",
        }
    for i, item in enumerate(evidence):
        if not isinstance(item, dict):
            issues.append(f"evidence[{i}] not object")
            continue
        for key in REQUIRED_EVIDENCE_KEYS:
            if key not in item or item[key] in (None, ""):
                issues.append(f"evidence[{i}] missing {key}")
        integrity = item.get("integrity")
        if isinstance(integrity, dict) and integrity.get("source_preserved") is False:
            issues.append(f"evidence[{i}] source_preserved=false")
    for field in ("contradictions", "gaps", "abstentions"):
        if field in payload and not isinstance(payload[field], list):
            issues.append(f"{field} must be array")
    if issues:
        return {
            "grader": "evidence",
            "result": "fail",
            "gate": "evidence_incomplete",
            "detail": "; ".join(issues[:10]),
        }
    return {
        "grader": "evidence",
        "result": "pass",
        "gate": "evidence_ok",
        "detail": f"{len(evidence)} cited item(s)",
    }
