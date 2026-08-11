# SRS — Deployment notes (Prompt 08 §I)

## Modes

| `AEGIS_RUNTIME_MODE` | Default | Requires |
|---|---|---|
| `assessment` | **yes** | Python 3.10+; challenge `data/` + `evaluation/contracts/` |
| `cloud` | no | Azure OpenAI env + Cosmos Gremlin env + network |
| `ai_disabled` | no | same as assessment; inference adapter forced off |

## Env var names (values never committed)

```
AEGIS_RUNTIME_MODE
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_API_KEY
AZURE_OPENAI_DEPLOYMENT
AZURE_OPENAI_API_VERSION
COSMOS_GREMLIN_ENDPOINT
COSMOS_GREMLIN_KEY
COSMOS_GREMLIN_DATABASE
COSMOS_GREMLIN_GRAPH
AEGIS_KILL_SWITCH
AZURE_OPENAI_MODEL_HASH
AEGIS_GRAPH_FALLBACK
```

`AEGIS_GRAPH_FALLBACK` default `true` (Cosmos error → memory port). Set `false` to emit AEGIS-504.

## Health

`health()` JSON:

```json
{"status":"ok","mode":"assessment","inference":"stub","graph":"memory"}
```

Cloud example: `inference=azure_openai`, `graph=cosmos_gremlin` or `graph=degraded`.

## Containerization

**Out of scope** for POC (no Docker required). Runnable via `python submission/scripts/run.py` (to be added Prompt 11) and Taipy entry `python submission/app/main.py`.

## Reverse proxy

**Out of scope.** Bind Taipy/HTTP to `127.0.0.1` only if HTTP enabled.

## Dependencies

| Mode | Allowed extra packages |
|---|---|
| assessment | none beyond stdlib **or** Taipy if UI launched; tests must not import Azure |
| cloud | `openai` (Azure), `gremlinpython`, `taipy` — lock versions in Prompt 11 `requirements` file |

Assessment unittest path MUST remain stdlib-runnable (current `submission/scripts/test.py`).

## PUB-09–15

Participant extra contracts under `submission/evaluation/` are **deferred to Prompt 11/12** (Prompt 08 mapping: Stage 3 uses package `evaluation/contracts/`; PUB-09–15 extensions wait). Not a silent omit.
