"""Shim — canonical: aegis-sdd/packages/domain/replay_store.py."""
from src._canon import load_canon

_mod = load_canon(
    "aegis_sdd_domain_replay_store",
    "aegis-sdd/packages/domain/replay_store.py",
)
ReplayStore = _mod.ReplayStore
TTL_SECONDS = _mod.TTL_SECONDS
composite_key = _mod.composite_key
payload_hash = _mod.payload_hash
request_hash = _mod.request_hash
