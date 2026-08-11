"""AC tests for FR-B (T-010). Engine pack; submit_workflow is T-013."""
from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    from src.engines.pv import build_pv_pack
except Exception:
    build_pv_pack = None  # type: ignore

from src.contracts import validate_workflow_response  # noqa: E402

_CASES = ["PV-1001", "PV-1009", "PV-1014"]


def _request(*, user: str = "pv_assessor_1", role: str = "pv_assessor", case_ids: list[str] | None = None) -> dict:
    ids = case_ids if case_ids is not None else list(_CASES)
    return {
        "request_id": "REQ-B-1",
        "as_of": "2026-08-01T08:00:00Z",
        "workflow": "pv_intake",
        "case_ids": ids,
        "authorization": {
            "user": user,
            "purpose": "pv_intake",
            "object_id": ids[0],
            "role": role,
        },
    }


@unittest.skipUnless(build_pv_pack is not None, "T-010 not implemented")
class PvAcTests(unittest.TestCase):
    def test_ac_b1_schema(self) -> None:
        pack = build_pv_pack(_request())
        self.assertNotIn("error", pack)
        self.assertEqual(validate_workflow_response(pack), [])

    def test_ac_b2_duplicates_include_pv1009(self) -> None:
        pack = build_pv_pack(_request())
        blob = json.dumps(pack["duplicate_candidates"])
        self.assertIn("PV-1001", blob)
        self.assertIn("PV-1009", blob)
        self.assertIn("PV-1014", blob)
        self.assertNotIn("merge", blob)

    def test_ac_b3_clocks(self) -> None:
        pack = build_pv_pack(_request())
        channels = {c.get("channel") for c in pack["clock_evidence"]}
        self.assertTrue({"vendor", "affiliate", "global"} <= channels)

    def test_ac_b4_listedness(self) -> None:
        pack = build_pv_pack(_request())
        docs = {row.get("source_doc") for row in pack["listedness_context"]}
        listed = {row.get("listed") for row in pack["listedness_context"]}
        self.assertIn("IB", docs)
        self.assertIn("CCDS", docs)
        self.assertIn("local_label", docs)
        self.assertIn("yes", listed)
        self.assertIn("no", listed)

    def test_ac_b5_final_reportability_rejected(self) -> None:
        req = _request()
        req["final_reportability"] = "reportable"
        out = build_pv_pack(req)
        self.assertEqual(out["error"]["code"], "AEGIS-422")

    def test_ac_b6_ai_disabled(self) -> None:
        previous = os.environ.get("AEGIS_RUNTIME_MODE")
        os.environ["AEGIS_RUNTIME_MODE"] = "ai_disabled"
        try:
            pack = build_pv_pack(_request())
            blob = json.dumps(pack["duplicate_candidates"])
            self.assertIn("PV-1009", blob)
        finally:
            if previous is None:
                os.environ.pop("AEGIS_RUNTIME_MODE", None)
            else:
                os.environ["AEGIS_RUNTIME_MODE"] = previous

    def test_ac_b7_meddra_versions(self) -> None:
        pack = build_pv_pack(_request())
        versions = {t.get("meddra_version") for t in pack["terminology"]}
        self.assertIn("27.1", versions)
        self.assertIn("28.0", versions)

    def test_ac_b8_sensitive_segment(self) -> None:
        denied = build_pv_pack(_request(user="auditor_1", role="auditor", case_ids=["PV-1020", "PV-1001"]))
        allowed = build_pv_pack(_request(user="pv_medical_1", role="pv_medical", case_ids=["PV-1020", "PV-1001"]))
        denied_vals = json.dumps(denied.get("source_facts", []))
        allowed_vals = json.dumps(allowed.get("source_facts", []))
        self.assertNotIn("[sensitive]", denied_vals)
        self.assertIn("[sensitive]", allowed_vals)

    def test_ac_b9_social_abstain(self) -> None:
        pack = build_pv_pack(_request())
        codes = [a.get("code") for a in pack["abstentions"]]
        self.assertIn("authenticity_failed", codes)
