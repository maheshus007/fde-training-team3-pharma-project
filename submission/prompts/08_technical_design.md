> **V3 adaptation:** Team method prompt. Do not edit hashed prompts/PROMPT_LIBRARY.md. Write all outputs under submission/ only. Obey package control prompts, GxP fail-closed contracts, and prohibited-action boundaries. See submission/prompts/PROMPT_MAPPING.md.
# Prompt 08 — Technical Design (SRS Contracts)

**Lifecycle stage:** Spec-Driven Development — Technical Design  
**Framework derived:** Spec-Driven Development (modern SRS / technical specification); VisionScan-style SDD contracts  
**Core question:** Exactly how should the system behave — contracts, data, errors, NFRs?  
**Prerequisites:** Prompt 05 feature specs; Prompt 06 C4; Prompt 07 ADRs.  
**Primary output type:** Technical contracts the agent must not invent at coding time.

---

## Intent

This is the layer that **pays for AI coding**: exact request/response shapes, validation with real values, error paths with status codes, state transitions, data model, and measurable NFRs.

Architecture (C4) said *where* code belongs. ADRs said *why*. This prompt says *exactly how it behaves* so nothing material is left to guess.

---

## Entry criteria

- Feature specs with BRs and ACs exist.  
- C4 map and ADR index exist (stable or provisional).  
- Architecture review from Prompt 07 is `pass` or `conditional` (not `fail`).  
- Spec ambiguities from Prompt 05 are visible (resolve or explicitly assume here).
- Matching/confidence checklist from Prompt 05 is available when applicable.

---

## Produce

### A. API / interface contracts

For each endpoint or interface needed by in-scope features:

- Method, path (or message name)  
- Request schema and validation rules (**numeric/time values required**, not adjectives)  
- Response schemas for success  
- Error cases with HTTP (or protocol) codes  
- Idempotency / auth expectations if in scope (or “auth out of scope — trusted network only” if that is the decision)

### B. Data model

- Entities/tables/collections with fields and types  
- Identity and timestamp semantics  
- Relationships and constraints  
- What must never be written back (align to C4/ADR)

### C. State transitions

- Session/entity state machines as applicable  
- Triggers and illegal transitions

### D. Non-functional requirements

Measurable only (VisionScan style). Examples: latency budgets, coverage targets, logging, transactionality, deployment constraints. Untestable “preferences” are not NFRs.

### E. Error envelope & security controls

- Standard error JSON (or equivalent)  
- Validation, injection safety, CORS, logging/correlation, no internal traces in client responses  
- Explicit note if authentication is out of scope and what that implies for deployment

### F. Module / layering rules (agent constraints)

- Folder/module layout aligned to C4  
- Rules such as: routers hold no business logic; services hold no SQL; UI does not bypass API — state as enforceable constraints

### G. Pre-build traceability matrix

| Feature / FR | Endpoint(s) / contract | Business rules | Acceptance criteria | ADR(s) | Ambiguity status |
|--------------|------------------------|----------------|---------------------|--------|------------------|
| … | … | … | … | … | resolved / assumed / open |

### H. Spec ambiguity closure

- Resolve items from Prompt 05 `spec_ambiguities.md` and `matching_confidence_checklist.md` with values, or mark **assumed** with revisit triggers, or **open** (blocks related implementation tasks).
- For matching/classification features: lock **priority order** and **numeric thresholds** (or document open blockers).

### H2. Orphan / gap audit (VisionScan appendix style)

Record gap audit inside artefact `09_REQUIREMENTS_TRACEABILITY.md` (do not create `traceability_gap_audit.md`) that explicitly flags:

1. **FR without AC**  
2. **BR without verifying AC** (or without a numeric threshold where the BR needs one)  
3. **AC without endpoint/contract**  
4. **Endpoint without FR**  
5. **Matching/confidence rule without a number** (or marked Unknown + backlog)  
6. **Error envelope / security rule without an AC or NFR check**

Every gap must be: fixed now, assumed with revisit trigger, or open-blocked for tasks.

### I. Deployment notes (lightweight)

- Containerization / env config / health checks / reverse-proxy expectations if in scope (VisionScan-style), as measurable NFRs or explicit out-of-scope.

### Lean / DMAIC lens (spine — thin)

**DMAIC focus this stage:** **Improve** contracts to prevent token/retrieval/integration/eval waste; set measurable NFRs for **Measure/Control**.

In artefact `02_DMAIC_WORKBOOK.md` (short notes only), record:

1. Contract choices that cap Token / Retrieval / Context waste (limits, filters, pagination)?  
2. Error/retry rules that avoid blind Model waste (retry without diagnosis)?  
3. NFRs that are actually measurable Control metrics for Prompt 12?  
4. Ambiguities left open that would cause Extra processing at build time?

---

## Exit criteria (handoff to Prompt 09)

- [ ] APIs/data/state/NFRs/errors are specified for the minimum governed slice.  
- [ ] Traceability matrix covers in-scope FRs (or explicit gaps listed).  
- [ ] `traceability_gap_audit.md` has no unmarked orphans (FR/BR/AC/threshold/contract).  
- [ ] Matching/confidence thresholds resolved, assumed, or open-blocked.  
- [ ] No open ambiguity remains unmarked for in-scope build path.  
- [ ] Values are precise where claimed; adjectives without numbers are rejected.  
- [ ] Contracts respect C4 boundaries and ADR guardrails.  
- [ ] Specs landed in artefact `12_INTEGRATION_CONTRACTS.md` (and PUB-09–15 contract extensions under `submission/evaluation/` as applicable).  
- [ ] artefact `02_DMAIC_WORKBOOK.md` is complete (feeds Prompt 09 consolidation).

---

## Constraints

- Do not start feature coding here.  
- Do not expand PRD out-of-scope.  
- Do not run full Prompt 09 waste registers here — only the thin lens.  
- Prefer small focused files (api, data-model, nfrs, errors) over one monolith.

---

## Output

Per `WORKSHOP_DEPLOYMENT_PLAN.md` **Stage 3**, write contracts into:

- `submission/artefacts/12_INTEGRATION_CONTRACTS.md`
- Update trace rows in `09_REQUIREMENTS_TRACEABILITY.md` only if needed for Stage 3

PUB-09–15 participant contracts and Stage 4 threat artefacts wait for later stages. Do **not** create artefacts 16+.

See `submission/prompts/PROMPT_MAPPING.md`.
