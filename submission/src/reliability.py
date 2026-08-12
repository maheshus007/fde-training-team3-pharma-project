"""Runtime mode selection (AI-disabled continuity / INJ-079 / INJ-082)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeSelection:
    mode: str
    endpoint: str | None
    model: str | None
    reason: str


def select_runtime_mode(workflow: str) -> RuntimeSelection:
    """Default POC path is deterministic / AI-disabled (ADR-001, ADR-008)."""
    return RuntimeSelection(
        mode="ai_disabled_deterministic",
        endpoint=None,
        model=None,
        reason=(
            f"Workflow '{workflow}' runs on the offline deterministic path. "
            "Inference kill switch engaged for continuity (INJ-082); "
            "no unverified model endpoint selected (INJ-070)."
        ),
    )
