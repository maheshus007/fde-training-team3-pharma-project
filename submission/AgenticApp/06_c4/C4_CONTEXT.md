# C4 Level 1 — System Context

| Field | Entry |
|---|---|
| Artifact status | **stable** for actors/systems; containers refined with ontology/KG provisional |

```text
[QP/QA] [PV Assessor] [Supply Planner] [Auditor]
              | purpose + entitlement (execution-time)
              v
        +------------------+
        | AEGIS AgenticApp |  advisory, offline-capable
        +--------+---------+
                 | read-only ACL adapters / fixtures
     +-----------+----------+-----------+----------+
     v           v          v           v          v
   LIMS       MES/eBR      QMS      Safety DB   Inventory/IRT*
```

\*IRT/inventory: read for supply/trial demand constraints only — **no** eligibility decisions; **no** stock writes.

| Question | Answer |
|---|---|
| Who uses it? | Authorized Quality, PV, Supply reviewers |
| What does it do? | Cite, flag, abstain, draft options, assemble readiness packs |
| What does it never do? | Disposition; final PV; allocate/ship/recall; eligibility; formulation/spec change |
| Trust model | Docs/tools untrusted until verified |
