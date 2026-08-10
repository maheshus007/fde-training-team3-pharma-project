"""Deterministic prohibited-action tests (INJ-006 hard gates)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.policy_guard import check_workflow_payload  # noqa: E402


class ProhibitedActionTests(unittest.TestCase):
    def test_batch_release_denied(self) -> None:
        d = check_workflow_payload(
            "batch_evidence",
            {"disposition": "release", "execution_status": "executed"},
        )
        self.assertFalse(d.allow)

    def test_batch_reject_denied(self) -> None:
        d = check_workflow_payload("batch_evidence", {"reject_decision": "reject"})
        self.assertFalse(d.allow)

    def test_batch_reprocess_denied(self) -> None:
        d = check_workflow_payload("batch_evidence", {"reprocess": True})
        self.assertFalse(d.allow)

    def test_batch_recall_denied(self) -> None:
        d = check_workflow_payload("batch_evidence", {"recall": True})
        self.assertFalse(d.allow)

    def test_pv_final_causality_denied(self) -> None:
        d = check_workflow_payload("pv_intake", {"final_causality": "related"})
        self.assertFalse(d.allow)

    def test_pv_final_seriousness_denied(self) -> None:
        d = check_workflow_payload("pv_intake", {"final_seriousness": "serious"})
        self.assertFalse(d.allow)

    def test_pv_reportability_denied(self) -> None:
        d = check_workflow_payload("pv_intake", {"final_reportability": "expedited"})
        self.assertFalse(d.allow)

    def test_pv_signal_confirmation_denied(self) -> None:
        d = check_workflow_payload("pv_intake", {"signal_confirmation": True})
        self.assertFalse(d.allow)

    def test_supply_reserve_denied(self) -> None:
        d = check_workflow_payload("supply_planning", {"reserve": {"qty": 5}})
        self.assertFalse(d.allow)

    def test_supply_allocate_denied(self) -> None:
        d = check_workflow_payload(
            "supply_planning",
            {"allocate": {"qty": 10}, "no_side_effects": False},
        )
        self.assertFalse(d.allow)

    def test_supply_ship_denied(self) -> None:
        d = check_workflow_payload("supply_planning", {"ship": True})
        self.assertFalse(d.allow)

    def test_supply_quality_status_denied(self) -> None:
        d = check_workflow_payload(
            "supply_planning",
            {"quality_status_change": "quarantine"},
        )
        self.assertFalse(d.allow)

    def test_supply_recall_initiate_denied(self) -> None:
        d = check_workflow_payload("supply_planning", {"recall_initiate": True})
        self.assertFalse(d.allow)

    def test_clean_batch_allowed(self) -> None:
        d = check_workflow_payload(
            "batch_evidence",
            {"execution_status": "not_executed", "gaps": []},
        )
        self.assertTrue(d.allow)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
