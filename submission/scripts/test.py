#!/usr/bin/env python3
"""Run AEGIS-PHARMA submission tests; write submission/evidence/test_results.json."""

from __future__ import annotations

import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "evaluation"))


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> int:
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()
    suite.addTests(loader.discover(str(ROOT / "tests"), pattern="test_*.py"))
    suite.addTests(loader.discover(str(ROOT / "evaluation" / "graders"), pattern="test_*.py"))

    result = unittest.TextTestRunner(verbosity=2).run(suite)

    rows = []
    for test, err in result.failures + result.errors:
        rows.append(
            {
                "suite": test.__class__.__module__,
                "test_id": test.id(),
                "requirement_ids": ["RUB-13", "TEVV"],
                "control_ids": ["HG-REPRO"],
                "result": "fail",
                "timestamp": _now(),
                "runtime_mode": "ai_disabled_deterministic",
                "evidence_path": "submission/evidence/test_results.json",
                "detail": (err or "")[:500],
            }
        )
    # Record successful tests from result (unittest does not keep a full pass list easily)
    # Emit summary rows for discovered modules when all OK.
    if result.wasSuccessful():
        rows.append(
            {
                "suite": "submission/tests + submission.evaluation.graders",
                "test_id": "ALL",
                "requirement_ids": ["RUB-13", "ARTEFACT_EXPECTATIONS.TEVV"],
                "control_ids": ["HG-SCHEMA", "HG-PROHIBITED", "HG-SEC", "HG-SUBGROUP"],
                "result": "pass",
                "timestamp": _now(),
                "runtime_mode": "ai_disabled_deterministic",
                "evidence_path": "submission/tests;submission/evaluation/graders/test_graders.py",
                "tests_run": result.testsRun,
            }
        )

    out = {
        "suite": "submission/tests + evaluation graders",
        "runner": "python submission/scripts/test.py",
        "generated_at": _now(),
        "runtime_mode": "ai_disabled_deterministic",
        "tests_run": result.testsRun,
        "passed": result.testsRun - len(result.failures) - len(result.errors),
        "failed": len(result.failures) + len(result.errors),
        "status": "OK" if result.wasSuccessful() else "FAIL",
        "results": rows,
        "evidence_path": "submission/evidence/test_results.json",
    }
    evidence = ROOT / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "test_results.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {(evidence / 'test_results.json').relative_to(REPO)}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
