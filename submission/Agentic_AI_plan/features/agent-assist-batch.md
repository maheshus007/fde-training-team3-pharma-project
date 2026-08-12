# Feature — Agent Assist: Batch Evidence

**Question this file answers:** What should batch agent-assist do?

| Field | Entry |
|---|---|
| Feature ID | F1 |
| Workflow | `batch_evidence` |
| Version / date | 1.0 / 2026-08-12 |

## Actor

Authorized batch evidence reviewer / QP support.

## Preconditions

- Entitlement active and fresh for purpose `batch_review_readiness`.
- Deterministic `reconcile_batch` can run offline from fixtures.
- `agent_mode` is `assist` **and** kill switch is open; otherwise agent is skipped.

## Allowed actions

reconcile, cite, flag, abstain (per `ai_use_boundaries.csv`).

## Prohibited actions

release, reject, reprocess, recall, disposition, any write to SoR.

## Happy path

1. Re-check authorization at execution time.
2. Run deterministic batch reconciliation → `core`.
3. If agent engaged: call allowlisted read-only tools; record trajectory.
4. Produce non-authoritative annotations (e.g. summarize contradictions already in `core`).
5. Merge into run envelope; force `human_review` acknowledgements.
6. Validate `core` against package batch schema.

## Exceptions

| Case | Behaviour |
|---|---|
| Kill switch / `agent_mode=disabled` | Return envelope with `agent.engaged=false`; `core` only |
| Stale entitlement | Deny; fail closed |
| Unapproved / poisoned tool | Deny tool; continue deterministic or fail closed per gate |
| Unit mapping `approved=no` (INJ-024) | Abstain; no silent convert |
| Budget / step exhaustion | Discard incomplete annotations; return deterministic `core` |

## Acceptance criteria

- [ ] `core` has no disposition/release fields
- [ ] `core.execution_status == not_executed`
- [ ] Forced acknowledgements retained when contradictions/gaps present
- [ ] Annotations have `authoritative: false`
- [ ] Trajectory actions never include disposition/release
