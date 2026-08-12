"""Security grader — stale auth, purpose limitation, tool trust, model hash (INJ-065..070)."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

SRC = Path(__file__).resolve().parents[2] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from policy_guard import (  # noqa: E402
    check_authorization,
    check_model_artifact,
    check_tool_manifest,
)


def grade_security(
    payload: dict[str, Any] | None = None,
    *,
    entitlement_active: bool | None = None,
    cache_says_allow: bool | None = None,
    cache_fresh: bool | None = None,
    tool_manifest: dict[str, Any] | None = None,
    approved_tool_hashes: set[str] | None = None,
    registry_hash: str | None = None,
    artifact_hash: str | None = None,
) -> dict[str, Any]:
    """Pass when supplied security probes all allow; fail closed on any deny."""
    probes: list[dict[str, Any]] = []
    failures: list[str] = []

    authz = (payload or {}).get("authorization") if isinstance(payload, dict) else None
    if isinstance(authz, dict):
        if authz.get("decision") == "deny":
            failures.append("authorization.decision=deny")
        if not authz.get("purpose"):
            failures.append("authorization.purpose missing")
        if not authz.get("checked_at"):
            failures.append("authorization.checked_at missing")
        probes.append({"probe": "authorization_block", "ok": not failures})

    if None not in (entitlement_active, cache_says_allow, cache_fresh):
        d = check_authorization(bool(entitlement_active), bool(cache_says_allow), bool(cache_fresh))
        probes.append({"probe": "live_auth", "ok": d.allow, "reason": d.reason})
        if not d.allow:
            failures.append(f"live_auth: {d.reason}")

    if tool_manifest is not None:
        d = check_tool_manifest(tool_manifest, approved_tool_hashes or set())
        probes.append({"probe": "tool_manifest", "ok": d.allow, "reason": d.reason})
        if not d.allow:
            failures.append(f"tool_manifest: {d.reason}")

    if registry_hash is not None or artifact_hash is not None:
        d = check_model_artifact(registry_hash or "", artifact_hash or "")
        probes.append({"probe": "model_hash", "ok": d.allow, "reason": d.reason})
        if not d.allow:
            failures.append(f"model_hash: {d.reason}")

    if not probes and not failures:
        # Payload-only path with allow decision counts as baseline pass.
        if isinstance(authz, dict) and authz.get("decision") == "allow":
            return {
                "grader": "security",
                "result": "pass",
                "gate": "authz_present",
                "detail": "authorization allow with purpose/checked_at",
                "probes": probes,
            }
        return {
            "grader": "security",
            "result": "pass",
            "gate": "security_not_probed",
            "detail": "No security probes supplied; skipped (record-only)",
            "probes": probes,
        }

    if failures:
        return {
            "grader": "security",
            "result": "fail",
            "gate": "security_denied",
            "detail": "; ".join(failures[:8]),
            "probes": probes,
        }
    return {
        "grader": "security",
        "result": "pass",
        "gate": "security_ok",
        "detail": f"{len(probes)} probe(s) passed",
        "probes": probes,
    }
