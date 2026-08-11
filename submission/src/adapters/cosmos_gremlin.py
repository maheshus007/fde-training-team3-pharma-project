"""Shim — canonical lazy Cosmos Gremlin adapter. Import must not load gremlinpython."""
from src._canon import load_canon

_mod = load_canon(
    "aegis_sdd_cosmos_gremlin",
    "aegis-sdd/services/integration/cosmos_gremlin.py",
)
CosmosGremlinGraph = _mod.CosmosGremlinGraph
GraphUnavailableError = _mod.GraphUnavailableError
select_graph = _mod.select_graph
fallback_enabled = _mod.fallback_enabled
