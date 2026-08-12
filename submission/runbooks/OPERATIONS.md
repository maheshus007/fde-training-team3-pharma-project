# Operations runbook

| Field | Entry |
|---|---|
| Prerequisites | Setup PASS |
| Inputs | Contract samples; public fixtures (inputs only) |
| Outputs | `submission/evidence/test_results.json`, `evaluation_results.json` |

## Daily / demo commands

```powershell
python submission/scripts/test.py
python submission/scripts/evaluate.py
python submission/scripts/hash_and_manifest.py
```

Optional advisory UI: `python submission/scripts/run.py`

## Expected outputs

- test: unittest success
- evaluate: `fail` count 0; may show `not_implemented` for uncovered public fixtures (POC)
- hashes/manifest under `submission/evidence/`

## Failure handling

Hard-gate fail → release blocked (`RELEASE_GATE_POLICY.md`). Do not waive by editing package fixtures.

## Reset / rollback

`python submission/scripts/reset.py` then re-run evaluate.
