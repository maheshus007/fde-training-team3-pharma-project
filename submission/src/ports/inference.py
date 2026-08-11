"""Shim — canonical: aegis-sdd/services/integration/ports/inference.py."""
from src._canon import load_canon

_mod = load_canon(
    "aegis_sdd_port_inference",
    "aegis-sdd/services/integration/ports/inference.py",
)
InferencePort = _mod.InferencePort
