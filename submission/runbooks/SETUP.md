# SETUP — AEGIS-PHARMA assessment

## Purpose

Bring up the advisory POC on a clean machine with **no Azure OpenAI or Cosmos keys**. Challenge `data/` and `evaluation/contracts/` stay immutable.

## Prerequisites

- Python 3.10+ (team lock: 3.12)
- Repository root as working directory
- Stdlib only for assessment tests (AA-NFR-09)

## Commands

```text
python submission/scripts/setup.py
python submission/scripts/test.py
python submission/scripts/run.py
```

Optional HITL (needs Taipy locally; not required for assessment tests):

```text
python submission/app/main.py
```

Binds **127.0.0.1** only (AA-NFR-19).

## Environment

Leave cloud variables unset. Default:

- `AEGIS_RUNTIME_MODE=assessment`
- `AEGIS_GRAPH_FALLBACK=true`
- `AEGIS_KILL_SWITCH` unset or false

Copy `submission/aegis-sdd/.env.example` locally if needed. Never commit `.env` or keys (AA-NFR-16).

## Verify

`health()` must return `status=ok`, `mode=assessment`, `inference=stub`, `graph=memory`.
