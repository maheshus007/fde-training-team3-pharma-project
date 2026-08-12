# Setup runbook

| Field | Entry |
|---|---|
| Prerequisites | Python 3.11+, repo root checkout, offline network OK |
| Inputs | Package `evaluation/`, `submission/` tree |
| Outputs | Verified prerequisites for test/evaluate |

## Steps

1. From repo root: `python submission/scripts/setup.py`
2. Expected: `PASS — evaluation setup prerequisites present`
3. Optional UI deps only if running Taipy: install per `submission/app` docs

## Failure handling

Missing package `evaluation/` or graders → restore challenge package; do not invent fixtures under package `evaluation/`.

## Reset / rollback

`python submission/scripts/reset.py` clears regenerable evaluation_results only.
