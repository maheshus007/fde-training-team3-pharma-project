"""Platform stubs: health, envelope, purpose-bind, inference stub (Prompt 10). T-013 façade."""
from __future__ import annotations

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


@unittest.skipUnless(service is not None and hasattr(service, "health"), "T-002 not implemented")
class PlatformHealthTests(unittest.TestCase):
    def test_aa_nfr_12_health(self) -> None:
        import time

        started = time.perf_counter()
        body = service.health()
        elapsed_ms = (time.perf_counter() - started) * 1000
        self.assertLessEqual(elapsed_ms, 200.0)
        self.assertEqual(set(body.keys()), {"status", "mode", "inference", "graph"})
        self.assertEqual(body["status"], "ok")
        self.assertEqual(body["mode"], "assessment")
        self.assertEqual(body["inference"], "stub")
        self.assertEqual(body["graph"], "memory")

    def test_error_envelope_keys_only(self) -> None:
        env = service.make_error("AEGIS-401", "stale authorization cache", "req-1")
        self.assertEqual(set(env.keys()), {"error"})
        self.assertEqual(
            set(env["error"].keys()),
            {"code", "message", "request_id", "retryable"},
        )
        self.assertEqual(env["error"]["code"], "AEGIS-401")
        self.assertFalse(env["error"]["retryable"])
        self.assertNotIn("traceback", str(env).lower())


try:
    from src.adapters.entitlements import EntitlementStore
except Exception:
    EntitlementStore = None  # type: ignore


@unittest.skipUnless(EntitlementStore is not None, "T-004 not implemented")
class PurposeBindTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = EntitlementStore()

    def test_purpose_mismatch_denied(self) -> None:
        result = self.store.authorize(
            user="qp_eu_1",
            purpose="batch_review_readiness",
            object_id="PV-1001",
            role="qualified_person",
            workflow="pv_intake",
            as_of="2026-08-02T12:00:00Z",
            request_id="req-purpose-1",
        )
        self.assertFalse(result.allow)
        self.assertEqual(result.error["error"]["code"], "AEGIS-401")
        self.assertFalse(result.error["error"]["retryable"])
        self.assertIn("purpose", result.error["error"]["message"].lower())

    def test_revoked_returns_aegis_401(self) -> None:
        result = self.store.authorize(
            user="contractor_77",
            purpose="batch_review_readiness",
            object_id="NCB204-B24071",
            role="supplier_quality_viewer",
            workflow="batch_evidence",
            as_of="2026-08-02T12:00:00Z",
            request_id="req-revoked-1",
        )
        self.assertFalse(result.allow)
        self.assertEqual(result.error["error"]["code"], "AEGIS-401")

    def test_stale_cache_returns_aegis_401(self) -> None:
        result = self.store.authorize(
            user="contractor_77",
            purpose="batch_review_readiness",
            object_id="NCB204-B24071",
            role="supplier_quality_viewer",
            workflow="batch_evidence",
            as_of="2026-08-02T12:00:00Z",
            request_id="req-stale-1",
        )
        self.assertFalse(result.allow)
        self.assertEqual(result.error["error"]["code"], "AEGIS-401")

    def test_fresh_matching_purpose_allowed(self) -> None:
        result = self.store.authorize(
            user="qp_eu_1",
            purpose="batch_review_readiness",
            object_id="NCB204-B24071",
            role="qualified_person",
            workflow="batch_evidence",
            as_of="2026-08-02T12:00:00Z",
            request_id="req-ok-1",
        )
        self.assertTrue(result.allow)
        self.assertIsNone(result.error)


class InferenceStubImportTests(unittest.TestCase):
    def test_src_import_does_not_require_openai(self) -> None:
        import src  # noqa: F401
        import src.service  # noqa: F401
        import src.adapters.azure_openai  # noqa: F401
        import src.adapters.cosmos_gremlin  # noqa: F401

        self.assertNotIn("openai", sys.modules)
        self.assertNotIn("gremlinpython", sys.modules)
        self.assertNotIn("gremlin_python", sys.modules)

    def test_azure_missing_keys_and_hash_mismatch_stub(self) -> None:
        import time

        from src.adapters.azure_openai import AzureOpenAIInference

        class _Boom:
            def complete(self, **kwargs):
                raise AssertionError("must not call Azure")

        class _JsonClient:
            def complete(self, **kwargs):
                del kwargs
                return '{"hint": "ok"}'

        class _BannedClient:
            def complete(self, **kwargs):
                del kwargs
                return '{"disposition": "release"}'

        previous = {name: os.environ.get(name) for name in (
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_DEPLOYMENT",
            "AZURE_OPENAI_MODEL_HASH",
            "AEGIS_ALLOW_LIVE_INFERENCE",
        )}
        try:
            for name in previous:
                os.environ.pop(name, None)
            started = time.perf_counter()
            missing = AzureOpenAIInference(client=_Boom()).suggest("cluster_hint", {"text": "x"}, None)
            self.assertLessEqual((time.perf_counter() - started) * 1000, 50.0)
            self.assertFalse(missing["used"])
            self.assertEqual(missing["suggestions"], [])
            self.assertNotIn("openai", sys.modules)

            os.environ["AZURE_OPENAI_ENDPOINT"] = "https://example.openai.azure.com"
            os.environ["AZURE_OPENAI_API_KEY"] = "not-a-real-key"
            os.environ["AZURE_OPENAI_DEPLOYMENT"] = "gxp-sum-1"
            os.environ["AZURE_OPENAI_MODEL_HASH"] = "sha256:222bbb"
            mismatch = AzureOpenAIInference(client=_Boom()).suggest(
                "narrative_summary",
                {"batch_id": "NCB204-B24071"},
                {"artifact_hash": "sha256:deadbeef"},
            )
            self.assertFalse(mismatch["used"])

            parsed = AzureOpenAIInference(client=_JsonClient()).suggest(
                "cluster_hint",
                {"text": "x"},
                {"artifact_hash": "sha256:222bbb"},
            )
            self.assertTrue(parsed["used"])
            self.assertEqual(parsed["suggestions"], [{"hint": "ok"}])

            banned = AzureOpenAIInference(client=_BannedClient()).suggest(
                "cluster_hint",
                {"text": "x"},
                {"artifact_hash": "sha256:222bbb"},
            )
            self.assertFalse(banned["used"])
        finally:
            for name, value in previous.items():
                if value is None:
                    os.environ.pop(name, None)
                else:
                    os.environ[name] = value
            self.assertNotIn("openai", sys.modules)

    def test_inference_stub_used_false(self) -> None:
        import time

        from src.adapters.inference_stub import InferenceStub

        started = time.perf_counter()
        result = InferenceStub().suggest("cluster_hint", {"text": "x"}, None)
        elapsed_ms = (time.perf_counter() - started) * 1000
        self.assertLessEqual(elapsed_ms, 50.0)
        self.assertFalse(result["used"])
        self.assertEqual(result["suggestions"], [])

    def test_fixture_ingest_edge_count_positive(self) -> None:
        from src.adapters.graph_memory import MemoryGraph

        self.assertGreater(MemoryGraph().ingest_from_fixtures(), 0)

    def test_forbidden_edge_rejected(self) -> None:
        from src.adapters.graph_memory import MemoryGraph

        with self.assertRaises(ValueError):
            MemoryGraph().add_edge("RESERVED_FOR", "a", "b")

    def test_cosmos_fallback_and_504(self) -> None:
        import json

        from src.adapters.cosmos_gremlin import CosmosGremlinGraph, GraphUnavailableError

        names = (
            "AEGIS_RUNTIME_MODE",
            "AEGIS_GRAPH_FALLBACK",
            "AEGIS_ALLOW_LIVE_GRAPH",
            "COSMOS_GREMLIN_ENDPOINT",
            "COSMOS_GREMLIN_KEY",
            "COSMOS_GREMLIN_DATABASE",
            "COSMOS_GREMLIN_GRAPH",
        )
        previous = {name: os.environ.get(name) for name in names}
        try:
            for name in names:
                os.environ.pop(name, None)
            os.environ["AEGIS_RUNTIME_MODE"] = "assessment"
            os.environ["AEGIS_GRAPH_FALLBACK"] = "true"
            port = CosmosGremlinGraph()
            self.assertGreater(port.ingest_from_fixtures(), 0)
            result = port.query(
                "CQ-1",
                {"batch_id": "NCB204-B24071"},
                "batch_review_readiness",
                "2026-08-01T08:00:00Z",
            )
            self.assertIn("SUA-88", json.dumps(result))
            with self.assertRaises(ValueError):
                port.add_edge("RESERVED_FOR", "a", "b")
            self.assertNotIn("gremlin_python", sys.modules)

            os.environ["AEGIS_RUNTIME_MODE"] = "cloud"
            os.environ["AEGIS_GRAPH_FALLBACK"] = "false"
            with self.assertRaises(GraphUnavailableError):
                CosmosGremlinGraph().query(
                    "CQ-1",
                    {"batch_id": "NCB204-B24071"},
                    "batch_review_readiness",
                    "2026-08-01T08:00:00Z",
                )
            denied = service.query_graph(
                {
                    "purpose": "batch_review_readiness",
                    "as_of": "2026-08-01T08:00:00Z",
                    "cq_id": "CQ-1",
                    "params": {"batch_id": "NCB204-B24071"},
                }
            )
            self.assertEqual(denied["error"]["code"], "AEGIS-504")
            self.assertTrue(denied["error"]["retryable"])
        finally:
            for name, value in previous.items():
                if value is None:
                    os.environ.pop(name, None)
                else:
                    os.environ[name] = value
            self.assertNotIn("gremlin_python", sys.modules)


@unittest.skipUnless(service is not None and hasattr(service, "submit_workflow"), "T-013 not implemented")
class ServiceFacadeTests(unittest.TestCase):
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

    def test_submit_batch_schema_valid(self) -> None:
        from src.contracts import validate_workflow_response

        pack = service.submit_workflow(
            {
                "request_id": "REQ-SVC-A",
                "idempotency_key": "idem-svc-batch-01",
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
        self.assertEqual(pack["execution_status"], "not_executed")
        ranks = [int(item["priority"]) for item in pack["contradictions"]]
        self.assertEqual(ranks, sorted(ranks))
        self.assertTrue(all(item.get("advisory_note") for item in pack["contradictions"]))
        self.assertTrue(all(item.get("note_source") == "rules" for item in pack["contradictions"]))
        event_id = pack["audit"]["event_id"]
        sidecar = Path(self._tmp.name) / "audit" / f"{event_id}.json"
        self.assertTrue(sidecar.is_file())

    def test_submit_additional_properties_denied(self) -> None:
        out = service.submit_workflow(
            {
                "request_id": "REQ-SVC-X",
                "idempotency_key": "idem-svc-extra-01",
                "as_of": "2026-08-01T08:00:00Z",
                "workflow": "batch_evidence",
                "batch_id": "NCB204-B24071",
                "runtime_mode": "cloud",
                "authorization": {
                    "user": "qp_eu_1",
                    "purpose": "batch_review_readiness",
                    "object_id": "NCB204-B24071",
                    "role": "qualified_person",
                },
            }
        )
        self.assertEqual(out["error"]["code"], "AEGIS-400")

    def test_query_and_ingest_graph(self) -> None:
        ingested = service.ingest_graph()
        self.assertGreater(ingested["edge_count"], 0)
        unknown = service.query_graph(
            {"purpose": "batch_review_readiness", "as_of": "2026-08-01T08:00:00Z", "cq_id": "CQ-99", "params": {}}
        )
        self.assertEqual(unknown["error"]["code"], "AEGIS-404")
        denied = service.query_graph(
            {"purpose": "exfiltrate", "as_of": "2026-08-01T08:00:00Z", "cq_id": "CQ-1", "params": {}}
        )
        self.assertEqual(denied["error"]["code"], "AEGIS-401")
        result = service.query_graph(
            {
                "purpose": "batch_review_readiness",
                "as_of": "2026-08-01T08:00:00Z",
                "cq_id": "CQ-1",
                "params": {"batch_id": "NCB204-B24071"},
            }
        )
        self.assertEqual(result["cq_id"], "CQ-1")
        self.assertIn("paths", result)
        self.assertIn("provenance", result)
