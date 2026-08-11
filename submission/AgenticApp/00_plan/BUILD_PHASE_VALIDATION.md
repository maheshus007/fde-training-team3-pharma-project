# Build-phase plan validation — agentic app coverage

| Field | Entry |
|---|---|
| Date | 2026-08-11 |
| Verdict | **Covered for the minimum governed agentic slice.** Two items were under-specified in the plan wording (now locked). Nothing in-scope is missing a wave. |

Plan: `BUILD_PHASE_PLAN.md`. Tasks: `TASK_INDEX.md`. Spec: `BUILD_SDD.md`.

---

## 1. PRD in-scope → wave

| PRD item | Wave / task | Gap? |
|---|---|---|
| A batch pack | C / T-009 | No |
| B PV pack | C / T-010 | No |
| C draft supply | C / T-011 | No |
| Ontology / semantic | B / T-008 | No |
| Evidence KG read/query | B T-005..007; E T-015 Cosmos | No |
| Agentic orchestrator | D T-012a/b/c | **Lock:** allowlisted tools only (below) |
| HITL Taipy + forced view | F T-016; D T-013 AC-F1 | No |
| Deterministic + kill switch | A T-003; D T-012b; ACs A5/B6/C4 | No |
| Audit / evidence export | **Split:** append on submit = T-013 (AA-NFR-13). Inspection pack FR-X-05 = **deferred** after build | Labeled, not unmarked |

---

## 2. Agentic loop (this is the “agentic AI” path)

GEN_AI §14 minimum workflow is mapped:

```text
request → T-004 entitlement
       → T-005 ACL/fixtures into graph
       → T-008 ontology
       → T-006/007 KG citation
       → T-009/010/011 deterministic engines
       → T-001/contracts policy_guard
       → T-014 optional Azure structured JSON (never SoT)
       → T-012c checkpoint
       → T-013/T-016 HITL
       → T-013 audit append
```

| Agent piece | Task | Must / must-not |
|---|---|---|
| Tool allowlist (8 names) | T-012a | Only `resolve_concept`, `get_provenance`, `find_conflicts`, `traverse_evidence_path`, `assess_readiness`, `propose_duplicate_candidates`, `enumerate_draft_options`, `request_human_review` |
| Signed manifests | T-012a | Poisoned/unsigned deny |
| Budgets 20/30/3 | T-012b | Over budget → abstain, still schema-valid |
| Kill switch | T-012b + T-014 | `inference_used=false` |
| Azure OpenAI T=0 JSON | T-014 | Lazy; assessment stub; hash pin INJ-070 |
| Inference never writes SoR | ADR-AA-001/016 | Rules remain source of truth |
| Checkpoints / idempotency | T-012c | 409 on payload mismatch |
| HITL ack | T-013 / T-016 | 412 if conflicts not viewed |

---

## 3. FR / ADR / C4

| ID | Plan coverage |
|---|---|
| FR-A AC-A1..A7 | T-009 |
| FR-B AC-B1..B9 | T-010 |
| FR-C AC-C1..C5 | T-011 |
| FR-D AC-D1..D5 | T-012a/b/c, T-003/004 |
| FR-E AC-E1..E5 | T-005..007 |
| FR-F AC-F1..F2 | T-013, T-016; F3 deferred keyboard |
| ADR-AA-001..009, 011..018 | Mapped; 015/018 CQ gate = Wave B |
| C4 containers | API, engines, ontology, graph, agent, inference, policy, Taipy, audit |

---

## 4. Dual runtime (package + product stack)

| Concern | Covered? |
|---|---|
| Assessment without keys | T-003 stub + T-005 memory graph; T-017 test.py |
| Cloud Azure + Cosmos | T-014/T-015 lazy; live **blocked** |
| `supply_options` enum | T-001 |
| additionalProperties / prohibited | existing tests + engines |
| Product tree `aegis-sdd` + scoring shims | Yes; stay under `submission/` |
| HTTP | Optional; Python service is enough | Not a miss |

---

## 5. Intentionally not in build (still complete for POC)

MCP/SAP/M365 · apps/admin · live CI cloud · WCAG AA · CAPA auto-link · INJ-044 · FR-X-05 inspection zip · BR-01 % · Azure AD · Neo4j · artefact 28 · SAST/DAST

---

## 6. Locks applied this audit (were thin, not missing)

1. **T-013** writes ≥1 audit record per submit (`submission/evidence/audit/`, AA-NFR-13). Full export pack stays deferred.  
2. **T-012** is a **bounded tool loop** on the eight named tools, then engines; it is not free-form function calling. Azure may **suggest** structured JSON after rules; policy_guard still owns the pack.  
3. Canonical code after T-001 lives in `aegis-sdd`; `submission/src` re-exports (avoid two logics).

---

## 7. Verdict

The plan **does** cover the agentic app: workflows A–C, ontology, KG (memory then Cosmos), orchestrator, Azure behind kill switch, Taipy HITL, assessment continuity.

It does **not** cover enterprise MCP or production SaaS. That is correct.

**Still start at T-001 only.**
