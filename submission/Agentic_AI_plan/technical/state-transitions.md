# Technical Spec — Run State Transitions

**Question this file answers:** Exactly which states exist and what triggers transitions?

| Field | Entry |
|---|---|
| Spec ID | T4 |
| Version / date | 1.0 / 2026-08-12 |

## States

| State | Meaning |
|---|---|
| `RECEIVED` | Request accepted |
| `AUTHZ_CHECKED` | Entitlement re-check passed |
| `DETERMINISTIC_DONE` | Workflow `core` built |
| `AGENT_SKIPPED` | Assist not engaged |
| `AGENT_RUNNING` | Loop executing tools/model |
| `MERGED` | Envelope assembled |
| `VALIDATED` | `core` package-schema valid |
| `AUDITED` | Audit event emitted |
| `FAIL_CLOSED` | Terminal deny/abstain path |

## Transitions

```
RECEIVED
  → AUTHZ_CHECKED          [entitlement active + fresh]
  → FAIL_CLOSED            [else]

AUTHZ_CHECKED
  → DETERMINISTIC_DONE     [workflow runner succeeds]
  → FAIL_CLOSED            [workflow cannot run]

DETERMINISTIC_DONE
  → AGENT_SKIPPED          [agent_mode=disabled OR kill switch]
  → AGENT_RUNNING          [assist + kill switch open]
  → FAIL_CLOSED            [checkpoint_stale=true]

AGENT_RUNNING
  → MERGED                 [loop complete or budget stop with discard]
  → FAIL_CLOSED            [unrecoverable policy violation with no safe core publish]

AGENT_SKIPPED
  → MERGED

MERGED
  → VALIDATED              [core schema + prohibited checks pass]
  → FAIL_CLOSED            [core invalid]

VALIDATED
  → AUDITED                [always]
```

## Checkpoint rules (INJ-080)

- Checkpoint after `AUTHZ_CHECKED` and after `DETERMINISTIC_DONE`.
- If resume payload has `checkpoint_stale=true` → `FAIL_CLOSED`.
- If resume payload has `draft_reservations` → `FAIL_CLOSED`.
- Rollback of agent work = drop annotations/trajectory incomplete steps; keep last good `core`.

## Terminal outputs

| Terminal | Envelope |
|---|---|
| Success advisory | `AUDITED` with valid `core` |
| AI-disabled success | `agent.engaged=false`, empty trajectory |
| Fail closed | Explicit deny/abstain reason; no prohibited fields |
