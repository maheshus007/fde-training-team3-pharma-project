# SRS — State transitions (Prompt 08)

## 1. AgentRun

```text
accepted → authz_checked → (denied)
                         → running → checkpointed ⇄ running
                                  → budget_exhausted (terminal, not_executed)
                                  → completed_advisory (terminal, not_executed)
                                  → kill_switch_inference_off → running (rules only)
```

Illegal: `completed_executed`; any transition that sets `execution_status` other than `not_executed`.

## 2. Human review (HITL)

```text
review_required → conflicts_unviewed → (ack attempted) → rejected_412
                 → conflicts_viewed → acked
```

Ack does **not** mean batch released or option executed.

## 3. Readiness_state (batch output)

Computed, not a stored workflow that users advance:

| State | When |
|---|---|
| `insufficient_evidence` | gaps non-empty and no blocking contradiction forcing conflicted |
| `conflicted_evidence` | ≥1 contradiction (e.g. INJ-021 both sides) |
| `ready_for_authorized_review` | no unresolved unit/identity/authority abstention **and** no unsurfaced contradiction; gaps may still exist as listed |

**Assumed:** any genealogy contradiction ⇒ `conflicted_evidence` even if pack is otherwise complete. Revisit: none for POC.

## 4. Runtime mode

```text
assessment (default) ↔ cloud (requires keys)
either → ai_disabled (kill switch or env)
```

Illegal: `cloud` with missing Azure/Cosmos keys without fallback — **assumed** fallback to assessment GraphPort + inference stub and `health.graph=degraded`.
