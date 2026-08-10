"""Deny-by-default policy enforcement for prohibited regulated actions.

Separate from workflow JSON contracts (`contracts.py`). Enforces INJ-006
boundaries, INJ-066 tool trust, INJ-067 authorization freshness and
INJ-070 model hash pinning.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping, Optional


BATCH_PROHIBITED = {
    "disposition",
    "release_decision",
    "reject_decision",
    "reprocess",
    "relabel",
    "recall",
    "batch_disposition",
    "release",
    "reject",
}
PV_PROHIBITED = {
    "final_seriousness",
    "final_causality",
    "final_expectedness",
    "final_reportability",
    "signal_confirmation",
    "causality",
    "seriousness_decision",
    "reportability_decision",
}
SUPPLY_PROHIBITED = {
    "reserve",
    "allocate",
    "shipment_execute",
    "ship",
    "quality_status_change",
    "recall_initiate",
    "recall",
}

WRITE_LIKE_PERMISSIONS = {
    "write",
    "update",
    "disposition",
    "release",
    "allocate",
    "ship",
    "recall",
    "batch:disposition:write",
    "batch:write",
}


@dataclass(frozen=True)
class Decision:
    allow: bool
    reason: str


def _parse_utc(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _contains_prohibited(payload: dict[str, Any], banned: set[str]) -> list[str]:
    hits: list[str] = []
    for key in payload:
        if key in banned:
            hits.append(key)
    for nest in ("action", "actions", "decision", "execution", "side_effects"):
        obj = payload.get(nest)
        if isinstance(obj, dict):
            for key in obj:
                if key in banned:
                    hits.append(f"{nest}.{key}")
            for key, val in obj.items():
                if key in {"type", "name", "action"} and isinstance(val, str) and val in banned:
                    hits.append(f"{nest}.{key}={val}")
        if isinstance(obj, list):
            for i, item in enumerate(obj):
                if isinstance(item, str) and item in banned:
                    hits.append(f"{nest}[{i}]={item}")
                if isinstance(item, dict):
                    hits.extend(f"{nest}[{i}].{h}" for h in _contains_prohibited(item, banned))
    return hits


def check_workflow_payload(workflow: str, payload: dict[str, Any]) -> Decision:
    """Reject payloads that attempt prohibited batch/PV/supply side effects."""
    if workflow == "batch_evidence":
        hits = _contains_prohibited(payload, BATCH_PROHIBITED)
        if payload.get("execution_status") not in (None, "not_executed") and "execution_status" in payload:
            if payload.get("execution_status") != "not_executed":
                hits.append("execution_status")
    elif workflow == "pv_intake":
        hits = _contains_prohibited(payload, PV_PROHIBITED)
    elif workflow == "supply_planning":
        hits = _contains_prohibited(payload, SUPPLY_PROHIBITED)
        if payload.get("no_side_effects") is False:
            hits.append("no_side_effects=false")
    else:
        return Decision(False, f"unknown workflow {workflow}")
    if hits:
        return Decision(False, "prohibited fields: " + ", ".join(sorted(set(hits))))
    return Decision(True, "ok")


def check_authorization(
    entitlement_active: bool,
    cache_says_allow: bool,
    cache_fresh: bool,
) -> Decision:
    """INJ-067: stale or revoked entitlements deny even if cache allows."""
    if not entitlement_active:
        return Decision(False, "entitlement revoked")
    if not cache_fresh:
        return Decision(False, "stale authorization cache")
    if not cache_says_allow:
        return Decision(False, "cache deny")
    return Decision(True, "fresh allow")


def check_authorization_records(
    entitlement: Mapping[str, Any],
    cache_record: Mapping[str, Any],
    *,
    as_of: str,
) -> Decision:
    """Derive freshness from entitlement + access-cache fixture records (INJ-067)."""
    iam_state = str(entitlement.get("iam_state", "")).strip().lower()
    entitlement_active = iam_state in {"active", "enabled", "allow"}
    as_of_dt = _parse_utc(as_of) or datetime.now(timezone.utc)
    revoked_at = _parse_utc(
        str(cache_record.get("revoked_at") or entitlement.get("revoked_at") or "") or None
    )
    cached_until = _parse_utc(str(cache_record.get("cached_until") or "") or None)
    gateway = str(
        entitlement.get("ai_gateway_state") or cache_record.get("gateway_state") or ""
    ).lower()

    cache_says_allow = "active" in gateway or bool(cache_record.get("allow", False))
    cache_fresh = True
    if not entitlement_active:
        cache_fresh = False
    if revoked_at is not None and revoked_at <= as_of_dt:
        cache_fresh = False
    if cached_until is not None and cached_until < as_of_dt:
        cache_fresh = False

    return check_authorization(entitlement_active, cache_says_allow, cache_fresh)


def check_tool_manifest(manifest: dict[str, Any], approved_hashes: set[str]) -> Decision:
    """INJ-066: deny unsigned, hash-mismatched, or write/disposition tools."""
    tool_hash = manifest.get("sha256") or manifest.get("hash")
    if not tool_hash or tool_hash not in approved_hashes:
        return Decision(False, "tool hash not approved")
    if manifest.get("signed") is not True and not manifest.get("signature"):
        return Decision(False, "tool not signed")

    perms = {str(p).lower() for p in (manifest.get("permissions") or [])}
    if perms & {p.lower() for p in WRITE_LIKE_PERMISSIONS}:
        return Decision(False, "write/disposition permissions not allowed in assessed mode")
    for perm in perms:
        if "disposition" in perm and "write" in perm:
            return Decision(False, "write/disposition permissions not allowed in assessed mode")

    if manifest.get("side_effects") is True:
        return Decision(False, "side_effects not allowed")

    post_action = str(manifest.get("postAction") or manifest.get("post_action") or "")
    if post_action and any(
        token in post_action.lower() for token in ("disposition", "release", "reject", "recall")
    ):
        return Decision(False, "postAction mutates regulated state")

    hidden = manifest.get("hidden_default")
    if isinstance(hidden, dict) and any(k in BATCH_PROHIBITED or k in SUPPLY_PROHIBITED for k in hidden):
        return Decision(False, "hidden_default attempts prohibited side effect")

    return Decision(True, "approved read tool")


def check_model_artifact(registry_hash: str, artifact_hash: str) -> Decision:
    """INJ-070: model supply-chain hash pin."""
    if not registry_hash or not artifact_hash or registry_hash != artifact_hash:
        return Decision(False, "model hash mismatch")
    return Decision(True, "hash match")
