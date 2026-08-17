"""Protocol context resolution — never decide eligibility (INJ-013 / INJ-014).

Reads protocol_versions.csv and site_approvals.csv. Does not invent versions.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

try:
    from src.inject_controls import evaluate
except ImportError:  # app/demo puts src/ on sys.path
    from inject_controls import evaluate

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data"


@dataclass(frozen=True)
class ProtocolContext:
    subject_id: str
    site_id: str
    site_approved_protocol: str
    global_current_protocol: str
    eligibility_decision: str
    action: str
    flags: list[str] = field(default_factory=list)


def _rows(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def resolve_protocol_context(subject_id: str, site_id: str = "IN-014") -> ProtocolContext:
    versions = _rows("protocol_versions.csv")
    approvals = _rows("site_approvals.csv")
    current = next(r for r in versions if r["status"] == "global_current")
    site = next((r for r in approvals if r["site_id"] == site_id), approvals[0])
    inj013 = evaluate("INJ-013")
    inj014 = evaluate("INJ-014")
    return ProtocolContext(
        subject_id=subject_id,
        site_id=site["site_id"],
        site_approved_protocol=f"{site['trial_id']} v{site['approved_protocol']}",
        global_current_protocol=f"{current['trial_id']} v{current['version']}",
        eligibility_decision="not_decided",
        action="surface_conflict_abstain",
        flags=[
            f"Site vs global protocol version divergence (INJ-013): {inj013.observed}.",
            f"Eligibility not decided (INJ-014 / {inj014.action}).",
            "Human clinical accountability preserved (D-203).",
        ],
    )
