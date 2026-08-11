> **V3 adaptation:** Team method prompt. Do not edit hashed prompts/PROMPT_LIBRARY.md. Write all outputs under submission/ only. Obey package control prompts, GxP fail-closed contracts, and prohibited-action boundaries. See submission/prompts/PROMPT_MAPPING.md.
# Prompt 12 — Assurance & Control (Deliver & Evaluate)

**Lifecycle stage:** Deliver & Evaluate / DMAIC Control / Spec-Driven Development — Tests & Review  
**Framework derived:** Assurance against prior artifacts + DMAIC Measure/Control + AC verification  
**Core question:** Does the system match the design and the claims we make about it?  
**Prerequisites:** Prompt 11 build, task execution log, and updated traceability; Prompts 02–10 artifacts.  
**Primary output type:** Evaluation report with residual risk and control actions.

---

## Intent

Close the loop: audit the built system against **SCQA/PRD outcomes**, **feature ACs/BRs**, **technical contracts**, **DDD** rules/AI/HITL boundaries, **C4** structure, **ADR** decisions, and **Lean/DMAIC** measures. Separate **offline evaluation** (domain/AC cases) from **online/operability assurance** (runtime, security, degraded mode).

**DDD stage 16 (production readiness & handover):** assess what is production-ready vs still PoC; name handover owners.

**Lean spine close:** after scoring, record Control roll-up inside artefacts `22`/`24`/`25`/`28` (do not create a separate control_lens file), consolidating DMAIC notes from Prompts **10–12** and Prompt 09 Control.

---

## Entry criteria

- Governed slice is runnable.
- Traceability matrix (FR → contract → AC → task → code/test) and PoC-vs-production list exist.
- DMAIC Measure targets and Control owners are defined.

---

## Assess

### Design fidelity

- Architecture-to-code consistency with C4 and DDD  
- ADR implementation (followed, violated, or deferred)  
- Technical contracts honored (APIs, validation values, error envelope)  
- Module rules respected (e.g. UI does not bypass API)  
- Ubiquitous language reflected in UX, APIs, and logs where claimed  
- Feature ACs and BRs verified or explicitly failed/inconclusive  

### Data & authority

- Data-contract handling (enforced, versioned, documented)  
- Identifier and timestamp behavior (stability, timezone/event vs report time)  
- Conflict and freshness visibility  
- Authority and prohibited-language / source-of-truth controls  
- Privacy; security and remote-access handling  

### AI / decision quality

- Deterministic behavior where claimed  
- Explainability of outputs  
- False-positive and false-negative examples documented  
- HITL paths exercised for domain-critical decisions  
- Evaluation cases use DDD vocabulary and feature AC IDs (from Prompts 04–05)  
- Lean evaluation waste check — metrics tied to release/risk decisions  

### Operability

- Degraded-mode operation  
- Critical user workflows end to end  
- Performance under expected load (vs NFRs in Prompt 08)  
- Observability useful for failure explanation (avoid observability waste)  

### Control & risk

- DMAIC Control: standards, monitors, owners, revisit triggers  
- Residual risk — accepted, deferred, or requiring sponsor decision  
- Open items from `spec_ambiguities` / `ambiguity_closure`  

---

## Produce

1. Evaluation report with **pass / fail / partial / `inconclusive (data scarcity)`** per assessment area (including each material AC).  
   Use `inconclusive (data scarcity)` when the claim cannot be verified because required evidence, baselines, or environments were unavailable — not when the test failed.
2. Evidence sampling notes (what was tested, what was not, what could not be tested due to scarcity).  
3. Defect & waste findings that should re-enter DMAIC Analyze/Improve.  
4. Updated residual risk register (include unresolved acquisition backlog items).  
5. Assumption-test results summary (from Prompt 11), if applicable.  
6. Go / conditional-go / no-go recommendation for demo vs production path.  
   **Production go is disallowed** while material areas remain `inconclusive (data scarcity)` unless sponsors explicitly accept that residual risk.

### Lean / DMAIC lens (spine — thin)

**DMAIC focus this stage:** **Control** (+ Measure verification).

In artefact `02_DMAIC_WORKBOOK.md` (short notes only), record:

1. Were Prompt 09 Measure targets actually checked? Pass / fail / inconclusive.  
2. Are Control owners and revisit triggers operating (or only documented)?  
3. Defect & waste findings to re-enter Analyze/Improve.  
4. Evaluation waste check — metrics that do not affect release decisions?

### Control lens rollup (close the spine)

Record Control roll-up inside artefacts `22`/`24`/`25`/`28` as applicable — do not create `control_lens_rollup.md`:

1. Table of artefact `02_DMAIC_WORKBOOK.md` from Prompts **10, 11, 12** (+ summary link to Prompt 09 Control section)  
2. Measure targets: met / missed / inconclusive  
3. Wastes still open after build  
4. Next Discover/Frame loop recommendation (if any)  
5. Control owners for handover (feeds Prompt 13 / DDD stage 16)

### Production readiness & handover (DDD stage 16)

In artefact `28_PRODUCTION_READINESS.md`:

- What is production-ready vs PoC-only  
- Domain / ops / support owners  
- Open ADRs, open ambiguities, residual risks blocking production  
- Handover checklist status

---

## Exit criteria (handoff to Prompt 13)

- [ ] Claims in SCQA/PRD/ADRs/ACs are verified, falsified, partial, untested, or `inconclusive (data scarcity)`.
- [ ] PoC vs production gaps are evidence-based.
- [ ] Residual risks and sponsor decisions (including data-access needs) are explicit.
- [ ] Control owners and revisit triggers are named.
- [ ] Control roll-up is recorded in artefacts `22`/`24`/`25`/`28` (no separate control_lens file).
- [ ] Artefact `28_PRODUCTION_READINESS.md` covers DDD stage 16 handover concerns.
- [ ] artefact `02_DMAIC_WORKBOOK.md` Control focus is complete.

---

## Constraints

- Do not hide failed ADR or AC compliance; record deviations.
- Do not invent production readiness — distinguish demonstrated vs required.
- Do not treat `inconclusive (data scarcity)` as a pass.
- Prefer concrete FP/FN examples over generic quality statements.

---

## Output

Do **not** create a parallel evaluation report tree. Write assurance into the expected artefacts and dirs:

- `submission/artefacts/13_GXP_LIFECYCLE_VALIDATION.md` through `15_QUALITY_RISK_MANAGEMENT.md`
- Threat/abuse: use **package control #4** + `submission/artefacts/16_THREAT_ABUSE_MODEL.md` (repo approach; no team threat prompt)
- `17_PRIVACY_ETHICS.md` through `21_ASSURANCE_CASE.md`
- `22_EVALUATION_SCORECARD.md` through `25_INCIDENT_RECOVERY.md`
- `28_PRODUCTION_READINESS.md`
- Machine-readable results in `submission/evaluation/` and `submission/evidence/` only (required names per `SUBMISSION_EVIDENCE_STANDARD.md`)

See `submission/prompts/PROMPT_MAPPING.md`.
