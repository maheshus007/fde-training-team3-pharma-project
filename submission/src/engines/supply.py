"""Shim — canonical: aegis-sdd/packages/domain/supply_engine.py."""
from src._canon import load_canon

_mod = load_canon(
    "aegis_sdd_domain_supply_engine",
    "aegis-sdd/packages/domain/supply_engine.py",
)
build_supply_pack = _mod.build_supply_pack
