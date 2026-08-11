"""Cloud GraphPort (T-015). Must not import gremlinpython at module load. CI uses memory."""
from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path
from typing import Any

_INTEGRATION = Path(__file__).resolve().parent
if str(_INTEGRATION) not in sys.path:
    sys.path.insert(0, str(_INTEGRATION))

from graph_memory import MemoryGraph  # noqa: E402
from ports.graph import FORBIDDEN_EDGE_LABELS, ForbiddenEdgeError  # noqa: E402

_REQUIRED_ENV = (
    "COSMOS_GREMLIN_ENDPOINT",
    "COSMOS_GREMLIN_KEY",
    "COSMOS_GREMLIN_DATABASE",
    "COSMOS_GREMLIN_GRAPH",
)


class GraphUnavailableError(RuntimeError):
    """Cosmos unreachable and AEGIS_GRAPH_FALLBACK is false → AEGIS-504 at façade."""


def runtime_mode() -> str:
    mode = str(os.environ.get("AEGIS_RUNTIME_MODE", "assessment")).strip().lower()
    if mode not in {"assessment", "ai_disabled", "cloud"}:
        return "assessment"
    return mode


def fallback_enabled() -> bool:
    flag = str(os.environ.get("AEGIS_GRAPH_FALLBACK", "true")).strip().lower()
    return flag not in {"0", "false", "no", "off"}


def _missing_keys() -> bool:
    return any(not str(os.environ.get(name) or "").strip() for name in _REQUIRED_ENV)


def _live_allowed() -> bool:
    flag = str(os.environ.get("AEGIS_ALLOW_LIVE_GRAPH") or "").strip().lower()
    return flag in {"1", "true", "yes", "on"}


class CosmosGremlinGraph:
    """Product GraphPort. Assessment / missing keys / errors → MemoryGraph when fallback on."""

    def __init__(self, memory: MemoryGraph | None = None) -> None:
        self._memory = memory or MemoryGraph()

    def _lazy_gremlin_client(self) -> Any | None:
        """Import SDK only when live graph is explicitly enabled. Unused in CI."""
        if not _live_allowed() or _missing_keys():
            return None
        try:
            return importlib.import_module("gremlin_python.driver.client")
        except ImportError:
            return None

    def _memory_or_raise(self) -> MemoryGraph:
        if runtime_mode() != "cloud":
            return self._memory
        if fallback_enabled():
            return self._memory
        raise GraphUnavailableError("cosmos unavailable and fallback disabled")

    def ingest_from_fixtures(self) -> int:
        return self._memory_or_raise().ingest_from_fixtures()

    def query(self, cq_id: str, params: dict[str, Any], purpose: str, as_of: str) -> dict[str, Any]:
        return self._memory_or_raise().query(cq_id, params, purpose, as_of)

    def add_edge(self, label: str, from_id: str, to_id: str, properties: dict[str, Any] | None = None) -> None:
        if label in FORBIDDEN_EDGE_LABELS:
            raise ForbiddenEdgeError(label)
        self._memory_or_raise().add_edge(label, from_id, to_id, properties)


_PORT: CosmosGremlinGraph | None = None


def select_graph() -> CosmosGremlinGraph:
    global _PORT
    if _PORT is None:
        _PORT = CosmosGremlinGraph()
    return _PORT
