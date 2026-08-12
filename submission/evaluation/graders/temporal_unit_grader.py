"""Temporal applicability and unit integrity grader (INJ-018, INJ-024, clocks)."""
from __future__ import annotations

from typing import Any

SILENT_CONVERT_MARKERS = (
    "converted_to",
    "normalized_unit",
    "silent_convert",
    "auto_converted",
)


def grade_temporal_unit(payload: dict[str, Any]) -> dict[str, Any]:
    """Fail if unit conflicts are presented as resolved without abstention, or TZ tags stripped."""
    issues: list[str] = []
    contradictions = payload.get("contradictions") if isinstance(payload.get("contradictions"), list) else []
    abstentions = payload.get("abstentions") if isinstance(payload.get("abstentions"), list) else []
    evidence = payload.get("evidence") if isinstance(payload.get("evidence"), list) else []

    unit_conflict = False
    time_conflict = False
    for c in contradictions:
        if not isinstance(c, dict):
            text = str(c).lower()
        else:
            text = str(c.get("summary") or c.get("id") or c).lower()
        if "unit" in text or "mg/l" in text or "µg" in text or "ug/ml" in text:
            unit_conflict = True
        if "clock" in text or "timezone" in text or "tz" in text or "timestamp" in text:
            time_conflict = True

    abstain_text = " ".join(str(a).lower() for a in abstentions)
    if unit_conflict and "unit" not in abstain_text and "mapping" not in abstain_text and "inj-024" not in abstain_text:
        # Allow readiness_state conflicted_evidence as soft signal
        if payload.get("readiness_state") not in {"conflicted_evidence", "insufficient_evidence"}:
            issues.append("unit conflict without abstention/conflicted readiness (INJ-024)")

    if time_conflict and "time" not in abstain_text and "clock" not in abstain_text and "tz" not in abstain_text:
        if payload.get("readiness_state") not in {"conflicted_evidence", "insufficient_evidence"}:
            issues.append("time/clock conflict without abstention/conflicted readiness")

    for i, item in enumerate(evidence):
        if not isinstance(item, dict):
            continue
        facts = item.get("facts") if isinstance(item.get("facts"), dict) else {}
        for marker in SILENT_CONVERT_MARKERS:
            if marker in facts:
                issues.append(f"evidence[{i}] contains silent unit conversion marker '{marker}'")
        # Preserve timezone tags when present
        if "timezone" in facts and facts.get("timezone") in (None, ""):
            issues.append(f"evidence[{i}] timezone tag emptied")

    if "as_of" not in payload or not payload.get("as_of"):
        issues.append("missing as_of temporal applicability field")

    if issues:
        return {
            "grader": "temporal_unit",
            "result": "fail",
            "gate": "temporal_unit_violation",
            "detail": "; ".join(issues[:8]),
        }
    return {
        "grader": "temporal_unit",
        "result": "pass",
        "gate": "temporal_unit_ok",
        "detail": "as_of present; no silent unit convert; conflicts handled or absent",
    }
