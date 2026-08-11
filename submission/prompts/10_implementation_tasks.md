> **V3 adaptation:** Team method prompt. Do not edit hashed prompts/PROMPT_LIBRARY.md. Write all outputs under submission/ only. Obey package control prompts, GxP fail-closed contracts, and prohibited-action boundaries. See submission/prompts/PROMPT_MAPPING.md.
# Prompt 10 — Implementation Tasks

**Lifecycle stage:** Spec-Driven Development — Implementation Tasks  
**Framework derived:** Spec-Driven Development (executable task units for AI agents)  
**Core question:** What code needs writing — as numbered, handoff-ready tasks?  
**Prerequisites:** Prompt 08 technical design + traceability; Prompt 09 Lean/DMAIC build constraints.  
**Primary output type:** Numbered task files (one task per file) + ordered execution plan.

---

## Intent

Break the governed slice into **small, independently reviewable tasks** an agent can execute one at a time. Each task points at the exact specs it needs — never a 200-page blob.

SDD: tasks are numbered units; retrieval pulls only the relevant feature + technical + architecture files.

---

## Entry criteria

- Technical contracts and traceability matrix exist.  
- Architecture review from Prompt 07 is `pass` or `conditional` (not `fail`); conditional items are reflected in tasks or residual risk.  
- Prompt 09 structural reopen gate in artefacts `10`/`11` is **`cleared`** (reopen of 06–08 completed if it was required).  
- Lean must-fix / Measure-first / assumption-test priorities exist.  
- Out-of-scope remains explicit.
- Specs are available under `submission/artefacts/` (and `submission/evaluation/` contracts) so work units can cite repo paths.
- AC register from Prompt 05 is available so test tasks can be mapped 1:1.

---

## Produce

### A. Task index / execution order

Ordered list of tasks with dependencies. Prioritize:

1. Assumption tests / Measure instrumentation (if hypothesis/provisional or Lean Measure-first)  
2. Foundational contracts (schema, error envelope, health)  
3. Features in dependency order  
4. **Tests mapped to ACs** — required: every in-scope AC has at least one test under `submission/tests/` (or an explicit deferral with risk). Record the AC→test map in artefact `09`.  
5. Docs/deployment only as needed for the slice

Record the AC to test mapping inside `submission/artefacts/09_REQUIREMENTS_TRACEABILITY.md` (implement tests under `submission/tests/` — no separate plan file):

| AC ID | Test task ID(s) | Test type | Status |
|-------|-----------------|-----------|--------|
| AC-00N | task-00N | unit/integration/e2e | planned |

### B. Task units (describe in artefacts `09` / `28`; do **not** create `task-00N.md` files)

Each task must include:

1. **Goal** — one sentence  
2. **Specs to load** — exact paths (feature file, API section, ADR IDs, C4 view, module rules)  
3. **Out of scope for this task**  
4. **Implementation steps** — checklist  
5. **Acceptance checks** — which AC/BR/NFR this task proves  
6. **Test expectations** — what tests to add/update  
7. **Done when** — binary exit criteria  

### C. Mapping

- Task → FR → AC → contract rows from the traceability matrix  
- Tasks that are blocked on open ambiguities must be marked `blocked` (do not hand to the agent)

### Lean / DMAIC lens (spine — thin)

**DMAIC focus this stage:** **Improve** sequencing — turn Prompt 09 constraints into task order.

In artefact `02_DMAIC_WORKBOOK.md` (short notes only), record:

1. Which tasks implement Measure-first / must-fix-before-build items?  
2. Which tasks are deferred because they are Overproduction or Model waste?  
3. How assumption-test tasks reduce Unknown baselines?  
4. Any blocked tasks that are really Waiting on evidence acquisition?

---

## Exit criteria (handoff to Prompt 11)

- [ ] Architecture review is `pass` or `conditional` with conditions mapped into tasks/risks.  
- [ ] Prompt 09 structural reopen gate is `cleared`.  
- [ ] Tasks cover the minimum governed slice end to end.  
- [ ] Artefact `09` maps every in-scope AC to a `submission/tests/` case or explicit deferral.  
- [ ] Each task lists the only specs an agent should read.  
- [ ] Lean/assumption-test priorities appear first when required.  
- [ ] Blocked tasks are explicit; no silent guessing left as a task.  
- [ ] One task ≈ one agent run (reviewable in one sitting).  
- [ ] No separate task-tree files; AC→test mapping is in artefact `09` and tests live under `submission/tests/`.  
- [ ] artefact `02_DMAIC_WORKBOOK.md` is complete.

---

## Constraints

- Do not implement code in this prompt.  
- Do not create mega-tasks (“build the whole checkout”). Split them.  
- Do not reference specs that do not exist yet.  
- Do not re-run full Prompt 09 — apply its build constraints.

---

## Output

Do **not** create a `tasks/` tree. Capture implementation sequencing inside:

- Traceability/test plan rows in `submission/artefacts/09_REQUIREMENTS_TRACEABILITY.md`
- Production/build readiness notes in `submission/artefacts/28_PRODUCTION_READINESS.md` as needed
- Create actual test stubs under `submission/tests/` (package-expected dir) mapped to ACs — no extra task markdown files

See `submission/prompts/PROMPT_MAPPING.md`.
