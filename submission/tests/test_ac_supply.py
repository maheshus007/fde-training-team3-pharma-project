"""AC tests for FR-C (T-011). Engine pack; submit_workflow is T-013."""
from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    from src.engines.supply import build_supply_pack
except Exception:
    build_supply_pack = None  # type: ignore

from src.contracts import validate_workflow_response  # noqa: E402

_REQUEST = {
    "request_id": "REQ-C-1",
    "as_of": "2026-08-01T08:00:00Z",
    "workflow": "supply_options",
    "event_id": "SH-901",
    "authorization": {
        "user": "supply_planner_1",
        "purpose": "supply_options",
        "object_id": "SH-901",
        "role": "supply_planner",
    },
}


@unittest.skipUnless(build_supply_pack is not None, "T-011 not implemented")
class SupplyAcTests(unittest.TestCase):
    def test_ac_c1_schema_no_side_effects(self) -> None:
        pack = build_supply_pack(_REQUEST)
        self.assertNotIn("error", pack)
        self.assertTrue(pack["no_side_effects"])
        self.assertEqual(validate_workflow_response(pack), [])
        for option in pack["options"]:
            self.assertEqual(option["status"], "draft")
            self.assertNotIn("reservation_id", option)
            self.assertNotIn("allocation_id", option)
            self.assertNotIn("shipment_id", option)

    def test_ac_c2_sh901_association(self) -> None:
        pack = build_supply_pack(_REQUEST)
        blob = json.dumps(pack)
        self.assertIn("LG-31", blob)
        self.assertIn("P-88", blob)
        self.assertIn("P-89", blob)

    def test_ac_c3_reservation_rejected(self) -> None:
        bad = dict(_REQUEST)
        bad["reservation_id"] = "RSV-1"
        out = build_supply_pack(bad)
        self.assertEqual(out["error"]["code"], "AEGIS-422")

    def test_ac_c4_ai_disabled(self) -> None:
        previous = os.environ.get("AEGIS_RUNTIME_MODE")
        os.environ["AEGIS_RUNTIME_MODE"] = "ai_disabled"
        try:
            pack = build_supply_pack(_REQUEST)
            self.assertGreaterEqual(len(pack["options"]), 1)
            self.assertTrue(all(o["status"] == "draft" for o in pack["options"]))
        finally:
            if previous is None:
                os.environ.pop("AEGIS_RUNTIME_MODE", None)
            else:
                os.environ["AEGIS_RUNTIME_MODE"] = previous

    def test_ac_c5_channel_constraints(self) -> None:
        pack = build_supply_pack(_REQUEST)
        channels = {c.get("channel") for c in pack["constraints"]}
        self.assertIn("trial", channels)
        self.assertIn("compassionate", channels)
        self.assertIn("commercial", channels)
