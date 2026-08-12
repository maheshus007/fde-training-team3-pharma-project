# Judge controls

| Field | Entry |
|---|---|
| Owner | Evaluation / reliability |
| Version | 1.0 / 2026-08-12 |

## Decision

**No LLM-as-judge** is used in the assessed POC path (D-004; offline deterministic default).

| Control | Status |
|---|---|
| Primary scoring | Deterministic graders under `submission/evaluation/graders/` |
| Schema authority | Package `evaluation/contracts/*.schema.json` |
| Human judgement | `HUMAN_REVIEW_RUBRIC.md` — not automated |
| LLM judge prompts / rubrics | Not deployed |
| If LLM judge introduced later | Must be version-pinned, dual-run with deterministic graders, never sole hard-gate authority, recorded in regression_history |

## Rationale

Package EVALUATION_PLAN allows judge controls *if* an LLM judge is used. Introducing an LLM judge without dual-controls would weaken reproducibility and offline defence requirements.
