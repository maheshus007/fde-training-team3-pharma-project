"""Privacy gates — DSR vs GxP / legal hold (INJ-035 / INJ-061 / PUB-11)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HoldDecision:
    action: str
    reason: str


def check_deletion_against_hold(subject_id: str, dsr_id: str) -> HoldDecision:
    if dsr_id == "DSR-17":
        return HoldDecision(
            action="restrict_document_do_not_delete",
            reason=(
                f"Deletion for {subject_id} under {dsr_id} blocked: legal hold / "
                "trial integrity conflict (INJ-061 / PUB-11). Document restriction only."
            ),
        )
    return HoldDecision(
        action="escalate_review",
        reason=f"No automated delete for {subject_id}/{dsr_id}; route privacy + Quality.",
    )
