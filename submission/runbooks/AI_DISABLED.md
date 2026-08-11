# AI_DISABLED — continuity (INJ-082)

## Policy (challenge CSV)

`data/continuity_requirements.csv` (immutable):

| Workflow in CSV | Max AI outage | Manual runbook |
|---|---|---|
| batch_review | 14 days | required |
| pv_intake | 0 hours (manual required) | required |
| supply_planning | 14 days | required |

Product workflow enum for supply is **`supply_options`**. The CSV label `supply_planning` is not a callable API (denied as unknown).

## How to run without inference

```text
set AEGIS_RUNTIME_MODE=ai_disabled
python submission/scripts/test.py
```

Or kill switch on a single request. Engines A/B/C remain rules-only:

- AC-A5: genealogy MISSING_BRANCH / ISSUED and unit abstain still detected
- AC-B6: PV duplicates and clocks still detected; no final reportability
- AC-C4: draft options with `no_side_effects=true`; no reservation

`health()` in this mode: `inference=off`, `graph=memory`.

## Human path

QP, PV assessor/medical, and supply planner review packs in Taipy or JSON export. Acknowledgement does not release a batch, confirm a signal, or allocate stock.

## Limits

Assessment does not claim BR-01 cycle-time reduction. Live Azure/Cosmos is optional demo only and must not be required for the 14-day window.
