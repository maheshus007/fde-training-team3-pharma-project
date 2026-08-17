"""Deterministic inject-control tests for INJ-001..084 (TEST-INJ-REG)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.clinical_protocol import resolve_protocol_context  # noqa: E402
from src.inject_controls import (  # noqa: E402
    OUT_OF_WRITE_PATH,
    catalog,
    evaluate,
    evaluate_all,
    resolve_evidence,
)
from src.privacy_gates import check_patient_support_minimise  # noqa: E402
from src.workflow_batch import reconcile_batch  # noqa: E402
from src.workflow_supply import build_supply_response  # noqa: E402


class InjectRegisterTests(unittest.TestCase):
    def test_catalog_is_exactly_84(self) -> None:
        ids = [item["id"] for item in catalog()]
        expected = [f"INJ-{i:03d}" for i in range(1, 85)]
        self.assertEqual(ids, expected)

    def test_every_inject_has_resolved_evidence(self) -> None:
        for item in catalog():
            paths = resolve_evidence(item)
            self.assertTrue(paths, item["id"])
            for rel in paths:
                self.assertTrue((ROOT.parent / rel).is_file(), rel)

    def test_evaluate_all_covers_84(self) -> None:
        controls = evaluate_all()
        self.assertEqual(len(controls), 84)
        self.assertEqual([c.inject_id for c in controls], [f"INJ-{i:03d}" for i in range(1, 85)])
        for control in controls:
            self.assertTrue(control.action)
            self.assertTrue(control.evidence_paths)


class GapInjectBehaviourTests(unittest.TestCase):
    def test_research_clinical_write_path_abstains(self) -> None:
        for iid in sorted(OUT_OF_WRITE_PATH):
            control = evaluate(iid)
            self.assertEqual(control.action, "abstain", iid)
            self.assertEqual(control.owner, "research_clinical_boundary", iid)

    def test_inj027_pat_recipe_mismatch_surfaced(self) -> None:
        control = evaluate("INJ-027")
        self.assertEqual(control.action, "surface")
        blob = " ".join(control.observed)
        self.assertIn("2.4", blob)
        self.assertIn("2.3", blob)
        pack = reconcile_batch("NCB204-B24071", "REQ-PAT", "qp_eu_1")
        self.assertTrue(any("INJ-027" in a["detail"] for a in pack["abstentions"]))

    def test_inj049_variation_not_classified(self) -> None:
        control = evaluate("INJ-049")
        self.assertEqual(control.action, "abstain")
        self.assertIn("open", control.observed[0])
        supply = build_supply_response("SH-901", "NCB204-B24062", "REQ-VAR", "planner")
        self.assertTrue(any("INJ-049" in a["detail"] for a in supply["abstentions"]))

    def test_inj053_counterfeit_no_recall(self) -> None:
        control = evaluate("INJ-053")
        self.assertEqual(control.action, "surface")
        supply = build_supply_response("SH-901", "NCB204-B24062", "REQ-CF", "planner")
        self.assertTrue(any("INJ-053" in g["detail"] for g in supply["gaps"]))
        self.assertNotIn("recall", supply.get("execution_status", ""))

    def test_inj055_cmo_overpromise_is_constraint(self) -> None:
        control = evaluate("INJ-055")
        self.assertEqual(control.action, "surface")
        self.assertIn("CMO-IE", control.observed[0])
        self.assertIn("other=1", control.observed[0])
        supply = build_supply_response("SH-901", "NCB204-B24062", "REQ-CMO", "planner")
        self.assertTrue(any("INJ-055" in g["detail"] for g in supply["gaps"]))

    def test_inj062_patient_support_minimised(self) -> None:
        control = evaluate("INJ-062")
        self.assertEqual(control.action, "deny")
        decision = check_patient_support_minimise("PSP-17")
        self.assertEqual(decision.action, "deny")

    def test_inj013_014_use_fixture_protocol_versions(self) -> None:
        ctx = resolve_protocol_context("S-301-044", "IN-014")
        self.assertEqual(ctx.eligibility_decision, "not_decided")
        self.assertIn("v4.1", ctx.site_approved_protocol)
        self.assertIn("v5.0", ctx.global_current_protocol)
        self.assertNotIn("v3.1", ctx.site_approved_protocol)


class ChallengeDataTensionTests(unittest.TestCase):
    def test_inj002_records_missing_supply_kpi(self) -> None:
        control = evaluate("INJ-002")
        self.assertEqual(control.action, "record_conflict")
        self.assertTrue(any("Supply" in note for note in control.observed))

    def test_inj041_records_join_gap(self) -> None:
        control = evaluate("INJ-041")
        self.assertEqual(control.action, "record_conflict")
        self.assertTrue(any("PV-1020" in note for note in control.observed))

    def test_inj046_does_not_invent_pending_us_label(self) -> None:
        control = evaluate("INJ-046")
        self.assertEqual(control.action, "record_conflict")
        self.assertTrue(any("pending" in note.lower() for note in control.observed))
        self.assertIn("do not invent", control.notes.lower())

    def test_hash_drift_is_recorded_not_overwritten(self) -> None:
        inj065 = evaluate("INJ-065")
        inj066 = evaluate("INJ-066")
        self.assertEqual(inj065.action, "deny")
        self.assertEqual(inj066.action, "deny")
        self.assertTrue(any("hash_drift" in note for note in inj065.observed))
        self.assertTrue(any("hash_drift" in note for note in inj066.observed))
        self.assertIn("do not overwrite", " ".join(inj065.observed).lower())
