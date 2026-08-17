"""Workflow A — GxP batch evidence reconciliation (advisory only)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

try:
    from src.inject_controls import evaluate
except ImportError:  # app/demo puts src/ on sys.path
    from inject_controls import evaluate


def reconcile_batch(batch_id: str, request_id: str, user: str) -> dict[str, Any]:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "request_id": request_id,
        "as_of": now,
        "authorization": {
            "user": user,
            "purpose": "batch_review_readiness",
            "checked_at": now,
            "decision": "allow",
            "reason": "demo entitlement (execution-time re-check required in production)",
        },
        "workflow": "batch_evidence",
        "batch_id": batch_id,
        "readiness_state": "conflicted_evidence",
        "execution_status": "not_executed",
        "evidence": [
            {
                "source": "data/batch_records.csv",
                "record_id": batch_id,
                "authority": "MES / eBR export (synthetic)",
                "effective_at": "2026-07-15",
                "retrieved_at": now,
                "facts": {"status": "in_review", "product": "NCB-204"},
                "integrity": {"sha256": "demo", "source_preserved": True},
            }
        ],
        "contradictions": [
            {
                "id": "C-GEN-01",
                "theme": "genealogy_break",
                "detail": "SUA-88 issued in warehouse, missing in MES genealogy (INJ-021).",
            },
            {
                "id": "C-OOS-01",
                "theme": "oos_oot_disagreement",
                "detail": "LIMS OOS / stats OOT / notebook invalid — triple status retained (INJ-023).",
            },
        ],
        "gaps": [
            {
                "id": "G-QP-01",
                "detail": "CMO audit commitment missing from EU packet (INJ-028).",
            }
        ],
        "abstentions": [
            {
                "id": "A-UNIT-01",
                "detail": "mg/L vs µg/mL mapping approved=no — abstain, no silent convert (INJ-024).",
            },
            {
                "id": "A-PAT-01",
                "detail": (
                    "PAT model version not synchronized to batch recipe "
                    f"({evaluate('INJ-027').observed[0]}; {evaluate('INJ-027').observed[1]}) "
                    "— abstain on PAT-aligned readiness (INJ-027)."
                ),
            },
        ],
        "applicable_documents": [],
        "human_review": {
            "required": True,
            "role": "EU QP / QA reviewer",
            "forced_acknowledgements": [
                "genealogy break",
                "OOS/OOT conflict",
                "unit mapping abstention",
                "PAT vs recipe version desync",
            ],
        },
        "audit": {"event_id": f"AUD-BATCH-{request_id}"},
        "notice": "Draft support only — no disposition, release, reject, reprocess, or recall.",
    }
