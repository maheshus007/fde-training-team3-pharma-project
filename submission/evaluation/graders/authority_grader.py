"""Authority / applicability grader — evidence items must carry authority metadata."""
from __future__ import annotations

from typing import Any


def grade_authority(payload: dict[str, Any]) -> dict[str, Any]:
    """Pass when every evidence item has non-empty authority (or evidence is empty with abstention)."""
    evidence = payload.get("evidence")
    if not isinstance(evidence, list):
        return {
            "grader": "authority",
            "result": "fail",
            "gate": "authority_missing",
            "detail": "evidence must be an array",
        }
    missing: list[str] = []
    for i, item in enumerate(evidence):
        if not isinstance(item, dict):
            missing.append(f"evidence[{i}]: not an object")
            continue
        auth = item.get("authority")
        if auth is None or (isinstance(auth, str) and not auth.strip()):
            missing.append(f"evidence[{i}]: missing authority")
    if missing:
        return {
            "grader": "authority",
            "result": "fail",
            "gate": "authority_incomplete",
            "detail": "; ".join(missing[:8]),
        }
    if not evidence and not payload.get("abstentions"):
        return {
            "grader": "authority",
            "result": "fail",
            "gate": "empty_without_abstention",
            "detail": "empty evidence requires abstentions",
        }
    return {
        "grader": "authority",
        "result": "pass",
        "gate": "authority_present",
        "detail": f"{len(evidence)} evidence item(s) with authority",
    }
