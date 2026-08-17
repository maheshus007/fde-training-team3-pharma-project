"""Privacy gates — DSR vs GxP / legal hold / purpose minimise (INJ-035 / INJ-061 / INJ-062)."""
from __future__ import annotations

from dataclasses import dataclass

try:
    from src.inject_controls import evaluate
except ImportError:  # app/demo puts src/ on sys.path
    from inject_controls import evaluate


@dataclass(frozen=True)
class HoldDecision:
    action: str
    reason: str


def check_patient_support_minimise(case_id: str) -> HoldDecision:
    control = evaluate("INJ-062")
    return HoldDecision(
        action=control.action,
        reason=f"{case_id}: {control.notes} {control.observed}",
    )


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
