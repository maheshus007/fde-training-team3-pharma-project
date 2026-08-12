#!/usr/bin/env python3
"""Minimal participant-facing demonstrator (CLI).

Shows current fail-closed status for the three workflows and runtime mode
without enabling model inference. Assessed-mode entry point for defence demos.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

import clinical_protocol  # noqa: E402
import finops  # noqa: E402
import reliability  # noqa: E402
import workflow_batch  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="AEGIS-PHARMA deterministic demo")
    parser.add_argument("--ai-disabled", action="store_true", help="Force AI-disabled narrative")
    args = parser.parse_args()

    sel = reliability.select_runtime_mode("batch_review")
    batch = workflow_batch.reconcile_batch("NCB204-B24071", "demo-batch", "demo_user")
    protocol = clinical_protocol.resolve_protocol_context("S-301-044")
    cost = finops.cost_per_successful_task("batch_review")

    payload = {
        "mode": "ai_disabled_deterministic" if args.ai_disabled or sel.mode != "inference" else sel.mode,
        "runtime_selection": {
            "mode": sel.mode,
            "endpoint": sel.endpoint,
            "model": sel.model,
            "reason": sel.reason,
        },
        "batch_demo": {
            "batch_id": "NCB204-B24071",
            "readiness_state": batch.get("readiness_state"),
            "execution_status": batch.get("execution_status"),
        },
        "clinical_demo": {
            "subject_id": protocol.subject_id,
            "site_approved_protocol": protocol.site_approved_protocol,
            "global_current_protocol": protocol.global_current_protocol,
            "eligibility_decision": protocol.eligibility_decision,
            "action": protocol.action,
        },
        "finops_demo": {
            "cost_per_successful_task_usd": cost.cost_per_successful_task_stated_usd,
            "human_review_undercount_flag": cost.human_review_undercount_flag,
        },
        "notice": "Draft support only — no regulated side effects; humans remain accountable.",
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
