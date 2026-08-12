# AI-disabled continuity runbook

| Field | Entry |
|---|---|
| Default mode | `ai_disabled_deterministic` (D-004) |
| Related | PUB-10 continuity; suite 12; JUDGE_CONTROLS |

## Purpose

Continue evidence assembly and grader validation when model providers are unavailable or disabled by policy.

## Steps

1. Do not invoke LLM judges or generative paths.
2. Run: `python submission/scripts/test.py`
3. Run: `python submission/scripts/evaluate.py`
4. Use human review packs only (`HUMAN_REVIEW_RUBRIC.md`) for qualitative acceptance.

## Expected outputs

Deterministic pass/fail from graders; public fixtures indexed with input hashes; no model-dependent scores required for POC demo gate.

## Failure handling

If contracts or graders missing → treat as unreproducible evaluation (hard gate). Escalate; do not invent answers from public fixtures.

## Reset / rollback

`python submission/scripts/reset.py`; re-evaluate offline.
