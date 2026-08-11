"""Scoring shim — canonical: aegis-sdd/packages/domain/ontology.py."""
from src._canon import load_canon

_mod = load_canon(
    "aegis_sdd_domain_ontology",
    "aegis-sdd/packages/domain/ontology.py",
)
evaluate_unit_mapping = _mod.evaluate_unit_mapping
evaluate_lab_comparability = _mod.evaluate_lab_comparability
resolve_product_identity = _mod.resolve_product_identity
retain_coding = _mod.retain_coding
