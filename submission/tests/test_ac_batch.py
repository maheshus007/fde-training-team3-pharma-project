"""AC tests for FR-A (T-009). Engine pack; submit_workflow is T-013."""
from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    from src.engines.batch import build_batch_pack
except Exception:
    build_batch_pack = None  # type: ignore

from src.contracts import validate_workflow_response  # noqa: E402

_REQUEST = {
    "request_id": "REQ-A-1",
    "as_of": "2026-08-01T08:00:00Z",
    "workflow": "batch_evidence",
    "batch_id": "NCB204-B24071",
    "authorization": {
        "user": "qp_eu_1",
        "purpose": "batch_review_readiness",
        "object_id": "NCB204-B24071",
        "role": "qualified_person",
    },
}


@unittest.skipUnless(build_batch_pack is not None, "T-009 not implemented")
class BatchAcTests(unittest.TestCase):
    def test_ac_a1_schema(self) -> None:
        pack = build_batch_pack(_REQUEST)
        self.assertNotIn("error", pack)
        self.assertEqual(validate_workflow_response(pack), [])

    def test_ac_a2_genealogy(self) -> None:
        pack = build_batch_pack(_REQUEST)
        blob = json.dumps(pack).lower()
        self.assertIn("sua-88", blob)
        self.assertIn("missing_branch", blob)
        self.assertIn("issued", blob)
        self.assertEqual(pack["readiness_state"], "conflicted_evidence")

    def test_ac_a3_unit_abstain(self) -> None:
        pack = build_batch_pack(_REQUEST)
        codes = [a.get("code") for a in pack["abstentions"]]
        self.assertIn("unit_unapproved", codes)

    def test_ac_a4_disposition_rejected(self) -> None:
        bad = dict(_REQUEST)
        bad["batch_disposition"] = "release"
        out = build_batch_pack(bad)
        self.assertEqual(out["error"]["code"], "AEGIS-422")

    def test_ac_a5_ai_disabled(self) -> None:
        previous = os.environ.get("AEGIS_RUNTIME_MODE")
        os.environ["AEGIS_RUNTIME_MODE"] = "ai_disabled"
        try:
            pack = build_batch_pack(_REQUEST)
            blob = json.dumps(pack).lower()
            self.assertIn("missing_branch", blob)
            self.assertIn("issued", blob)
            codes = [a.get("code") for a in pack["abstentions"]]
            self.assertIn("unit_unapproved", codes)
        finally:
            if previous is None:
                os.environ.pop("AEGIS_RUNTIME_MODE", None)
            else:
                os.environ["AEGIS_RUNTIME_MODE"] = previous

    def test_ac_a6_oos_conflict(self) -> None:
        pack = build_batch_pack(_REQUEST)
        blob = json.dumps(pack)
        self.assertIn("OOS", blob)
        self.assertIn("OOT", blob)
        self.assertIn("invalid", blob.lower())

    def test_ac_a7_qp_gap(self) -> None:
        pack = build_batch_pack(_REQUEST)
        kinds = [g.get("kind") for g in pack["gaps"]]
        self.assertIn("supplier_audit_commitment", kinds)
