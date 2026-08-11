"""Scoring shim — canonical module: `aegis-sdd/services/api/service.py`."""
from src._canon import load_canon

_mod = load_canon("aegis_sdd_api_service", "aegis-sdd/services/api/service.py")
health = _mod.health
make_error = _mod.make_error
submit_workflow = _mod.submit_workflow
ack_human_review = _mod.ack_human_review
query_graph = _mod.query_graph
ingest_graph = _mod.ingest_graph
