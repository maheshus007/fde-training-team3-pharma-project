"""Checkpoints + idempotency (T-012c). No SoR writes. Replay flags live in audit sidecars."""
from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TTL_SECONDS = 86400
_TERMINATION = frozenset({None, "budget", "kill_switch", "completed"})


def _canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _envelope(code: str, message: str, request_id: str) -> dict[str, Any]:
    return {
        "error": {
            "code": code,
            "message": message.replace("\n", " ").strip(),
            "request_id": str(request_id),
            "retryable": False,
        }
    }


def object_ids(request: dict[str, Any]) -> dict[str, Any]:
    auth = request.get("authorization") or {}
    return {
        "object_id": auth.get("object_id"),
        "batch_id": request.get("batch_id"),
        "case_ids": request.get("case_ids"),
        "event_id": request.get("event_id"),
    }


def composite_key(request: dict[str, Any]) -> str:
    auth = request.get("authorization") or {}
    return _canon(
        {
            "idempotency_key": request.get("idempotency_key"),
            "workflow": request.get("workflow"),
            "as_of": request.get("as_of"),
            "user": auth.get("user"),
            "object_ids": object_ids(request),
        }
    )


def payload_hash(request: dict[str, Any]) -> str:
    body = {key: value for key, value in request.items() if key not in {"request_id", "resume_checkpoint_id"}}
    return _sha256(_canon(body))


def request_hash(request: dict[str, Any]) -> str:
    return payload_hash(request)


def _facts_hash(pack: dict[str, Any]) -> str:
    subset = {
        "workflow": pack.get("workflow"),
        "evidence": pack.get("evidence"),
        "contradictions": pack.get("contradictions"),
        "gaps": pack.get("gaps"),
        "abstentions": pack.get("abstentions"),
    }
    return _sha256(_canon(subset))


class ReplayStore:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.checkpoints = self.root / "checkpoints"
        self.idempotency = self.root / "idempotency"
        self.audit = self.root / "audit"
        for folder in (self.checkpoints, self.idempotency, self.audit):
            folder.mkdir(parents=True, exist_ok=True)

    def write_audit(self, event_id: str, extra: dict[str, Any]) -> None:
        path = self.audit / f"{event_id}.json"
        body = {"event_id": event_id, **extra}
        path.write_text(_canon(body) + "\n", encoding="utf-8")

    def _write_audit_sidecar(self, event_id: str, extra: dict[str, Any]) -> None:
        self.write_audit(event_id, extra)

    def save_checkpoint(
        self,
        checkpoint_id: str,
        request: dict[str, Any],
        pack: dict[str, Any],
        *,
        step: int = 0,
        tool_calls_used: int = 0,
        inference_calls_used: int = 0,
        termination_reason: str | None = "completed",
    ) -> dict[str, Any]:
        if termination_reason not in _TERMINATION:
            termination_reason = "completed"
        record = {
            "checkpoint_id": checkpoint_id,
            "request_hash": request_hash(request),
            "step": int(step),
            "tool_calls_used": int(tool_calls_used),
            "inference_calls_used": int(inference_calls_used),
            "partial_facts_hash": _facts_hash(pack),
            "termination_reason": termination_reason,
            "pack": pack,
            "stored_at": _now_iso(),
        }
        path = self.checkpoints / f"{checkpoint_id}.json"
        path.write_text(_canon(record) + "\n", encoding="utf-8")
        return record

    def load_checkpoint(self, checkpoint_id: str, request_id: str) -> dict[str, Any]:
        path = self.checkpoints / f"{checkpoint_id}.json"
        if not path.is_file():
            return _envelope("AEGIS-404", f"unknown checkpoint {checkpoint_id}", request_id)
        return json.loads(path.read_text(encoding="utf-8"))

    def resume(self, request: dict[str, Any]) -> dict[str, Any]:
        checkpoint_id = str(request.get("resume_checkpoint_id") or "")
        request_id = str(request.get("request_id") or "req-resume")
        loaded = self.load_checkpoint(checkpoint_id, request_id)
        if "error" in loaded:
            return loaded
        stored_hash = loaded.get("request_hash")
        if stored_hash != request_hash(request):
            return _envelope("AEGIS-409", "checkpoint request hash mismatch", request_id)
        pack = dict(loaded.get("pack") or {})
        event_id = str((pack.get("audit") or {}).get("event_id") or f"AUD-{request_id}")
        if "audit" not in pack:
            pack["audit"] = {"event_id": event_id}
        self._write_audit_sidecar(event_id, {"resume_of": checkpoint_id, "replay": True})
        return pack

    def save_run(self, request_id: str, pack: dict[str, Any]) -> None:
        folder = self.root / "packs"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{request_id}.json").write_text(_canon(pack) + "\n", encoding="utf-8")

    def load_run(self, request_id: str) -> dict[str, Any] | None:
        path = self.root / "packs" / f"{request_id}.json"
        if not path.is_file():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def claim(self, request: dict[str, Any]) -> dict[str, Any] | None:
        """Stored pack, AEGIS-409 envelope, or None on miss/expiry."""
        request_id = str(request.get("request_id") or "req-idem")
        key = composite_key(request)
        digest = payload_hash(request)
        path = self.idempotency / (_sha256(key) + ".json")
        now = time.time()
        if not path.is_file():
            return None
        prior = json.loads(path.read_text(encoding="utf-8"))
        stored_at = float(prior.get("stored_at_unix") or 0)
        if stored_at and (now - stored_at) > TTL_SECONDS:
            path.unlink(missing_ok=True)
            return None
        if prior.get("payload_hash") != digest:
            return _envelope("AEGIS-409", "idempotency key reuse with different payload", request_id)
        replayed = dict(prior.get("pack") or {})
        event_id = str((replayed.get("audit") or {}).get("event_id") or f"AUD-{request_id}")
        self._write_audit_sidecar(event_id, {"replay": True})
        return replayed

    def remember(self, request: dict[str, Any], pack: dict[str, Any]) -> dict[str, Any]:
        request_id = str(request.get("request_id") or "req-idem")
        key = composite_key(request)
        digest = payload_hash(request)
        filename = _sha256(key) + ".json"
        path = self.idempotency / filename
        now = time.time()
        if path.is_file():
            prior = json.loads(path.read_text(encoding="utf-8"))
            stored_at = float(prior.get("stored_at_unix") or 0)
            if stored_at and (now - stored_at) > TTL_SECONDS:
                path.unlink(missing_ok=True)
            else:
                if prior.get("payload_hash") != digest:
                    return _envelope("AEGIS-409", "idempotency key reuse with different payload", request_id)
                replayed = dict(prior.get("pack") or {})
                event_id = str((replayed.get("audit") or {}).get("event_id") or f"AUD-{request_id}")
                self._write_audit_sidecar(event_id, {"replay": True})
                return replayed
        event_id = str((pack.get("audit") or {}).get("event_id") or f"AUD-{request_id}")
        record = {
            "composite_key": key,
            "payload_hash": digest,
            "stored_at_unix": now,
            "stored_at": _now_iso(),
            "pack": pack,
        }
        path.write_text(_canon(record) + "\n", encoding="utf-8")
        self._write_audit_sidecar(event_id, {"replay": False})
        return pack
