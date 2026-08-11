# Architecture Decision Register

> Participant working artefact for Project AEGIS-PHARMA. Analysis cites challenge evidence under `case/`, `data/`, `knowledge/` and `starter/`; implementation remains under `submission/`.

## Document control

| Field | Entry |
|---|---|
| Team / owner | Team 3 — Architecture / integration lead |
| Version / date | 1.0 / 2026-08-10 |
| Reviewers | GxP/quality lead; Security/privacy lead; Product/value lead |
| Status | Reviewed |
| Related requirements / ADRs | D-001..D-010; C4 `10_C4_ARCHITECTURE.md`; contracts `12_INTEGRATION_CONTRACTS.md` |

## Purpose

Record architecture decisions that bound AEGIS-PHARMA as a deterministic-first, offline-capable advisory system with replaceable inference, fail-closed prohibited actions and human-in-the-loop controls.

Accountable owner: Architecture / integration lead. Completion criteria: at least ten accepted ADRs with context, options, consequences and revisit triggers.

## Evidence register

| Evidence ID | Source path / record | Authority and effective time | Fact used | Integrity / limitation |
|---|---|---|---|---|
| E-411 | `case/INTEGRATED_CASE.md` §5 | Case operating properties | Provenance, abstention, budgets, checkpoints, rollback, kill switch | Narrative |
| E-412 | `data/ai_use_boundaries.csv` | INJ-006 | Prohibited autonomous decisions | Binding |
| E-413 | `PACKAGE_SCOPE_AND_ASSUMPTIONS.md` | Package assumptions | Offline mode; participant architecture freedom | Synthetic |
| E-414 | `starter/contracts/WORKFLOW_CONTRACTS.md` | Starter contracts | Fail-closed I/O boundaries | Points to evaluation schemas |
| E-415 | `knowledge/AI_GXP_BOUNDARY.md` (K-003) | Effective 2026-05-01 | AI cannot replace accountable GxP decisions | Synthetic policy |
| E-416 | `data/continuity_requirements.csv` | INJ-082 | AI-disabled continuity windows | Synthetic |

## 1. ADR index

| ADR | Title | Status | Owner |
|---|---|---|---|
| ADR-001 | Deterministic-first execution path | Accepted | Architecture |
| ADR-002 | Replaceable inference interface behind kill switch | Accepted | Architecture |
| ADR-003 | Fail-closed rejection of prohibited action fields | Accepted | GxP + Build |
| ADR-004 | Authority-checked retrieval before citation | Accepted | Security + Domain |
| ADR-005 | Signed / hashed tool manifests only | Accepted | Security |
| ADR-006 | Supply path enforces no side effects | Accepted | Architecture + GxP |
| ADR-007 | Versioned structured contracts with additionalProperties denial | Accepted | Architecture |
| ADR-008 | Offline synthetic mode as primary POC runtime | Accepted | Build |
| ADR-009 | Human-in-the-loop mandatory for readiness and options | Accepted | GxP |
| ADR-010 | Budget, checkpoint, rollback and stop policy | Accepted | Evaluation + Architecture |
| ADR-011 | Kill switch isolates inference without disabling advisory continuity | Accepted | Architecture |
| ADR-012 | Execution-time entitlement re-check (deny by default) | Accepted | Security |

## 2. Context and forces

| Force | Evidence | Pull |
|---|---|---|
| BR-01 speed | Board −14% release lead time | Automate more |
| AI-use boundaries | E-412 | Automate less / never decide |
| Offline workshop | E-413 | No cloud dependency |
| Continuity | E-416 | AI-disabled path must work |
| Trust defects | INJ-065..070 | Deny untrusted tools/docs/models |
| Unit integrity | INJ-024 | No silent conversion |
| Automation bias | INJ-071 | Force human evidence viewing |

## 3. Options considered

Across ADRs the recurring options were: (A) LLM-first agent with write tools; (B) rules-only with no inference option; (C) hybrid deterministic core + optional replaceable inference + fail-closed contracts. Team 3 selected (C) unless an ADR states otherwise.

## 4. Decision and rationale

### ADR-001 — Deterministic-first execution path

**Decision:** Default runtime is rules/fixtures reconciliation; inference is optional assist only (aligns D-004).

**Rationale:** No-AI baselines are first-class competitors (INJ-003); continuity requires non-inference path (E-416); model hash mismatch must not halt advisory work (INJ-070).

**Consequences:** Slightly less “AI showcase” optics; higher auditability and offline reliability.

### ADR-002 — Replaceable inference interface behind kill switch

**Decision:** Inference accessed only through a narrow adapter interface (prompt in → structured suggestion out); implementation swappable; kill switch disables adapter.

**Rationale:** Vendor/model churn and hash mismatch (INJ-070); need AI-disabled continuity without rewriting workflows.

**Consequences:** Extra interface discipline; forbids embedding model calls inside reconciliation core.

### ADR-003 — Fail-closed rejection of prohibited action fields

**Decision:** Response schemas deny additional properties and forbid disposition, final PV conclusions and supply side-effect fields (`evaluation/contracts/`; E-412; E-414).

**Rationale:** Hard gates and poisoned tool risk (INJ-066); K-003 boundary (E-415).

**Consequences:** Contract tests must stay green; any “helpful” disposition field is a defect.

### ADR-004 — Authority-checked retrieval before citation

**Decision:** Cite only after status, authority, effective date, integrity hash and applicability are verified; otherwise abstain/escalate (D-008).

**Rationale:** Untrusted knowledge and supersession injects (INJ-065, INJ-031).

**Consequences:** More abstentions; slower false “ready” states — intentional.

### ADR-005 — Signed / hashed tool manifests only

**Decision:** Tools must present approved hash/signature and read-only capability; write-capable or mismatched manifests are rejected.

**Rationale:** Tool-manifest poisoning requesting disposition writes (INJ-066).

**Consequences:** No dynamic tool registration without Security approval.

### ADR-006 — Supply path enforces no side effects

**Decision:** Supply responses require `no_side_effects: true`; reservation/allocation/shipment/quality-status/recall properties are schema-illegal; options remain `status: draft`.

**Rationale:** INJ-006; WORKFLOW_CONTRACTS supply clause; ethical shortage constraints (INJ-056).

**Consequences:** Humans execute selected options in SoR systems outside AEGIS.

### ADR-007 — Versioned structured contracts with additionalProperties denial

**Decision:** I/O uses versioned JSON Schema contracts aligned to `starter/contracts/WORKFLOW_CONTRACTS.md` and `evaluation/contracts/`; unknown fields fail validation.

**Rationale:** Prevent silent contract drift and prohibited field injection.

**Consequences:** Extensions require new version + compatibility tests.

### ADR-008 — Offline synthetic mode as primary POC runtime

**Decision:** POC runs from package fixtures without internet, cloud keys or live instructor services (A-003; E-413).

**Rationale:** Workshop fairness and continuity; package design intent.

**Consequences:** Live brownfield adapters deferred; fixtures must carry authority metadata.

### ADR-009 — Human-in-the-loop mandatory for readiness and options

**Decision:** Every workflow response includes human_review requirements; readiness/option acceptance needs named authorized role; forced critical-deviation view counters INJ-071.

**Rationale:** K-003; QP/PV mandates in stakeholder pack; automation bias inject.

**Consequences:** Review minutes count in value metrics (INJ-077).

### ADR-010 — Budget, checkpoint, rollback and stop policy

**Decision:** Bound steps, tokens and wall-clock; checkpoint after authZ and after reconciliation; on budget/stop, discard incomplete inference and return deterministic result or abstain.

**Rationale:** Case §5 operating properties (E-411); FinOps later gates.

**Consequences:** Partial AI answers never publish as complete readiness.

### ADR-011 — Kill switch isolates inference without disabling advisory continuity

**Decision:** Kill switch turns off inference adapter only; deterministic advisory path remains available for all three workflows.

**Rationale:** Continuity CSV (E-416); avoid “all or nothing” outage.

**Consequences:** Operators must understand two modes; runbooks required.

### ADR-012 — Execution-time entitlement re-check (deny by default)

**Decision:** Re-validate user, purpose, object, role and tool authorization at execution; stale cache hits deny (D-009; INJ-067).

**Rationale:** Baseline diagnostics show stale entitlement cache.

**Consequences:** Higher deny rates under cache defects — treated as correct safety behaviour.

## 5. Consequences and risks

| ADR | Residual risk | Mitigation |
|---|---|---|
| ADR-001/002 | Underused inference if budgets too tight | Measure no-AI vs assist on fixtures |
| ADR-003/007 | Schema rigidity slows feature adds | Versioned extensions with tests |
| ADR-004/005 | False abstention under incomplete metadata | Domain improves fixture authority fields |
| ADR-009 | Reviewer rubber-stamping | Forced evidence acknowledgement (INJ-071) |
| ADR-012 | Operational friction | Fix entitlement source of truth, not relax deny |

## 6. Validation evidence

| ADR | Validation |
|---|---|
| ADR-003, ADR-006, ADR-007 | `submission/tests/test_workflow_contracts.py` positive pass / prohibited fail |
| ADR-001, ADR-008, ADR-011 | Offline AI-disabled demo path |
| ADR-004, ADR-005, ADR-012 | Entitlement/tool/authority adversarial tests |
| ADR-009, ADR-010 | Human-review and budget stop tests |

## 7. Revisit triggers

| Trigger | ADRs to reopen |
|---|---|
| Continuity CSV changes AI-disabled windows | ADR-008, ADR-011 |
| New write tool approved by Security (unexpected) | ADR-005, ADR-006 |
| Evaluation proves rules path cannot meet agreed proxies while hard gates hold | ADR-001, ADR-002 |
| Contract schema major version bump in package | ADR-007 |
| Jurisdiction requires different human-role mapping | ADR-009 |

## Risks, assumptions and unresolved gaps

| ID | Type | Description | Impact | Owner | Due / trigger | Status |
|---|---|---|---|---|---|---|
| R-411 | Assumption | Evaluation schemas remain the executable minimum through defence | Test drift | Architecture | Schema change in package | Accepted |
| R-412 | Gap | Detailed inference adapter API refined in threat model | Interface polish | Security | Phase 4 artefacts | Open |

## Traceability and acceptance

| Claim / requirement | Architecture or control | Test / evaluation | Evidence path | Result |
|---|---|---|---|---|
| ≥10 ADRs covering required themes | ADR-001..012 | Independent review | This register | Accepted |
| Fail-closed prohibited actions | ADR-003, ADR-006 | Contract tests | `submission/tests/` | Tests green |
| Offline + kill switch | ADR-008, ADR-011 | Continuity | E-416 | Design accepted |

## Review record

| Reviewer | Role | Finding | Resolution | Date |
|---|---|---|---|---|
| GxP/quality lead | Reviewer | Add explicit human-in-the-loop ADR | ADR-009 | 2026-08-10 |
| Security/privacy lead | Reviewer | Split tool signing from authority retrieval | ADR-004 and ADR-005 | 2026-08-10 |
| Product/value lead | Reviewer | Keep deterministic-first aligned to no-AI comparison | ADR-001 cites INJ-003 | 2026-08-10 |

---

## Prompt 09 / 10 structural reopen gate (2026-08-11)

| Field | Entry |
|---|---|
| Decision | **cleared** |
| ADR reopen | **Not required** for Prompt 10 handoff. ADR-AA-012 (`supply_options`) and CQ proofs are **implementation tasks** (T-001, T-006/T-007), not architecture reopens |
| Residual | Full Prompt 09 DMAIC workshop pending; ADR-AA-015 remains conditional on CQ tests (architecture review O-1) |
| Recorded for | `submission/prompts/10_implementation_tasks.md` entry/exit |
