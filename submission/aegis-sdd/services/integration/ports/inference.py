"""InferencePort protocol (T-003). No Azure SDK."""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class InferencePort(Protocol):
    def suggest(self, kind: str, payload: dict[str, Any], budget: dict[str, Any] | None = None) -> dict[str, Any]:
        """Return {used: bool, suggestions: list}. Never writes SoR."""
        ...
