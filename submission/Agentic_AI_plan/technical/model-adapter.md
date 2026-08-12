# Technical Spec — Model Adapter

**Question this file answers:** Exactly how may inference propose suggestions?

| Field | Entry |
|---|---|
| Spec ID | T3 |
| Version / date | 1.0 / 2026-08-12 |
| Implements | F5; F6; INJ-070; INJ-081; ADR-002 |

## Interface

```
propose(context: StructuredContext) -> SuggestionBundle | Abstain
```

### StructuredContext (minimum)

| Field | Rule |
|---|---|
| `workflow` | one of three workflows |
| `language` | `en` or `de` only for assessed selection |
| `core_digest` | hash or bounded summary of deterministic `core` (facts already decided) |
| `intended_use` | matches workflow purpose |

### SuggestionBundle

| Field | Rule |
|---|---|
| `annotations` | list of `{kind, text, authoritative:false}` |
| `model_id` | string (e.g. `ntg-offline-extract-v1`) |
| `artifact_hash` | must equal registry hash |

### Abstain

`{ "abstain": true, "reason": "<code or text>" }` — runtime continues with deterministic `core`.

## Preconditions (all required)

1. Kill switch open
2. `agent_mode == assist`
3. `check_model_artifact(registry_hash, artifact_hash)` allow
4. `select_model(intended_use, language)` returns a model id (not None)
5. Token budget allow

## Assessed implementation

`OfflineExtractAdapter`:

- No network I/O
- Returns fixture suggestions derived only from fields already present in `core` (no new “facts”)
- Records trajectory step `tool_id=model.propose`, `side_effect=false`

## Failure mapping

| Condition | Result |
|---|---|
| Hash mismatch | Abstain; deterministic continues |
| Unsupported language | Abstain (per current `model_gateway.select_model`) |
| Budget denied | Abstain |
| Kill switch | Adapter not called |

## Prohibitions

- Adapter must not write SoR
- Adapter must not overwrite `core.evidence` facts
- Adapter must not emit prohibited fields into `core`
