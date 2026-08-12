# Datasets

- **Suites:** `S01_*.json` … `S12_*.json` (package EVALUATION_PLAN suites 1–12)
- **Named sets:** `golden_set.json`, `edge_case_set.json`, `adversarial_set.json`, `failure_recovery_set.json` (failure/outage/recovery), `subgroup_analysis.json`
- **Meta:** `thresholds.json`, `regression_history.json`, `scorecard.json`, `cohort_index.csv`

Fixture bytes remain under package `evaluation/public_fixtures/`. Regenerate suites: `python submission/scripts/build_suite_datasets.py`.
