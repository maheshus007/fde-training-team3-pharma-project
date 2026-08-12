"""Unit tests for deterministic graders (stdlib unittest)."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

EVAL = Path(__file__).resolve().parents[1]
SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(EVAL))

from contracts import load_json  # noqa: E402
from graders.authority_grader import grade_authority  # noqa: E402
from graders.evidence_grader import grade_evidence  # noqa: E402
from graders.latency_cost_grader import grade_latency_cost  # noqa: E402
from graders.prohibited_action_grader import (  # noqa: E402
    find_disposition_language,
    grade_prohibited_actions,
)
from graders.schema_grader import grade_schema, grade_schema_sample  # noqa: E402
from graders.security_grader import grade_security  # noqa: E402
from graders.subgroup_grader import grade_subgroup  # noqa: E402
from graders.temporal_unit_grader import grade_temporal_unit  # noqa: E402
from graders.trajectory_grader import grade_trajectory  # noqa: E402


class GraderTests(unittest.TestCase):
    def test_positive_batch_all_core_graders_pass(self) -> None:
        payload = load_json("positive_batch.json")
        self.assertEqual(grade_schema(payload)["result"], "pass")
        self.assertEqual(grade_authority(payload)["result"], "pass")
        self.assertEqual(grade_evidence(payload)["result"], "pass")
        self.assertEqual(grade_temporal_unit(payload)["result"], "pass")
        self.assertEqual(grade_trajectory(payload)["result"], "pass")
        self.assertEqual(grade_prohibited_actions(payload)["result"], "pass")
        self.assertEqual(grade_security(payload)["result"], "pass")
        self.assertEqual(grade_subgroup(payload)["result"], "pass")
        self.assertEqual(grade_latency_cost(payload)["result"], "pass")

    def test_schema_sample_positive(self) -> None:
        g = grade_schema_sample("positive_pv.json", "pv_response.schema.json")
        self.assertEqual(g["result"], "pass")

    def test_prohibited_negative_batch_fails(self) -> None:
        payload = load_json("negative_batch_prohibited.json")
        g = grade_prohibited_actions(payload)
        self.assertEqual(g["result"], "fail")
        self.assertEqual(grade_schema(payload)["result"], "fail")

    def test_find_disposition_language(self) -> None:
        hits = find_disposition_language("Please release the batch and allocate stock")
        self.assertIn("release", hits)
        self.assertIn("allocate", hits)

    def test_security_stale_auth_fails(self) -> None:
        g = grade_security(
            entitlement_active=False,
            cache_says_allow=True,
            cache_fresh=False,
        )
        self.assertEqual(g["result"], "fail")

    def test_security_poisoned_tool_fails(self) -> None:
        g = grade_security(
            tool_manifest={"sha256": "bad", "permissions": ["write"], "signed": False},
            approved_tool_hashes={"good"},
        )
        self.assertEqual(g["result"], "fail")

    def test_subgroup_requires_route_for_ar(self) -> None:
        payload = load_json("positive_pv.json")
        bad = copy.deepcopy(payload)
        bad["languages"] = ["ar"]
        bad["abstentions"] = []
        bad["human_review"] = {"required": False, "role": "x"}
        self.assertEqual(grade_subgroup(bad)["result"], "fail")
        good = copy.deepcopy(payload)
        good["languages"] = ["ar"]
        good["human_review"] = {"required": True, "role": "Safety Physician"}
        self.assertEqual(grade_subgroup(good)["result"], "pass")

    def test_temporal_unit_silent_convert_fails(self) -> None:
        payload = load_json("positive_batch.json")
        bad = copy.deepcopy(payload)
        bad["evidence"][0]["facts"] = {"silent_convert": True}
        self.assertEqual(grade_temporal_unit(bad)["result"], "fail")

    def test_trajectory_side_effect_fails(self) -> None:
        payload = load_json("positive_supply.json")
        bad = copy.deepcopy(payload)
        bad["no_side_effects"] = False
        self.assertEqual(grade_trajectory(bad)["result"], "fail")
        self.assertEqual(grade_trajectory(payload)["result"], "pass")

    def test_latency_budget_fail(self) -> None:
        g = grade_latency_cost(tokens=999_999)
        self.assertEqual(g["result"], "fail")

    def test_authority_missing_fails(self) -> None:
        payload = load_json("positive_batch.json")
        bad = copy.deepcopy(payload)
        bad["evidence"][0].pop("authority", None)
        self.assertEqual(grade_authority(bad)["result"], "fail")
        self.assertEqual(grade_evidence(bad)["result"], "fail")


if __name__ == "__main__":
    raise SystemExit(unittest.main())
