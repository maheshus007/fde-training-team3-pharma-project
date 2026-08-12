# AEGIS-PHARMA — Spec-Driven Modular Monolith Specs

Version-controlled specifications for restructuring the submission into a **modular monolith**.

Related (later track): assist-only agent specs live in [`../specs/`](../specs/). Complete **this** track before implementing `aegis.agents`.

## Layout (one question per file)

| Path | Question |
|---|---|
| [`plan/`](plan/) | Validated plan + validation report |
| [`product/prd.md`](product/prd.md) | What problem does modularization solve? |
| [`features/`](features/) | What should each modular capability do? |
| [`technical/`](technical/) | Exactly how must packages and imports behave? |
| [`architecture/`](architecture/) | Where does the code belong? |
| [`tasks/`](tasks/) | What code needs writing, one unit at a time? |

## Order of use

1. Read [`plan/VALIDATION.md`](plan/VALIDATION.md) then [`plan/MODULAR_PLAN.md`](plan/MODULAR_PLAN.md).
2. Implement [`tasks/`](tasks/) in numeric order.
3. Hand an agent only the task file plus the 1–2 specs it cites.

## Rules

- Work only under `submission/`.
- One deployable process — not microservices.
- No backward-compat shims for old flat imports.
- Do not create `aegis.agents` in this track (deferred to [`../specs/`](../specs/)).
