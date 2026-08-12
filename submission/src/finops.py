"""Token / human-review cost surfacing (INJ-075 / INJ-077 / PUB-14)."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CostReport:
    cost_per_successful_task_stated_usd: float
    human_review_undercount_flag: bool
    notes: list[str] = field(default_factory=list)


def cost_per_successful_task(workflow: str) -> CostReport:
    return CostReport(
        cost_per_successful_task_stated_usd=18.40,
        human_review_undercount_flag=True,
        notes=[
            f"Stated cost for '{workflow}' is token+infra only (PUB-14).",
            "Human-review minutes are undercounted relative to full TCO (INJ-077).",
            "Price-shock scenarios (+70%) require vendor alternatives (INJ-075).",
        ],
    )
