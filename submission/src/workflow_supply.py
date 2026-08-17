"""Workflow C — supply shortage / cold-chain draft options (no side effects)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

try:
    from src.inject_controls import evaluate
except ImportError:  # app/demo puts src/ on sys.path
    from inject_controls import evaluate


def build_supply_response(
    event_id: str, root_lot: str, request_id: str, user: str
) -> dict[str, Any]:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "request_id": request_id,
        "as_of": now,
        "authorization": {
            "user": user,
            "purpose": "supply_options_draft",
            "checked_at": now,
            "decision": "allow",
            "reason": "demo entitlement",
        },
        "workflow": "supply_options",
        "event_id": event_id,
        "root_lot": root_lot,
        "execution_status": "not_executed",
        "no_side_effects": True,
        "evidence": [],
        "options": [
            {
                "option_id": "OPT-1",
                "status": "draft",
                "summary": f"Defer allocation on {root_lot}; escalate Quality hold assessment (INJ-051).",
            },
            {
                "option_id": "OPT-2",
                "status": "draft",
                "summary": "Enumerate shortage options under MA / trial / CU constraints (INJ-054 / INJ-056).",
            },
        ],
        "constraints": [
            {"id": "Q-HOLD", "detail": "Quality status change forbidden for this path."},
            {"id": "NO-ALLOC", "detail": "Reserve / allocate / ship not available as tools."},
        ],
        "quality_holds": [{"lot": root_lot, "status": "under_assessment"}],
        "approvals_required": ["Supply Governance Board"],
        "approval_required": {
            "role": "Supply Governance Board",
            "required": True,
        },
        "contradictions": [],
        "gaps": [
            {
                "id": "G-CC-01",
                "detail": "Cold-chain logger clock / pallet association may be disputed (INJ-051).",
            },
            {
                "id": "G-CF-01",
                "detail": (
                    "Returned serials have inconsistent print/distribution history "
                    f"({evaluate('INJ-053').observed[0]}) — no recall initiation (INJ-053)."
                ),
            },
            {
                "id": "G-CMO-01",
                "detail": (
                    f"CMO capacity conflict {evaluate('INJ-055').observed[0]} "
                    "— constraint only, not an allocation (INJ-055)."
                ),
            },
        ],
        "abstentions": [
            {
                "id": "A-VAR-01",
                "detail": (
                    f"Manufacturing-change classification remains open "
                    f"({evaluate('INJ-049').observed[0]}) — AEGIS does not classify (INJ-049)."
                ),
            }
        ],
        "human_review": {
            "required": True,
            "role": "Supply Governance Board",
        },
        "audit": {"event_id": f"AUD-SUPPLY-{request_id}"},
        "notice": "Draft options only — no reserve, allocate, ship, quality-status change, or recall.",
    }
