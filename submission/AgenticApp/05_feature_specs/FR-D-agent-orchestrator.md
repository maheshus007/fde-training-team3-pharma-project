# FR-D — Agentic Orchestrator

| Field | Entry |
|---|---|
| Matching/confidence | N/A |

## Preconditions

- Valid request envelope; known workflow ∈ {batch_evidence, pv_intake, supply_options}  
- Approved tool manifest set available  

## Happy path

1. Accept envelope (user, purpose, object, as-of, workflow, idempotency_key).  
2. Re-check entitlement; deny if stale.  
3. Plan bounded tool sequence under budget.  
4. Invoke tools; validate each result via contracts + policy_guard.  
5. Checkpoint; on stop persist reason.  
6. Hand off to HITL when required.  

## Exceptions

- Poisoned manifest → deny tools  
- BudgetExhausted → stop cleanly  
- Kill switch → disable inference only  
- Duplicate idempotency_key → return prior checkpoint result (no duplicate work product spam)

## Business rules

- BR-D1: Never bypass policy_guard.  
- BR-D2: Stop on budget / stale auth / high-risk unresolved contradiction.  
- BR-D3: Signed manifests only.  
- BR-D4: Canonical `supply_options` enum.  
- BR-D5: Purpose limitation on tool visibility.  

## Acceptance criteria

- AC-D1: Poisoned tool manifest denied.  
- AC-D2: Stale auth denied.  
- AC-D3: Checkpoint resume idempotent (no side effects exist).  
- AC-D4: Kill switch disables inference; rules path remains.  
- AC-D5: Idempotency key replay safe.  

## Ambiguities

- Exact numeric budgets — provisional (ADR-AA-009); finalize in FinOps.

## Out of scope

Write tools to SoR.
