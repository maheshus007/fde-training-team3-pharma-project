# Feature — Agent Assist: Supply Options

**Question this file answers:** What should supply agent-assist do?

| Field | Entry |
|---|---|
| Feature ID | F3 |
| Workflow | `supply_options` |
| Version / date | 1.0 / 2026-08-12 |

## Actor

Supply planner; approvals via Supply Governance Board.

## Preconditions

- Entitlement for purpose `supply_options_draft`.
- Deterministic `build_supply_response` available.
- Agent only if assist mode + kill switch open.

## Allowed actions

generate draft options (in-memory advisory objects only).

## Prohibited actions

reserve, allocate, ship, quality_status_change, recall initiation.

## Happy path

1. AuthZ re-check.
2. Deterministic supply options → `core` with `no_side_effects: true`.
3. Optional agent: refine draft option text / constraint listing via read-only tools.
4. Envelope merge; human approval required before any external action (outside AEGIS).

## Exceptions

| Case | Behaviour |
|---|---|
| Tool requests reserve/allocate/ship | Deny; trajectory must not record `side_effect=true` |
| `draft_reservations` present | Fail closed (INJ-080) |
| Quality hold on lot | Surface hold; do not change quality status |
| Kill switch | Deterministic drafts only |

## Acceptance criteria

- [ ] `core.no_side_effects === true`
- [ ] No `draft_reservations` field
- [ ] Options remain `status: draft`
- [ ] `draft_supply_option` tool creates envelope/core draft objects only — never SoR writes
