"""AC stubs for FR-E (Prompt 10). Unskip as Prompt 11 T-005..T-007 land."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    from src.adapters import graph_memory as graph_memory
except Exception:
    graph_memory = None  # type: ignore

try:
    from src import service
except Exception:
    service = None  # type: ignore

_GRAPH_READY = bool(getattr(graph_memory, "SUPPORTS_CQ", False)) or (
    service is not None and hasattr(service, "query_graph")
)
_INGEST_READY = bool(getattr(graph_memory, "SUPPORTS_INGEST", False))


@unittest.skipUnless(_INGEST_READY, "T-005 ingest not implemented")
class GraphIngestTests(unittest.TestCase):
    def test_ac_e4_forbidden_edge(self) -> None:
        g = graph_memory.MemoryGraph()
        count = g.ingest_from_fixtures()
        self.assertGreater(count, 0)
        self.assertEqual(g.ingest_from_fixtures(), count)
        with self.assertRaises(ValueError):
            g.add_edge("RESERVED_FOR", "a", "b")
        with self.assertRaises(ValueError):
            g.add_edge("CASE_MERGED", "PV-1001", "PV-1009")


@unittest.skipUnless(_GRAPH_READY, "T-006 CQ queries not implemented")
class GraphAcTests(unittest.TestCase):
    def setUp(self) -> None:
        self.g = graph_memory.MemoryGraph()
        self.g.ingest_from_fixtures()

    def test_ac_e1_cq1_genealogy(self) -> None:
        result = self.g.query(
            "CQ-1",
            {"batch_id": "NCB204-B24071"},
            "batch_review_readiness",
            "2026-08-01T08:00:00Z",
        )
        blob = json.dumps(result)
        self.assertEqual(result["cq_id"], "CQ-1")
        self.assertIn("SUA-88", blob)
        self.assertIn("MISSING_BRANCH", blob)
        self.assertIn("ISSUED", blob)
        self.assertLessEqual(len(result["paths"]), 50)
        self.assertFalse(result["truncated"])

    def test_ac_e2_cq2_unit_abstain(self) -> None:
        result = self.g.query(
            "CQ-2",
            {"lab_result_id": "LR-88"},
            "batch_review_readiness",
            "2026-08-01T08:00:00Z",
        )
        codes = [a.get("code") for a in result["abstentions"]]
        self.assertIn("unit_unapproved", codes)
        self.assertIn("LR-88", json.dumps(result))

    def test_ac_e3_cq6_logger_pallet(self) -> None:
        result = self.g.query(
            "CQ-6",
            {"shipment_id": "SH-901"},
            "supply_options",
            "2026-08-01T08:00:00Z",
        )
        blob = json.dumps(result)
        self.assertIn("LG-31", blob)
        self.assertIn("P-88", blob)
        self.assertIn("P-89", blob)
        self.assertNotIn("NCB204-B24071", json.dumps(result.get("paths", [])))


@unittest.skipUnless(
    bool(getattr(graph_memory, "SUPPORTS_CQ3", False)),
    "T-007 CQ-3 not implemented",
)
class GraphCq3Tests(unittest.TestCase):
    def test_ac_e5_cq3_pv1009(self) -> None:
        g = graph_memory.MemoryGraph()
        g.ingest_from_fixtures()
        result = g.query(
            "CQ-3",
            {"case_ids": ["PV-1001", "PV-1009", "PV-1014"]},
            "pv_intake",
            "2026-08-01T08:00:00Z",
        )
        blob = json.dumps(result)
        self.assertEqual(result["cq_id"], "CQ-3")
        self.assertIn("PV-1001", blob)
        self.assertIn("PV-1009", blob)
        self.assertIn("PV-1014", blob)
        self.assertIn("DUPLICATE_CANDIDATE", blob)
        self.assertNotIn("CASE_MERGED", blob)
        self.assertNotIn('"merge"', blob)
        similarities = []
        for path in result["paths"]:
            self.assertEqual(set(path.keys()), {"nodes", "edges", "provenance"})
            for prov in path.get("provenance") or []:
                self.assertNotIn("merge", prov)
                if "similarity" in prov:
                    similarities.append(prov["similarity"])
        rounded = {round(float(s), 2) for s in similarities}
        self.assertIn(0.93, rounded)
        self.assertIn(0.71, rounded)
