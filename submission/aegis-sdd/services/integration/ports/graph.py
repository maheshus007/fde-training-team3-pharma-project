"""GraphPort protocol (T-003). No Gremlin SDK."""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

FORBIDDEN_EDGE_LABELS = frozenset(
    {
        "RESERVED_FOR",
        "ALLOCATED_TO",
        "SHIPPED_AS",
        "DISPOSITION_SET",
        "QUALITY_STATUS_CHANGED",
        "SIGNAL_CONFIRMED",
        "CASE_MERGED",
        "ELIGIBILITY_DETERMINED",
    }
)

ALLOWED_CQ_IDS = frozenset({f"CQ-{i}" for i in range(1, 10)})


class ForbiddenEdgeError(ValueError):
    """Raised on forbidden Gremlin addE labels → AEGIS-422 at the façade."""


@runtime_checkable
class GraphPort(Protocol):
    def ingest_from_fixtures(self) -> int:
        """Return edge count. T-003 empty graph returns 0."""
        ...

    def query(self, cq_id: str, params: dict[str, Any], purpose: str, as_of: str) -> dict[str, Any]:
        ...

    def add_edge(self, label: str, from_id: str, to_id: str, properties: dict[str, Any] | None = None) -> None:
        ...
