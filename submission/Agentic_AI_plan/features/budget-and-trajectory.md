# Feature — Budgets and Trajectory Bounds

**Question this file answers:** What limits apply to an agent run?

| Field | Entry |
|---|---|
| Feature ID | F6 |
| Version / date | 1.0 / 2026-08-12 |
| Injects | INJ-080; FinOps budgets |

## Actor

Agent loop + FinOps/security gates.

## Preconditions

- Agent mode assist requested and kill switch open.
- Budgets configured for steps, tokens, wall-clock (POC constants below).

## Hard limits (values, not adjectives)

| Limit | Value |
|---|---|
| Max trajectory steps | **25** |
| Max tool calls per run | **25** (same bound) |
| Default token budget (POC) | **4000** requested tokens max per `check_token_budget` stance |
| `side_effect` on any step | **false** only |
| Prohibited action tokens in step action | reserve, allocate, ship, disposition, release |

## Happy path

1. Start trajectory empty.
2. Each tool/model step appends `{step, tool_id, action, side_effect:false, decision}`.
3. Stop before exceeding 25 steps.
4. On success, attach annotations with `authoritative: false`.

## Exceptions

| Case | Behaviour |
|---|---|
| Step would exceed 25 | Stop; discard incomplete inference; return deterministic `core` + abstention |
| Token budget denied | Same as above |
| Step attempts prohibited action | Deny step; fail closed for that tool; do not mutate `core` facts |

## Acceptance criteria

- [ ] Trajectory length > 25 fails grader/tests
- [ ] Budget stop never leaves partial AI text as sole readiness signal
- [ ] `human_review.role` present on advisory trajectories
