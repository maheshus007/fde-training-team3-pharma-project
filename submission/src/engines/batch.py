"""Shim — canonical: aegis-sdd/packages/domain/batch_engine.py."""
from src._canon import load_canon

_mod = load_canon(
    "aegis_sdd_domain_batch_engine",
    "aegis-sdd/packages/domain/batch_engine.py",
)
build_batch_pack = _mod.build_batch_pack
