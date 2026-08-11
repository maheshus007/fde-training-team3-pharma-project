"""Shim — canonical: aegis-sdd/services/integration/ports/graph.py."""
from src._canon import load_canon

_mod = load_canon(
    "aegis_sdd_port_graph",
    "aegis-sdd/services/integration/ports/graph.py",
)
GraphPort = _mod.GraphPort
FORBIDDEN_EDGE_LABELS = _mod.FORBIDDEN_EDGE_LABELS
ALLOWED_CQ_IDS = _mod.ALLOWED_CQ_IDS
ForbiddenEdgeError = _mod.ForbiddenEdgeError
