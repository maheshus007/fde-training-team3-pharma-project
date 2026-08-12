"""Protocol context resolution — never decide eligibility (INJ-013 / INJ-014 / PUB-15)."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProtocolContext:
    subject_id: str
    site_approved_protocol: str
    global_current_protocol: str
    eligibility_decision: str
    action: str
    flags: list[str] = field(default_factory=list)


def resolve_protocol_context(subject_id: str) -> ProtocolContext:
    return ProtocolContext(
        subject_id=subject_id,
        site_approved_protocol="S-301 Protocol v3.1 (site-approved)",
        global_current_protocol="S-301 Protocol v4.0 (global current)",
        eligibility_decision="not_decided",
        action="surface_conflict_abstain",
        flags=[
            "Site vs global protocol version divergence (INJ-013).",
            "Eligibility criteria conflict retained — system must not decide (INJ-014 / PUB-15).",
            "Human clinical accountability preserved.",
        ],
    )
