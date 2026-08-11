"""Shim — canonical: aegis-sdd/services/integration/inference_stub.py."""
from src._canon import load_canon

_mod = load_canon(
    "aegis_sdd_inference_stub",
    "aegis-sdd/services/integration/inference_stub.py",
)
InferenceStub = _mod.InferenceStub
