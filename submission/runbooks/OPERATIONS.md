# OPERATIONS — daily advisory use

## Intended use

Operators submit **advisory** packs only through `src.service` (CLI scripts or Taipy). The three workflows are `batch_evidence`, `pv_intake`, and `supply_options` (not `supply_planning`).

## Happy path

1. `python submission/scripts/run.py` — health + fixture ingest.
2. Submit via service or HITL pages (batch / PV / supply / review).
3. Review evidence, contradictions, and gaps **before** acknowledgement (INJ-071).
4. Ack only after all contradiction ids are viewed; incomplete ack returns `AEGIS-412`.

## Budgets (ADR-AA-009)

Stop cleanly at 20 steps, 30 tool calls, 3 inference calls, 2048 tokens, temperature 0. Over-budget returns a schema-valid pack with abstention `budget_exhausted` (not AEGIS-429).

## Prohibited (never execute)

- Batch: release, reject, reprocess, relabel, recall
- PV: final seriousness, causality, expectedness, reportability, signal confirmation
- Supply: reserve, allocate, ship, quality-status change, recall initiation

## Reset runtime stores

```text
python submission/scripts/reset.py
```

Deletes JSON under `submission/evidence/{idempotency,checkpoints,audit,packs}` only. Does not touch challenge `data/` or `test_results.json`.

## Evaluate golden packs

```text
python submission/scripts/evaluate.py
```
