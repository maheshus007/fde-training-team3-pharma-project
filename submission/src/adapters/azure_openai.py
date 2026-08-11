"""Shim — canonical lazy Azure adapter. Import must not load openai."""
from src._canon import load_canon

_mod = load_canon(
    "aegis_sdd_azure_openai",
    "aegis-sdd/services/integration/azure_openai.py",
)
AzureOpenAIInference = _mod.AzureOpenAIInference
