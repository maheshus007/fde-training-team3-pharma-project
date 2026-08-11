"""Shim — canonical: aegis-sdd/services/integration/graph_memory.py."""
from src._canon import load_canon

_mod = load_canon(
    "aegis_sdd_graph_memory",
    "aegis-sdd/services/integration/graph_memory.py",
)
MemoryGraph = _mod.MemoryGraph
SUPPORTS_CQ = _mod.SUPPORTS_CQ
SUPPORTS_CQ3 = getattr(_mod, "SUPPORTS_CQ3", False)
SUPPORTS_INGEST = _mod.SUPPORTS_INGEST
