#!/usr/bin/env python3
"""Evaluate golden A/B/C packs against package schemas (assessment, no Azure)."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("AEGIS_RUNTIME_MODE", "assessment")

from src.contracts import validate_workflow_response  # noqa: E402
from src.service import submit_workflow  # noqa: E402

REQUESTS = [
    {
        "request_id": "EVAL-A",
        "idempotency_key": "idem-eval-batch-01",
        "as_of": "2026-08-01T08:00:00Z",
        "workflow": "batch_evidence",
        "batch_id": "NCB204-B24071",
        "authorization": {
            "user": "qp_eu_1",
            "purpose": "batch_review_readiness",
            "object_id": "NCB204-B24071",
            "role": "qualified_person",
        },
    },
    {
        "request_id": "EVAL-B",
        "idempotency_key": "idem-eval-pv-01",
        "as_of": "2026-08-01T08:00:00Z",
        "workflow": "pv_intake",
        "case_ids": ["PV-1001", "PV-1009", "PV-1014"],
        "authorization": {
            "user": "pv_assessor_1",
            "purpose": "pv_intake",
            "object_id": "PV-1001",
            "role": "pv_assessor",
        },
    },
    {
        "request_id": "EVAL-C",
        "idempotency_key": "idem-eval-supply-01",
        "as_of": "2026-08-01T08:00:00Z",
        "workflow": "supply_options",
        "event_id": "SH-901",
        "authorization": {
            "user": "supply_planner_1",
            "purpose": "supply_options",
            "object_id": "SH-901",
            "role": "supply_planner",
        },
    },
]


def main() -> int:
    errors: list[str] = []
    rows: list[dict[str, object]] = []
    for request in REQUESTS:
        pack = submit_workflow(request)
        workflow = str(request["workflow"])
        if "error" in pack:
            errors.append(f"{workflow}: {pack['error']}")
            rows.append({"workflow": workflow, "ok": False})
            continue
        schema = validate_workflow_response(pack)
        if schema:
            errors.append(f"{workflow}: {schema[:3]}")
            rows.append({"workflow": workflow, "ok": False})
        else:
            rows.append({"workflow": workflow, "ok": True, "execution_status": pack.get("execution_status")})
    report = {"mode": "assessment", "passed": not errors, "results": rows, "errors": errors}
    out = ROOT / "evidence" / "evaluation_results.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
