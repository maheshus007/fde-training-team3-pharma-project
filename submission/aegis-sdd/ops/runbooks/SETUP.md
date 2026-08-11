# SETUP — AEGIS-PHARMA assessment

Canonical copy of `submission/runbooks/SETUP.md` (scoring surface).

Bring up the advisory POC on a clean machine with no Azure OpenAI or Cosmos keys. Challenge `data/` and `evaluation/contracts/` stay immutable.

Commands from repository root: `python submission/scripts/setup.py`, `python submission/scripts/test.py`, `python submission/scripts/run.py`. Optional HITL: `python submission/app/main.py` binds 127.0.0.1 only.

Default `AEGIS_RUNTIME_MODE=assessment`. Never commit secrets.
