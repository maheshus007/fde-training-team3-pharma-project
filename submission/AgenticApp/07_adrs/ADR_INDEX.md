# ADR Index — AgenticApp (Prompt 07)

> **ID scheme:** `ADR-AA-NNN` are AgenticApp working ADRs. They must **not** overwrite scored `artefacts/11_ADR_REGISTER.md` ADR-001..012 without an explicit merge map.  
> Scored ADR-010 = budgets/checkpoints/rollback. AgenticApp offline-KG decision is **ADR-AA-015** (renumbered from mistaken ADR-010).

| ADR-AA | Title | Status | Maps / relates to scored | DDD / C4 link |
|---|---|---|---|---|
| 001 | Deterministic-first execution path | accepted | ≈ scored ADR-001 | Platform |
| 002 | Replaceable inference behind kill switch | accepted | ≈ scored ADR-002 / 011 | Inference adapter |
| 003 | Fail-closed contracts | accepted | ≈ scored ADR-003 / 007 | All workflows |
| 004 | Authority-checked retrieval | accepted | ≈ scored ADR-004 | RAG / ACL |
| 005 | Signed tool manifests only | accepted | ≈ scored ADR-005 | Agent tools |
| 006 | Supply no side effects | accepted | ≈ scored ADR-006 | SupplyOptionSet |
| 007 | Execution-time entitlement re-check | accepted | ≈ scored ADR-012 | AuthZ |
| 008 | HITL mandatory acknowledgements | accepted | ≈ scored ADR-009 | Workbench |
| 009 | Agent budgets, checkpoints, stop | accepted | ≈ scored ADR-010 | AgentRun |
| 011 | Ontology/semantic before compare | accepted | new / artefact 07 | Ontology service |
| 012 | Canonical enum `supply_options` | accepted | code fix | policy_guard |
| 013 | IDMP non-merge | accepted | D-201 | ProductIdentityMap |
| 014 | Approved unit mapping only | accepted | D-010 / scored themes | LabResultView |
| **015** | Evidence graph dual-path (product + assessment) | **accepted (dual-path)** | D-205 retained as assessment fallback | EvidenceGraphView |
| **016** | Azure OpenAI as product LLM | accepted (stub in assessment) | scored ADR-002 adapter | Inference adapter |
| **017** | Taipy HITL workbench | accepted | FR-F | Workbench |
| **018** | Azure Cosmos DB Gremlin as product graph | accepted (in-memory port in assessment) | D-205 / artefact 08 to sync | GraphPort |
| **019** | LangGraph as agent orchestrator | accepted (optional package in assessment) | FR-D / ADR-AA-009 | AgentRun |

File note: `ADR-AA-010_offline_evidence_kg.md` holds ADR-AA-015 text.

## Backlog-blocked

| ADR | Blocked on |
|---|---|
| ADR-AA-015/018 | CQ-1/3/6 on **assessment GraphPort** before defence claims |
| ADR-AA-016 | Model deployment name + hash pin; stub tests |
| ADR-AA-009 budgets | FinOps measured numbers (artefact 23) |
