# Participant evaluation harness

Package `evaluation/` is immutable. This folder holds Team 3 TEVV assets.

| Path | Role |
|---|---|
| `TEVV_PLAN.md` | Suites 1–12 → datasets/graders/gates |
| `HUMAN_REVIEW_RUBRIC.md` | Calibrated human-review rubric |
| `JUDGE_CONTROLS.md` | No LLM-as-judge in POC |
| `RELEASE_GATE_POLICY.md` | Failed hard gates block release |
| `contracts/` | Participant non-executing gate schema (PUB-09..15) |
| `datasets/S01_*.json`…`S12_*.json` | Required suite datasets |
| `datasets/{golden,edge_case,adversarial,failure_recovery,subgroup,thresholds,regression,scorecard}*` | Named deliverable sets |
| `graders/` | Deterministic graders + `test_graders.py` |
| `adapters/` | PUB-* → contract mapping |

```powershell
python submission/scripts/setup.py
python submission/scripts/test.py
python submission/scripts/evaluate.py
```
