#!/usr/bin/env python3
"""Run AEGIS-PHARMA submission tests; write submission/evidence/test_results.json."""

from __future__ import annotations

import json
import sys
import unittest
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "evaluation"))


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _iter_tests(suite: unittest.TestSuite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from _iter_tests(item)
        else:
            yield item


def _trace(test_id: str) -> tuple[list[str], list[str], str]:
    """Map a unittest id to requirement/control IDs and a source evidence path."""
    if "test_inject_controls" in test_id:
        path = "submission/tests/test_inject_controls.py"
        if "research_clinical" in test_id:
            return ["FR-X-06"], ["TEST-INJ-D02D03", "D-203"], path
        if "inj027" in test_id:
            return ["FR-A-08"], ["TEST-INJ-027"], path
        if "inj049" in test_id:
            return ["FR-C-08"], ["TEST-INJ-049"], path
        if "inj053" in test_id:
            return ["FR-C-06"], ["TEST-INJ-053"], path
        if "inj055" in test_id:
            return ["FR-C-07"], ["TEST-INJ-055"], path
        if "inj062" in test_id:
            return ["PRI-06"], ["TEST-INJ-062"], path
        if "inj013" in test_id or "inj014" in test_id:
            return ["D-203"], ["TEST-INJ-013", "TEST-INJ-014"], path
        if "inj002" in test_id:
            return ["BR-AEGIS-05"], ["A-501"], path
        if "inj041" in test_id:
            return ["FR-B-06", "PRI-02"], ["A-502", "TEST-INJ-041"], path
        if "inj046" in test_id:
            return ["FR-X-07"], ["A-503", "TEST-INJ-046"], path
        if "hash_drift" in test_id:
            return ["SEC-02"], ["A-504", "INJ-065", "INJ-066"], path
        return ["FR-X-07"], ["TEST-INJ-REG"], path
    if "test_prohibited_actions" in test_id:
        return (
            ["GXP-03", "FR-A-06", "FR-B-08", "FR-C-04"],
            ["HG-PROHIBITED", "INJ-006"],
            "submission/tests/test_prohibited_actions.py",
        )
    if "test_authorization_freshness" in test_id:
        return ["SEC-01", "FR-X-01"], ["HG-SEC", "INJ-067"], "submission/tests/test_authorization_freshness.py"
    if "test_tool_trust" in test_id:
        return ["SEC-02", "SEC-03"], ["HG-SEC", "INJ-065", "INJ-066", "INJ-070"], "submission/tests/test_tool_trust.py"
    if "test_workflow_contracts" in test_id:
        return ["FR-X-02"], ["HG-SCHEMA"], "submission/tests/test_workflow_contracts.py"
    if "test_graders" in test_id:
        return (
            ["ARTEFACT_EXPECTATIONS.TEVV"],
            ["HG-SCHEMA", "HG-PROHIBITED", "HG-SEC", "HG-SUBGROUP"],
            "submission/evaluation/graders/test_graders.py",
        )
    return ["RUB-13"], ["HG-REPRO"], "submission/tests"


def _write_audit_export(path: Path) -> Path:
    from src.clinical_protocol import resolve_protocol_context
    from src.privacy_gates import check_deletion_against_hold, check_patient_support_minimise
    from src.workflow_batch import reconcile_batch
    from src.workflow_pv import build_pv_response
    from src.workflow_supply import build_supply_response

    protocol = resolve_protocol_context("S-301-044", "IN-014")
    payload = {
        "export_id": "AUD-PACK-POC",
        "generated_at": _now(),
        "runtime_mode": "ai_disabled_deterministic",
        "notice": "Advisory citation pack only — no disposition, final PV, allocate, ship, or recall.",
        "workflows": {
            "A_batch": reconcile_batch("NCB204-B24071", "AUD-A", "qp_eu_1"),
            "B_pv": build_pv_response(["PV-1001", "PV-1009", "PV-1014"], "AUD-B", "pv_reviewer"),
            "C_supply": build_supply_response("SH-901", "NCB204-B24062", "AUD-C", "planner"),
        },
        "cross_cutting": {
            "protocol": asdict(protocol),
            "psp_minimise": asdict(check_patient_support_minimise("PSP-17")),
            "dsr_hold": asdict(check_deletion_against_hold("S-301-044", "DSR-17")),
        },
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> int:
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()
    suite.addTests(loader.discover(str(ROOT / "tests"), pattern="test_*.py"))
    suite.addTests(loader.discover(str(ROOT / "evaluation" / "graders"), pattern="test_*.py"))
    discovered = list(_iter_tests(suite))

    result = unittest.TextTestRunner(verbosity=2).run(suite)
    failed_ids = {test.id(): err for test, err in result.failures + result.errors}
    stamp = _now()
    rows = []
    for test in discovered:
        test_id = test.id()
        reqs, controls, ev_path = _trace(test_id)
        status = "fail" if test_id in failed_ids else "pass"
        row = {
            "suite": test.__class__.__module__,
            "test_id": test_id,
            "requirement_ids": reqs,
            "control_ids": controls,
            "result": status,
            "timestamp": stamp,
            "runtime_mode": "ai_disabled_deterministic",
            "evidence_path": ev_path,
        }
        if status == "fail":
            row["detail"] = (failed_ids[test_id] or "")[:500]
        rows.append(row)

    out = {
        "suite": "submission/tests + evaluation graders",
        "runner": "python submission/scripts/test.py",
        "generated_at": stamp,
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
    if result.wasSuccessful():
        from src.inject_controls import write_register

        register = write_register(evidence / "INJECT_CONTROL_REGISTER.md")
        print(f"wrote {register.relative_to(REPO)}")
        audit = _write_audit_export(evidence / "audit_export.json")
        print(f"wrote {audit.relative_to(REPO)}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
