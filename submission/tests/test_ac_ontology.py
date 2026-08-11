"""Ontology gate stubs (Prompt 10). Unskip when src.ontology exists (T-008)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    from src import ontology
except Exception:
    ontology = None  # type: ignore


@unittest.skipUnless(ontology is not None, "T-008 not implemented")
class OntologyAcTests(unittest.TestCase):
    def test_ac_a3_unit_unapproved(self) -> None:
        result = ontology.evaluate_lab_comparability("LR-88")
        self.assertFalse(result["allowed"])
        self.assertIsNone(result["converted_value"])
        self.assertEqual(result["abstention"]["code"], "unit_unapproved")

    def test_cq5_idmp_not_equal(self) -> None:
        result = ontology.resolve_product_identity("NCB-204", "NCB204-DE")
        self.assertFalse(result["same_product"])
        self.assertEqual(result["status"], "conflict")
        self.assertFalse(result["merged"])

    def test_meddra_version_retained(self) -> None:
        v271 = ontology.retain_coding(
            {
                "case_id": "PV-1001",
                "verbatim": "anaphylactic reaction",
                "pt": "Anaphylactic reaction",
                "meddra_version": "27.1",
            }
        )
        v280 = ontology.retain_coding(
            {
                "case_id": "PV-1014",
                "verbatim": "breathing difficulty after infusion",
                "pt": "Infusion related reaction",
                "meddra_version": "28.0",
            }
        )
        self.assertEqual(v271["meddra_version"], "27.1")
        self.assertEqual(v280["meddra_version"], "28.0")
        self.assertNotEqual(v271["meddra_version"], v280["meddra_version"])
