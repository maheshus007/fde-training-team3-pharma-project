"""Kill switch + agent budgets (T-012b). Inference optional; rules remain."""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

_DOMAIN = Path(__file__).resolve().parent
_INTEGRATION = _DOMAIN.parents[1] / "services" / "integration"

for path in (_DOMAIN, _INTEGRATION):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from inference_stub import InferenceStub  # noqa: E402

MAX_STEPS = 20
MAX_TOOL_CALLS = 30
MAX_INFERENCE_CALLS = 3
MAX_TOKENS = 2048
TEMPERATURE = 0


def runtime_mode() -> str:
    mode = str(os.environ.get("AEGIS_RUNTIME_MODE", "assessment")).strip().lower()
    if mode not in {"assessment", "ai_disabled", "cloud"}:
        return "assessment"
    return mode


def env_kill_switch() -> bool:
    flag = str(os.environ.get("AEGIS_KILL_SWITCH", "")).strip().lower()
    return flag in {"1", "true", "yes", "on"}


def kill_switch_on(request: dict[str, Any] | None = None) -> bool:
    if request and request.get("kill_switch") is True:
        return True
    if env_kill_switch():
        return True
    return runtime_mode() == "ai_disabled"


def inference_budget() -> dict[str, Any]:
    return {
        "max_steps": MAX_STEPS,
        "max_tool_calls": MAX_TOOL_CALLS,
        "max_inference_calls": MAX_INFERENCE_CALLS,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
    }


class BudgetTracker:
    """Provisional POC caps (ADR-AA-009 / AA-NFR-03..07)."""

    def __init__(
        self,
        *,
        max_steps: int = MAX_STEPS,
        max_tool_calls: int = MAX_TOOL_CALLS,
        max_inference_calls: int = MAX_INFERENCE_CALLS,
        max_tokens: int = MAX_TOKENS,
    ) -> None:
        self.max_steps = max_steps
        self.max_tool_calls = max_tool_calls
        self.max_inference_calls = max_inference_calls
        self.max_tokens = max_tokens
        self.steps = 0
        self.tool_calls = 0
        self.inference_calls = 0
        self.tokens = 0
        self._exhausted: str | None = None

    def _stop(self, reason: str) -> bool:
        self._exhausted = reason
        return False

    def record_step(self) -> bool:
        if self._exhausted:
            return False
        if self.steps >= self.max_steps:
            return self._stop("max_steps")
        self.steps += 1
        return True

    def record_tool(self) -> bool:
        if self._exhausted:
            return False
        if self.tool_calls >= self.max_tool_calls:
            return self._stop("max_tool_calls")
        self.tool_calls += 1
        return True

    def record_inference(self, tokens: int = 0) -> bool:
        if self._exhausted:
            return False
        if self.inference_calls >= self.max_inference_calls:
            return self._stop("max_inference_calls")
        if tokens > self.max_tokens:
            return self._stop("max_tokens")
        self.inference_calls += 1
        self.tokens += max(0, tokens)
        return True

    @property
    def exhausted(self) -> bool:
        return self._exhausted is not None

    @property
    def exhausted_reason(self) -> str | None:
        return self._exhausted


def budget_abstention(tracker: BudgetTracker) -> dict[str, Any]:
    return {
        "code": "budget_exhausted",
        "reason": f"agent budget stop: {tracker.exhausted_reason}",
        "record_ref": None,
    }


def attach_budget_abstention(pack: dict[str, Any], tracker: BudgetTracker) -> dict[str, Any]:
    """Success pack + abstention. Never AEGIS-429 on submit/advisory path."""
    if not tracker.exhausted or "error" in pack:
        return pack
    abstentions = list(pack.get("abstentions") or [])
    if not any(item.get("code") == "budget_exhausted" for item in abstentions):
        abstentions.append(budget_abstention(tracker))
    pack["abstentions"] = abstentions
    return pack


class KillSwitchInference:
    """Wraps any InferencePort; kill switch always uses the stub (used=false)."""

    def __init__(self, inner: Any, *, kill_switch: bool) -> None:
        self._inner = inner
        self._kill = bool(kill_switch)
        self._stub = InferenceStub()

    def suggest(self, kind: str, payload: dict[str, Any], budget: dict[str, Any] | None = None) -> dict[str, Any]:
        if self._kill:
            return self._stub.suggest(kind, payload, budget)
        return self._inner.suggest(kind, payload, budget)


def select_inference(request: dict[str, Any] | None = None) -> KillSwitchInference:
    """assessment / ai_disabled / kill_switch → stub. Cloud adapter still lazy-stubs without keys."""
    kill = kill_switch_on(request)
    if kill or runtime_mode() != "cloud":
        inner: Any = InferenceStub()
    else:
        from azure_openai import AzureOpenAIInference  # lazy; no openai at import of this module

        inner = AzureOpenAIInference()
    return KillSwitchInference(inner, kill_switch=kill)


def bounded_suggest(
    port: Any,
    kind: str,
    payload: dict[str, Any],
    tracker: BudgetTracker,
    request: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if kill_switch_on(request):
        return InferenceStub().suggest(kind, payload, inference_budget())
    if not tracker.record_inference(0):
        return {"used": False, "suggestions": []}
    budget = dict(inference_budget())
    budget["kill_switch"] = False
    return port.suggest(kind, payload, budget)
