"""AC tests for FR-F HITL ack (T-013). Taipy app is T-016."""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    from src import service
except Exception:
    service = None  # type: ignore

from src.contracts import validate_workflow_response  # noqa: E402


@unittest.skipUnless(service is not None and hasattr(service, "ack_human_review"), "T-013 not implemented")
class HitlAckTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self._prev = os.environ.get("AEGIS_EVIDENCE_ROOT")
        os.environ["AEGIS_EVIDENCE_ROOT"] = self._tmp.name

    def tearDown(self) -> None:
        if self._prev is None:
            os.environ.pop("AEGIS_EVIDENCE_ROOT", None)
        else:
            os.environ["AEGIS_EVIDENCE_ROOT"] = self._prev
        self._tmp.cleanup()

    def test_ac_f1_ack_requires_viewed_conflicts(self) -> None:
        pack = service.submit_workflow(
            {
                "request_id": "REQ-F1",
                "idempotency_key": "idem-f1-ack-01",
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
        )
        self.assertNotIn("error", pack)
        self.assertEqual(validate_workflow_response(pack), [])
        conflict_ids = [item["id"] for item in pack["contradictions"]]
        self.assertTrue(conflict_ids)
        denied = service.ack_human_review(
            {
                "request_id": "REQ-F1",
                "user": "qp_eu_1",
                "viewed_conflict_ids": [],
                "ack": True,
            }
        )
        self.assertEqual(denied["error"]["code"], "AEGIS-412")
        ok = service.ack_human_review(
            {
                "request_id": "REQ-F1",
                "user": "qp_eu_1",
                "viewed_conflict_ids": conflict_ids,
                "ack": True,
            }
        )
        self.assertTrue(ok["human_review"]["acknowledged"])
        self.assertNotIn("acknowledged", json.dumps(pack.get("human_review")))


class HitlAppSmokeTests(unittest.TestCase):
    def test_ac_f2_app_main_exists(self) -> None:
        main = ROOT / "app" / "main.py"
        canon = ROOT / "aegis-sdd" / "apps" / "web" / "main.py"
        self.assertTrue(main.is_file())
        self.assertTrue(canon.is_file())
        canon_text = canon.read_text(encoding="utf-8")
        blob = (main.read_text(encoding="utf-8") + "\n" + canon_text).lower()
        self.assertIn("127.0.0.1", blob)
        for marker in ("PAGE_BATCH", "PAGE_PV", "PAGE_SUPPLY", "PAGE_REVIEW"):
            self.assertIn(marker, canon_text)
        for name in ('"batch"', '"pv"', '"supply"', '"review"'):
            self.assertIn(name, canon_text)
        for label in (
            "|release|button",
            "|reject|button",
            "|allocate|button",
            "|reserve|button",
            "|ship|button",
            "confirm signal",
            "final causality",
            "approve release",
        ):
            self.assertNotIn(label, blob)
        self.assertNotIn("azure_openai", blob)
        self.assertNotIn("cosmos_gremlin", blob)
        self.assertNotIn("gremlinpython", blob)

        from app.main import HOST, PAGES, ack_enabled, flatten_conflicts

        self.assertEqual(
            flatten_conflicts(
                [{"id": "c1", "kind": "oos", "left": {"source": "LIMS", "verbatim": "OOS"}, "right": {"source": "stats", "verbatim": "OOT"}}]
            )[0]["left_verbatim"],
            "OOS",
        )
        self.assertEqual(HOST, "127.0.0.1")
        self.assertIn("batch", PAGES)
        self.assertIn("pv", PAGES)
        self.assertIn("supply", PAGES)
        self.assertIn("review", PAGES)
        self.assertFalse(ack_enabled({"contradictions": [{"id": "c1"}]}, ""))
        self.assertTrue(ack_enabled({"contradictions": [{"id": "c1"}]}, "c1"))
        self.assertIn("|table|", canon_text)
        self.assertIn("Load batch pack", canon_text)
        self.assertIn("advisory_note", canon_text)
        self.assertIn("priority_label", canon_text)
