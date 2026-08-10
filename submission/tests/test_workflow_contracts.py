"""Contract tests: positive examples pass; prohibited actions fail closed.

Prefers evaluation/contract_samples and evaluation/contracts when present;
falls back to submission/tests/fixtures/.
"""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.contracts import (  # noqa: E402
    LOCAL_FIXTURES,
    PROHIBITED_BY_WORKFLOW,
    load_json,
    prohibited_field_errors,
    resolve_contracts_dir,
    resolve_samples_dir,
    validate,
    validate_named,
    validate_workflow_response,
)


class WorkflowContractTests(unittest.TestCase):
    def test_positive_batch(self) -> None:
        self.assertEqual(validate_named("positive_batch.json", "batch_response.schema.json"), [])

    def test_positive_pv(self) -> None:
        self.assertEqual(validate_named("positive_pv.json", "pv_response.schema.json"), [])

    def test_positive_supply(self) -> None:
        self.assertEqual(validate_named("positive_supply.json", "supply_response.schema.json"), [])

    def test_negative_batch_prohibited(self) -> None:
        errs = validate_named("negative_batch_prohibited.json", "batch_response.schema.json")
        self.assertTrue(errs)
        self.assertTrue(any("batch_disposition" in e for e in errs), msg=errs)

    def test_negative_pv_prohibited(self) -> None:
        errs = validate_named("negative_pv_prohibited.json", "pv_response.schema.json")
        self.assertTrue(errs)
        self.assertTrue(any("final_reportability" in e for e in errs), msg=errs)

    def test_negative_supply_side_effect(self) -> None:
        errs = validate_named("negative_supply_side_effect.json", "supply_response.schema.json")
        self.assertTrue(errs)

    def test_negative_pv_causality_fails_closed(self) -> None:
        path = LOCAL_FIXTURES / "negative_pv_causality.json"
        self.assertTrue(path.is_file())
        payload = load_json("negative_pv_causality.json")
        self.assertIn("causality_assessment", payload)
        errs = validate_workflow_response(payload)
        self.assertTrue(errs)
        self.assertTrue(any("causality_assessment" in e for e in errs), msg=errs)

    def test_additional_properties_denied(self) -> None:
        payload = copy.deepcopy(load_json("positive_batch.json"))
        payload["unexpected_execution_flag"] = True
        schema = load_json("batch_response.schema.json")
        errs = validate(payload, schema, contracts_dir=resolve_contracts_dir())
        self.assertTrue(any("additional property unexpected_execution_flag" in e for e in errs), msg=errs)

    def test_prohibited_helpers_cover_workflows(self) -> None:
        for workflow, fields in PROHIBITED_BY_WORKFLOW.items():
            sample = {
                "batch_evidence": "positive_batch.json",
                "pv_intake": "positive_pv.json",
                "supply_options": "positive_supply.json",
            }[workflow]
            payload = copy.deepcopy(load_json(sample))
            banned = next(iter(fields))
            payload[banned] = "forbidden"
            errs = prohibited_field_errors(payload, workflow)
            self.assertTrue(any(banned in e for e in errs), msg=(workflow, errs))

    def test_resolvers_available(self) -> None:
        self.assertTrue((resolve_contracts_dir() / "batch_response.schema.json").is_file())
        self.assertTrue((resolve_samples_dir() / "positive_batch.json").is_file())


if __name__ == "__main__":
    raise SystemExit(unittest.main())
