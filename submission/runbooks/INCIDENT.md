# Incident response runbook (advisory POC)

| Field | Entry |
|---|---|
| Prerequisites | Authorized reviewer; preserve evidence |
| Scope | Evaluation / UI anomalies — not batch disposition, PV final decisions, or shipment |

## Triggers

- evaluate.py exit 1 / hard-gate fail
- Suspected untrusted instruction influence (injection)
- Missing AI-disabled path

## Actions

1. Stop advisory UI if running.
2. Capture `submission/evidence/evaluation_results.json` and latest `regression_history.json` entry.
3. Fail closed: do not proceed with release claims.
4. Route to human roles per `HUMAN_REVIEW_RUBRIC.md` (QP / Safety / Supply / CISO).
5. Record assumption or defect; do not normalize or overwrite package evidence.

## Reset / rollback

Restore last known good submission commit; re-run setup → test → evaluate.
