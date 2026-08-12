# AEGIS-PHARMA — Spec-Driven Agentic Specs

Version-controlled specifications for the assist-only agentic layer.

**Prerequisite track:** complete [`../modular-specs/`](../modular-specs/) (modular monolith) before implementing tasks here.

## Layout (one question per file)

| Path | Question |
|---|---|
| [`plan/`](plan/) | Validated plan + validation report |
| [`product/prd.md`](product/prd.md) | What problem are we solving? |
| [`features/`](features/) | What should each capability do? |
| [`technical/`](technical/) | Exactly how must it behave? |
| [`architecture/`](architecture/) | Where does the code belong? |
| [`prompts/`](prompts/) | Versioned assist prompts (source) |
| [`tasks/`](tasks/) | What code needs writing, one unit at a time? |

## Order of use

1. Read [`plan/VALIDATION.md`](plan/VALIDATION.md) then [`plan/AGENTIC_PLAN.md`](plan/AGENTIC_PLAN.md).
2. Implement tasks in numeric order under [`tasks/`](tasks/).
3. Hand an agent **only** the task file plus the 1–2 specs it cites.

## Rules

- Work only under `submission/`.
- Challenge evidence outside `submission/` is immutable.
- Default runtime remains AI-disabled / deterministic.
- Agents may annotate; they must never perform regulated side effects.
