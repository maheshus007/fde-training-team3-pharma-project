"""AC stubs for FR-D. Unskip per T-012a/b/c (do not wait for T-013 submit)."""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tests" / "fixtures"
sys.path.insert(0, str(ROOT))

try:
    from src import service
except Exception:
    service = None  # type: ignore

try:
    from src.orchestrator.manifests import evaluate_manifest
except Exception:
    evaluate_manifest = None  # type: ignore

try:
    from src.engines.batch import build_batch_pack
    from src.orchestrator.runtime import (
        BudgetTracker,
        KillSwitchInference,
        attach_budget_abstention,
        bounded_suggest,
        select_inference,
    )
except Exception:
    build_batch_pack = None  # type: ignore
    BudgetTracker = None  # type: ignore
    KillSwitchInference = None  # type: ignore
    attach_budget_abstention = None  # type: ignore
    bounded_suggest = None  # type: ignore
    select_inference = None  # type: ignore

try:
    from src.orchestrator.replay import ReplayStore
except Exception:
    ReplayStore = None  # type: ignore

from src.contracts import validate_workflow_response  # noqa: E402

_BATCH_REQ = {
    "request_id": "REQ-D3",
    "idempotency_key": "idem-key-d5-01",
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


@unittest.skipUnless(evaluate_manifest is not None, "T-012a not implemented")
class OrchestratorManifestTests(unittest.TestCase):
    def test_ac_d1_poisoned_manifest(self) -> None:
        poisoned = json.loads((FIX / "tool_manifest_poisoned.json").read_text(encoding="utf-8"))
        denied = evaluate_manifest(poisoned)
        self.assertFalse(denied["allow"])
        self.assertEqual(denied["error"]["error"]["code"], "AEGIS-401")

        unsigned = json.loads((FIX / "tool_manifest_poisoned_data_style.json").read_text(encoding="utf-8"))
        denied_u = evaluate_manifest(unsigned)
        self.assertFalse(denied_u["allow"])

        approved = json.loads((FIX / "tool_manifest_approved.json").read_text(encoding="utf-8"))
        allowed = evaluate_manifest(approved)
        self.assertTrue(allowed["allow"])


@unittest.skipUnless(
    select_inference is not None and build_batch_pack is not None,
    "T-012b not implemented",
)
class OrchestratorBudgetTests(unittest.TestCase):
    def test_ac_d4_kill_switch(self) -> None:
        class _Live:
            def suggest(self, kind: str, payload: dict, budget=None):
                del kind, payload, budget
                return {"used": True, "suggestions": [{"hint": "should never surface"}]}

        guarded = KillSwitchInference(_Live(), kill_switch=True)
        out = guarded.suggest("cluster_hint", {"text": "x"}, None)
        self.assertFalse(out["used"])
        self.assertEqual(out["suggestions"], [])

        request = {
            "request_id": "REQ-D4",
            "as_of": "2026-08-01T08:00:00Z",
            "workflow": "batch_evidence",
            "batch_id": "NCB204-B24071",
            "kill_switch": True,
            "authorization": {
                "user": "qp_eu_1",
                "purpose": "batch_review_readiness",
                "object_id": "NCB204-B24071",
                "role": "qualified_person",
            },
        }
        port = select_inference(request)
        hinted = port.suggest("narrative_summary", {"batch_id": "NCB204-B24071"}, None)
        self.assertFalse(hinted["used"])
        pack = build_batch_pack(request)
        self.assertNotIn("error", pack)
        self.assertEqual(pack["execution_status"], "not_executed")
        self.assertEqual(validate_workflow_response(pack), [])
        blob = json.dumps(pack).lower()
        self.assertIn("missing_branch", blob)

        tracker = BudgetTracker(max_steps=1)
        self.assertTrue(tracker.record_step())
        self.assertFalse(tracker.record_step())
        stopped = attach_budget_abstention(dict(pack), tracker)
        codes = [a.get("code") for a in stopped["abstentions"]]
        self.assertIn("budget_exhausted", codes)
        self.assertNotIn("error", stopped)
        self.assertNotEqual(stopped.get("error", {}).get("code"), "AEGIS-429")
        self.assertEqual(validate_workflow_response(stopped), [])
        over_inf = BudgetTracker(max_inference_calls=0)
        skipped = bounded_suggest(port, "cluster_hint", {}, over_inf, request)
        self.assertFalse(skipped["used"])


@unittest.skipUnless(
    ReplayStore is not None and build_batch_pack is not None,
    "T-012c not implemented",
)
class OrchestratorReplayTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.store = ReplayStore(Path(self._tmp.name))

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_ac_d3_checkpoint_resume(self) -> None:
        pack = build_batch_pack(_BATCH_REQ)
        self.assertNotIn("error", pack)
        event_id = pack["audit"]["event_id"]
        self.store.save_checkpoint("cp-d3", _BATCH_REQ, pack, step=1, termination_reason="completed")
        missing = self.store.load_checkpoint("cp-missing", "REQ-D3")
        self.assertEqual(missing["error"]["code"], "AEGIS-404")

        resume_req = dict(_BATCH_REQ)
        resume_req["resume_checkpoint_id"] = "cp-d3"
        resume_req["request_id"] = "REQ-D3-RESUME"
        resumed = self.store.resume(resume_req)
        self.assertNotIn("error", resumed)
        self.assertEqual(resumed["audit"]["event_id"], event_id)
        self.assertEqual(validate_workflow_response(resumed), [])
        sidecar = json.loads((self.store.audit / f"{event_id}.json").read_text(encoding="utf-8"))
        self.assertEqual(sidecar["resume_of"], "cp-d3")
        self.assertNotIn("resume_of", resumed["audit"])

    def test_ac_d5_idempotency(self) -> None:
        pack = build_batch_pack(_BATCH_REQ)
        first = self.store.remember(_BATCH_REQ, pack)
        self.assertEqual(first["audit"]["event_id"], pack["audit"]["event_id"])
        replayed = self.store.remember(_BATCH_REQ, pack)
        self.assertEqual(replayed["audit"]["event_id"], pack["audit"]["event_id"])
        self.assertEqual(validate_workflow_response(replayed), [])
        sidecar = json.loads(
            (self.store.audit / f"{pack['audit']['event_id']}.json").read_text(encoding="utf-8")
        )
        self.assertTrue(sidecar["replay"])
        self.assertNotIn("replay", replayed["audit"])

        conflict_req = dict(_BATCH_REQ)
        conflict_req["kill_switch"] = True
        conflict = self.store.remember(conflict_req, pack)
        self.assertEqual(conflict["error"]["code"], "AEGIS-409")


@unittest.skipUnless(service is not None and hasattr(service, "submit_workflow"), "T-013 not implemented")
class OrchestratorAcTests(unittest.TestCase):
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

    def test_ac_d2_stale_auth(self) -> None:
        out = service.submit_workflow(
            {
                "request_id": "REQ-D2",
                "idempotency_key": "idem-d2-stale-01",
                "as_of": "2026-08-02T12:00:00Z",
                "workflow": "batch_evidence",
                "batch_id": "NCB204-B24071",
                "authorization": {
                    "user": "contractor_77",
                    "purpose": "batch_review_readiness",
                    "object_id": "NCB204-B24071",
                    "role": "supplier_quality_viewer",
                },
            }
        )
        self.assertEqual(out["error"]["code"], "AEGIS-401")
        self.assertFalse(out["error"]["retryable"])


try:
    from src.orchestrator.langgraph_agent import langgraph_available, run_langgraph
except Exception:
    langgraph_available = None  # type: ignore
    run_langgraph = None  # type: ignore


@unittest.skipUnless(
    callable(langgraph_available) and langgraph_available() and build_batch_pack is not None,
    "langgraph not installed",
)
class LangGraphOrchestratorTests(unittest.TestCase):
    def test_langgraph_runs_allowlisted_tools_without_mutating_pack(self) -> None:
        pack = build_batch_pack(
            {
                "request_id": "REQ-LG-1",
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
        before = json.dumps(pack, sort_keys=True)
        tracker = BudgetTracker()
        request = {
            "request_id": "REQ-LG-1",
            "workflow": "batch_evidence",
            "batch_id": "NCB204-B24071",
            "as_of": "2026-08-01T08:00:00Z",
            "kill_switch": True,
            "authorization": {
                "user": "qp_eu_1",
                "purpose": "batch_review_readiness",
                "object_id": "NCB204-B24071",
                "role": "qualified_person",
            },
        }
        out = run_langgraph(request, pack, tracker)
        self.assertEqual(out["framework"], "langgraph")
        self.assertFalse(out["inference_used"])
        self.assertTrue(any(item.startswith("find_conflicts:") for item in out["tool_trace"]))
        self.assertTrue(any(item.startswith("request_human_review:") for item in out["tool_trace"]))
        self.assertEqual(json.dumps(pack, sort_keys=True), before)
        self.assertNotIn("disposition", json.dumps(out["tool_trace"]).lower())
