"""Advisory API façade (T-002 health; T-013 submit/ack/query/ingest).

Canonical product module. Scoring shim: `submission/src/service.py`.
Do not import Azure or Gremlin SDKs here. Taipy binds only to this module.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

_API = Path(__file__).resolve().parent
_AEGIS = _API.parents[1]
_SUBMISSION = _AEGIS.parent
_DOMAIN = _AEGIS / "packages" / "domain"
_INTEGRATION = _AEGIS / "services" / "integration"
_WORKER = _AEGIS / "services" / "worker"
_SRC = _SUBMISSION / "src"

for path in (_DOMAIN, _INTEGRATION, _WORKER, _SRC, _SUBMISSION):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from agent_runtime import BudgetTracker  # noqa: E402
from batch_engine import build_batch_pack  # noqa: E402
from conflict_priority import merge_advisory_notes, prioritize_conflicts  # noqa: E402
from entitlements import ALLOWED_PURPOSES, EntitlementStore  # noqa: E402
from cosmos_gremlin import GraphUnavailableError, select_graph  # noqa: E402
from langgraph_orchestrator import run_langgraph  # noqa: E402
from policy_guard import check_workflow_payload  # noqa: E402
from ports.graph import ALLOWED_CQ_IDS, ForbiddenEdgeError  # noqa: E402
from pv_engine import build_pv_pack  # noqa: E402
from replay_store import ReplayStore  # noqa: E402
from supply_engine import build_supply_pack  # noqa: E402
from tool_catalog import evaluate_manifest  # noqa: E402

from contracts import validate_workflow_response  # noqa: E402

_ERROR_KEYS = frozenset({"code", "message", "request_id", "retryable"})
_RETRYABLE_CODES = frozenset({"AEGIS-504"})
_KNOWN_CODES = frozenset(
    {
        "AEGIS-400",
        "AEGIS-401",
        "AEGIS-404",
        "AEGIS-409",
        "AEGIS-412",
        "AEGIS-422",
        "AEGIS-504",
    }
)
_REQUEST_KEYS = frozenset(
    {
        "request_id",
        "idempotency_key",
        "workflow",
        "as_of",
        "authorization",
        "batch_id",
        "case_ids",
        "event_id",
        "kill_switch",
        "resume_checkpoint_id",
    }
)
_AUTH_KEYS = frozenset({"user", "purpose", "object_id", "role"})
_WORKFLOWS = {
    "batch_evidence": build_batch_pack,
    "pv_intake": build_pv_pack,
    "supply_options": build_supply_pack,
}
def _graph():
    return select_graph()


def _runtime_mode() -> str:
    mode = str(os.environ.get("AEGIS_RUNTIME_MODE", "assessment")).strip().lower()
    if mode not in {"assessment", "ai_disabled", "cloud"}:
        return "assessment"
    return mode


def _evidence_root() -> Path:
    override = str(os.environ.get("AEGIS_EVIDENCE_ROOT") or "").strip()
    if override:
        return Path(override)
    return _SUBMISSION / "evidence"


def _store() -> ReplayStore:
    return ReplayStore(_evidence_root())


def health() -> dict[str, str]:
    """AA-NFR-12: status/mode/inference/graph. No Azure import."""
    mode = _runtime_mode()
    if mode == "cloud":
        inference = "azure_openai"
        graph = "cosmos_gremlin"
    elif mode == "ai_disabled":
        inference = "off"
        graph = "memory"
    else:
        inference = "stub"
        graph = "memory"
    return {
        "status": "ok",
        "mode": mode,
        "inference": inference,
        "graph": graph,
    }


def make_error(code: str, message: str, request_id: str, *, retryable: bool | None = None) -> dict[str, Any]:
    """ErrorEnvelope: additionalProperties false on `error`."""
    clean_code = str(code)
    if clean_code not in _KNOWN_CODES:
        clean_code = "AEGIS-400"
    if retryable is None:
        retryable = clean_code in _RETRYABLE_CODES
    text = str(message).replace("\n", " ").strip()
    envelope = {
        "error": {
            "code": clean_code,
            "message": text,
            "request_id": str(request_id),
            "retryable": bool(retryable),
        }
    }
    extra = set(envelope["error"]) - _ERROR_KEYS
    if extra:
        raise RuntimeError("error envelope extra keys")
    return envelope


def _validate_request(request: dict[str, Any]) -> dict[str, Any] | None:
    request_id = str(request.get("request_id") or "missing")
    extra = set(request) - _REQUEST_KEYS
    if extra:
        return make_error("AEGIS-400", "request additionalProperties denied", request_id)
    if not str(request.get("request_id") or "").strip():
        return make_error("AEGIS-400", "request_id required", request_id)
    key = str(request.get("idempotency_key") or "")
    if len(key) < 8:
        return make_error("AEGIS-400", "idempotency_key minLength 8", request_id)
    workflow = str(request.get("workflow") or "")
    if workflow not in _WORKFLOWS:
        return make_error("AEGIS-400", "unknown workflow", request_id)
    if not str(request.get("as_of") or "").strip():
        return make_error("AEGIS-400", "as_of required", request_id)
    auth = request.get("authorization")
    if not isinstance(auth, dict):
        return make_error("AEGIS-400", "authorization required", request_id)
    if set(auth) - _AUTH_KEYS:
        return make_error("AEGIS-400", "authorization additionalProperties denied", request_id)
    for field in ("user", "purpose", "object_id", "role"):
        if not str(auth.get(field) or "").strip():
            return make_error("AEGIS-400", f"authorization.{field} required", request_id)
    if workflow == "batch_evidence" and not str(request.get("batch_id") or "").strip():
        return make_error("AEGIS-400", "batch_id required", request_id)
    if workflow == "pv_intake":
        cases = request.get("case_ids")
        if not isinstance(cases, list) or not cases:
            return make_error("AEGIS-400", "case_ids minItems 1", request_id)
    if workflow == "supply_options" and not str(request.get("event_id") or "").strip():
        return make_error("AEGIS-400", "event_id required", request_id)
    return None


def _guard_pack(workflow: str, pack: dict[str, Any], request_id: str) -> dict[str, Any]:
    if "error" in pack:
        return pack
    errors = validate_workflow_response(pack)
    if errors:
        return make_error("AEGIS-422", "; ".join(errors[:5]), request_id)
    guarded = check_workflow_payload(workflow, pack)
    if not guarded.allow:
        return make_error("AEGIS-422", guarded.reason, request_id)
    return pack


def submit_workflow(request: dict[str, Any]) -> dict[str, Any]:
    invalid = _validate_request(request)
    if invalid:
        return invalid
    request_id = str(request["request_id"])
    workflow = str(request["workflow"])
    auth = request["authorization"]
    store = _store()

    authz = EntitlementStore().authorize(
        user=str(auth["user"]),
        purpose=str(auth["purpose"]),
        object_id=str(auth["object_id"]),
        role=str(auth["role"]),
        workflow=workflow,
        as_of=str(request["as_of"]),
        request_id=request_id,
    )
    if not authz.allow:
        return authz.error or make_error("AEGIS-401", authz.reason, request_id)

    manifest_path = _SUBMISSION / "tests" / "fixtures" / "tool_manifest_approved.json"
    if manifest_path.is_file():
        trusted = evaluate_manifest(json.loads(manifest_path.read_text(encoding="utf-8")))
        if not trusted["allow"]:
            return trusted["error"] or make_error("AEGIS-401", "tool manifest denied", request_id)

    if request.get("resume_checkpoint_id"):
        resumed = store.resume(request)
        return _guard_pack(workflow, resumed, request_id)

    claimed = store.claim(request)
    if claimed is not None:
        return _guard_pack(workflow, claimed, request_id)

    pack = _WORKFLOWS[workflow](request)
    if "error" in pack:
        return pack

    pack = prioritize_conflicts(pack)
    tracker = BudgetTracker()
    tracker.record_step()
    agent = run_langgraph(request, pack, tracker)
    pack = merge_advisory_notes(
        pack,
        agent.get("suggestions"),
        used=bool(agent.get("inference_used")),
    )
    pack = _guard_pack(workflow, pack, request_id)
    if "error" in pack:
        return pack

    term = "budget" if agent.get("termination") == "budget" else "completed"
    if agent.get("termination") == "budget":
        from agent_runtime import attach_budget_abstention

        pack = attach_budget_abstention(pack, tracker)
        pack = _guard_pack(workflow, pack, request_id)
        if "error" in pack:
            return pack
    store.save_checkpoint(request_id, request, pack, step=tracker.steps, termination_reason=term)
    store.remember(request, pack)
    store.save_run(request_id, pack)
    event_id = str((pack.get("audit") or {}).get("event_id") or f"AUD-{request_id}")
    store.write_audit(
        event_id,
        {
            "request_id": request_id,
            "inference_used": bool(agent.get("inference_used")),
            "orchestrator": str(agent.get("framework") or "rules"),
            "tool_trace": list(agent.get("tool_trace") or []),
            "replay": False,
        },
    )
    return pack


def ack_human_review(payload: dict[str, Any]) -> dict[str, Any]:
    request_id = str(payload.get("request_id") or "")
    if not request_id:
        return make_error("AEGIS-400", "request_id required", "missing")
    if payload.get("ack") is not True:
        return make_error("AEGIS-400", "ack must be true", request_id)
    pack = _store().load_run(request_id)
    if pack is None:
        return make_error("AEGIS-404", "unknown request_id", request_id)
    conflict_ids = {str(item.get("id")) for item in (pack.get("contradictions") or []) if item.get("id")}
    viewed = {str(item) for item in (payload.get("viewed_conflict_ids") or [])}
    if conflict_ids and not conflict_ids.issubset(viewed):
        return make_error("AEGIS-412", "viewed_conflict_ids incomplete", request_id)
    ack_body = {"request_id": request_id, "human_review": {"acknowledged": True}}
    store = _store()
    event_id = str((pack.get("audit") or {}).get("event_id") or f"AUD-{request_id}")
    store.write_audit(event_id, {"request_id": request_id, "human_review_acknowledged": True})
    return ack_body


def query_graph(payload: dict[str, Any]) -> dict[str, Any]:
    request_id = str(payload.get("request_id") or "graph-cq")
    purpose = str(payload.get("purpose") or "")
    if purpose not in ALLOWED_PURPOSES:
        return make_error("AEGIS-401", "purpose mismatch", request_id)
    cq_id = str(payload.get("cq_id") or "")
    if cq_id not in ALLOWED_CQ_IDS:
        return make_error("AEGIS-404", f"unknown CQ {cq_id}", request_id)
    as_of = str(payload.get("as_of") or "2026-08-01T08:00:00Z")
    params = payload.get("params") if isinstance(payload.get("params"), dict) else {}
    try:
        result = _graph().query(cq_id, params, purpose, as_of)
    except GraphUnavailableError as exc:
        return make_error("AEGIS-504", str(exc), request_id, retryable=True)
    provenance: list[Any] = []
    for path in result.get("paths") or []:
        provenance.extend(path.get("provenance") or [])
    result["provenance"] = provenance
    return result


def ingest_graph() -> dict[str, Any]:
    try:
        count = _graph().ingest_from_fixtures()
    except GraphUnavailableError as exc:
        return make_error("AEGIS-504", str(exc), "ingest", retryable=True)
    except ForbiddenEdgeError as exc:
        return make_error("AEGIS-422", str(exc), "ingest")
    except ValueError as exc:
        return make_error("AEGIS-422", str(exc), "ingest")
    return {"edge_count": int(count)}
