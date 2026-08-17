# Phase 0–4 Exit Evidence Pack

| Field | Entry |
|---|---|
| Team | Team 3 |
| Date | 2026-08-10 |
| Recommendation | Conditional-go to Phase 5 POC build |

## Exit checklist

| Phase | Exit evidence | Status |
|---|---|---|
| 0 Preflight | `PREFLIGHT_REPORT.md`, charter, working agreements | Complete |
| 1 Discovery/DMAIC | Artefacts 01–04; assumptions/decision log | Complete |
| 2 Domain/evidence | Artefacts 05–09; `EVIDENCE_MAP.md` | Complete |
| 3 Architecture/controls | Artefacts 10–15; contract tests | Complete |
| 4 Secure AI design | Artefacts 16–21; prohibited-action/authz/tool tests | Complete |

## Commands

```text
python tools/check_submission_structure.py --scaffold
python tools/test_contracts.py
python submission/scripts/test.py
```

## Verification (2026-08-10)

| Check | Result |
|---|---|
| `python submission/scripts/test.py` | 35 passed, 0 failed (`submission/evidence/test_results.json`) |
| Phase 4 decisions | A-401..A-406 / D-401..D-405 in assumptions log |
| `policy_guard.py` vs `contracts.py` | Separate modules; deny-by-default enforcement intact |

## Known package limitation

`python run_capstone.py --check` fails on AppleDouble `prompts/._*.md` UTF-8 decode; challenge tools left unmodified (D-006).

## Later verification (2026-08-16)

Phase 0–4 counts above are historical. Current machine evidence (do not back-date the Phase 4 exit):

| Check | Result |
|---|---|
| `python submission/scripts/test.py` | Per-test `test_results.json` (see that file for live count) |
| Inject register | `INJECT_CONTROL_REGISTER.md` — INJ-001..084 |
| A/B/C citation pack | `audit_export.json` |
| Evaluation harness | Re-run `python submission/scripts/evaluate.py` → `evaluation_results.json` |
