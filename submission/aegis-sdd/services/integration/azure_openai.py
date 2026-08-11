"""Cloud InferencePort (T-014). Must not import openai at module load. Never SoT."""
from __future__ import annotations

import importlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

_INTEGRATION = Path(__file__).resolve().parent
_DOMAIN = _INTEGRATION.parents[1] / "packages" / "domain"
for path in (_INTEGRATION, _DOMAIN):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from inference_stub import InferenceStub  # noqa: E402
from policy_guard import (  # noqa: E402
    BATCH_PROHIBITED,
    PV_PROHIBITED,
    SUPPLY_PROHIBITED,
    check_model_artifact,
)

_ALLOWED_KINDS = frozenset({"cluster_hint", "option_rank_hint", "narrative_summary", "conflict_notes"})
_REQUIRED_ENV = ("AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_DEPLOYMENT")
_BANNED = BATCH_PROHIBITED | PV_PROHIBITED | SUPPLY_PROHIBITED
TEMPERATURE = 0
MAX_TOKENS = 2048
TIMEOUT_S = 15
API_VERSION_DEFAULT = "2024-10-21"


def _stub(kind: str, payload: dict[str, Any], budget: dict[str, Any] | None) -> dict[str, Any]:
    return InferenceStub().suggest(kind, payload, budget)


def _kill_switch(budget: dict[str, Any]) -> bool:
    if budget.get("kill_switch") is True:
        return True
    flag = str(os.environ.get("AEGIS_KILL_SWITCH", "")).strip().lower()
    return flag in {"1", "true", "yes", "on"}


def _missing_keys() -> bool:
    return any(not str(os.environ.get(name) or "").strip() for name in _REQUIRED_ENV)


def _hash_mismatch(budget: dict[str, Any]) -> bool:
    pinned = str(os.environ.get("AZURE_OPENAI_MODEL_HASH") or "").strip()
    if not pinned:
        return False
    observed = str(budget.get("artifact_hash") or os.environ.get("AZURE_OPENAI_ARTIFACT_HASH") or "").strip()
    return not check_model_artifact(pinned, observed).allow


def _live_allowed() -> bool:
    flag = str(os.environ.get("AEGIS_ALLOW_LIVE_INFERENCE") or "").strip().lower()
    return flag in {"1", "true", "yes", "on"}


def _banned(value: Any) -> bool:
    if isinstance(value, dict):
        if set(value) & _BANNED:
            return True
        return any(_banned(item) for item in value.values())
    if isinstance(value, list):
        return any(_banned(item) for item in value)
    return False


def _parse_content(raw: Any) -> Any | None:
    if raw is None:
        return None
    if hasattr(raw, "choices"):
        choices = raw.choices or []
        if not choices:
            return None
        message = getattr(choices[0], "message", None)
        raw = getattr(message, "content", None) if message is not None else None
    if not isinstance(raw, str) or not raw.strip():
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def _status_code(exc: BaseException) -> int | None:
    for attr in ("status_code", "status"):
        value = getattr(exc, attr, None)
        if isinstance(value, int):
            return value
    response = getattr(exc, "response", None)
    code = getattr(response, "status_code", None) if response is not None else None
    return code if isinstance(code, int) else None


class AzureOpenAIInference:
    def __init__(self, client: Any | None = None, *, sleeper: Any | None = None) -> None:
        self._client = client
        self._sleeper = sleeper or time.sleep

    def _lazy_sdk_client(self) -> Any | None:
        if not _live_allowed() or _missing_keys():
            return None
        try:
            openai = importlib.import_module("openai")
        except ImportError:
            return None
        azure_cls = getattr(openai, "AzureOpenAI", None)
        if azure_cls is None:
            return None
        return azure_cls(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION") or API_VERSION_DEFAULT,
            timeout=TIMEOUT_S,
            max_retries=0,
        )

    def _complete(self, client: Any, *, kind: str, payload: dict[str, Any], max_tokens: int) -> Any:
        system = f"Return JSON only. kind={kind}. Not source of truth."
        limit = 4000
        if kind == "conflict_notes":
            system = (
                "Return JSON only: {\"notes\":[{\"id\":\"conflict-id\",\"note\":\"...\"}]}. "
                "Advisory notes for a human reviewer. Use only provided verbatim facts. "
                "Do not invent values, units, identities, or missing evidence. "
                "Do not recommend release, reject, allocate, reserve, ship, or reportability."
            )
            limit = 8000
        kwargs = {
            "model": os.environ.get("AZURE_OPENAI_DEPLOYMENT") or "deployment",
            "temperature": TEMPERATURE,
            "max_tokens": max_tokens,
            "timeout": TIMEOUT_S,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=True, default=str)[:limit]},
            ],
        }
        if hasattr(client, "complete"):
            return client.complete(**kwargs)
        return client.chat.completions.create(**kwargs)

    def suggest(self, kind: str, payload: dict[str, Any], budget: dict[str, Any] | None = None) -> dict[str, Any]:
        budget = budget or {}
        if kind not in _ALLOWED_KINDS or _kill_switch(budget) or _hash_mismatch(budget) or _missing_keys():
            return _stub(kind, payload, budget)
        client = self._client if self._client is not None else self._lazy_sdk_client()
        if client is None:
            return _stub(kind, payload, budget)
        max_tokens = int(budget.get("max_tokens") or MAX_TOKENS)
        last_error: BaseException | None = None
        for attempt in range(2):
            try:
                raw = self._complete(client, kind=kind, payload=payload, max_tokens=max_tokens)
                parsed = _parse_content(raw)
                if parsed is None or _banned(parsed):
                    return {"used": False, "suggestions": []}
                return {"used": True, "suggestions": [parsed] if not isinstance(parsed, list) else parsed}
            except Exception as exc:  # noqa: BLE001 — Azure SDK errors are opaque
                last_error = exc
                code = _status_code(exc)
                if attempt == 0 and code in {408, 429}:
                    self._sleeper(1)
                    continue
                break
        del last_error
        return _stub(kind, payload, budget)
