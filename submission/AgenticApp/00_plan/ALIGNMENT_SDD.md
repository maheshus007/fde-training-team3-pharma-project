# Alignment — Spec-Driven Development + Cursor enterprise stack

| Field | Entry |
|---|---|
| Date | 2026-08-11 |
| Verdict | **Aligned on SDD steps 1–3 and principles. Step 4 (implement) is next. Enterprise MCP/SAP stack is intentionally out of this POC.** |

---

## A. Spec-first SDLC (6 steps)

| Step | Diagram | Our artefact | Status |
|---|---|---|---|
| 1 Define the spec | requirements, goals, constraints, ACs → Spec v1 | PRD, FR-A..F, AC-A..F, CQ-1..9 | **Done** |
| 2 Validate & align | approved spec | Architecture review (conditional); P08/P10 validation | **Done** (conditions mapped to tasks) |
| 3 Design from the spec | architecture/design from spec only | C4, ADR-AA, SRS, MODULE_LAYERING | **Done** |
| 4 Implement to the spec | no guessing, no scope creep | BUILD_SDD + TASK_INDEX T-001..T-018 | **Next** (T-001) |
| 5 Test against the spec | ACs → tests | AC stubs + existing contract/prohibited/trust/authz tests | **Partial** (stubs skip until code) |
| 6 Evolve the spec | feedback → Spec vNext | Rule: gap → patch `08_technical_design/` then code | **Process exists**; no vNext yet |

**Center of the diagram (SPEC drives design / guides implementation / enables testing / informs evolution):**  
SoT = `BUILD_SDD.md` + AgenticApp pack + package `evaluation/contracts/*.schema.json`. That matches.

**Principles**

| Principle | Us |
|---|---|
| Clarity before code | Specs closed before T-001 |
| Spec is source of truth | Cursor rule loads BUILD_SDD, not a generic build prompt |
| Alignment is explicit | Conditional architecture review; blocked/deferred labeled |
| Testable by design | Every in-scope AC has a `submission/tests/` case or deferral |

---

## B. Cursor / enterprise layers (diagrams 2–4)

These diagrams are an **enterprise control plane**. Our POC implements the **same ideas at workshop scale**, not SAP/M365/MCP production.

| Layer | Diagram | AEGIS mapping | Align? |
|---|---|---|---|
| 1 User / workforce | banker, RM, ops; Cursor = engineers | QP, PV assessor, supply planner, auditor; Cursor builds `submission/` | **Yes** (personas differ) |
| 1 Governance | identity, entitlement, consent, domain, jurisdiction | Fixture entitlements, purpose-bind, DDD, ontology; consent/INJ-060 flag-only | **Partial** |
| 2 AI access / routing | intake, risk tier, model catalog, budgets | `AEGIS_RUNTIME_MODE`, kill switch, model hash pin, AA-NFR budgets | **Partial** (POC, not employee invite) |
| 3 Application / agent | business agents + Cursor engineering agent | Product: FR-D orchestrator + FR-F HITL. Cursor: code against SDD | **Yes** |
| 4 Orchestration / policy | plan, tools, HITL, runtime policy | Signed tools, policy_guard, checkpoints, ack 412 | **Designed**; **not coded** |
| 5 MCP / connector | Web APIs, RAG, SAP, DB, M365, CRUD MCP | **Ports + adapters** (InferencePort, GraphPort); fixtures not live SoR | **Intentional gap** — no MCP servers, no SAP |
| 6 Enterprise systems | ERP, CRM, lakes | Brownfield via **read-only challenge CSVs** | **Assessment substitute** |
| 7 Validation gate | tests, SAST/DAST, PR, compliance | `submission/scripts/test.py` + AC map; no SAST/DAST yet | **Partial** (tests yes; scanners later) |
| 8 Output / release | code, docs, CI, controlled release | Waves E–F: scripts, runbooks, `--final` | **Later** |
| 9 Observability | telemetry, drift, feedback → spec | Audit records, AI-disabled continuity; no live LLM ops loop | **Later / thin** |

**Connector lane vs us:** we do **not** give Cursor CRUD against production DBs. Connectors are **in-app**: `graph_memory` / lazy Cosmos, `inference_stub` / lazy Azure, entitlement fixtures. Writes to MES/LIMS/safety SoR are **forbidden**. That is stricter than the generic MCP CRUD lane — and correct for GxP.

---

## C. Honest gaps (do not paper over)

1. **Implement + verify not started** — SDD says we are between step 3 and 4.  
2. **No MCP layer** — out of POC; ports/adapters are the substitute.  
3. **No enterprise model-routing catalog / credit gates** — kill switch + 3-call budget is the slice.  
4. **Validation gate** is unittest/contracts, not SAST/DAST/buddy PR.  
5. **Spec vNext** only after T-001+ learnings (patch SRS, do not silently code around it).

---

## D. How we stay aligned while building

1. Load BUILD_SDD + one TASK_INDEX unit.  
2. Tests from ACs before inference.  
3. If code needs a shape that is not in SRS → **update spec first**.  
4. Assessment must stay green without Azure.  
5. Do not add MCP/SAP/M365 to “look like” the enterprise poster.
