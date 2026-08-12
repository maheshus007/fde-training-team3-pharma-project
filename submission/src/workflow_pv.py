"""Workflow B — PV intake & signal support (advisory only)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def build_pv_response(case_ids: list[str], request_id: str, user: str) -> dict[str, Any]:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "request_id": request_id,
        "as_of": now,
        "authorization": {
            "user": user,
            "purpose": "pv_intake_support",
            "checked_at": now,
            "decision": "allow",
            "reason": "demo entitlement",
        },
        "workflow": "pv_intake",
        "case_ids": list(case_ids),
        "execution_status": "not_executed",
        "evidence": [],
        "source_facts": [
            {"case_id": cid, "channel": "mixed", "preserved": True} for cid in case_ids
        ],
        "duplicate_candidates": [
            {
                "cluster_id": "DUP-PV-1001",
                "members": [c for c in case_ids if c.startswith("PV-")],
                "note": "Candidate cluster only — no auto-merge (INJ-037).",
            }
        ],
        "clock_evidence": [
            {
                "theme": "awareness_date_conflict",
                "detail": "Awareness dates disagree across receipts — all clocks preserved (INJ-038).",
            }
        ],
        "terminology": [
            {
                "theme": "meddra_version_mismatch",
                "detail": "MedDRA version labels retained with coding (INJ-039).",
            }
        ],
        "listedness_context": [
            {
                "theme": "expectedness_source_conflict",
                "detail": "IB / CCDS / local label misaligned — no final expectedness (INJ-040).",
            }
        ],
        "contradictions": [],
        "gaps": [
            {
                "id": "G-AUTH-01",
                "detail": "Social-media authenticity uncertain where applicable (INJ-042).",
            }
        ],
        "abstentions": [
            {
                "id": "A-PV-01",
                "detail": "No final seriousness, causality, expectedness, or reportability.",
            }
        ],
        "required_reviews": ["safety physician"],
        "human_review": {
            "required": True,
            "role": "Safety Physician",
        },
        "audit": {"event_id": f"AUD-PV-{request_id}"},
        "notice": "Draft support only — humans remain accountable for PV decisions.",
    }
