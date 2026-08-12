# AEGIS specification set

Authoritative build inputs for the agentic app. The master build plan (`../00_plan/MASTER_BUILD_PLAN.md`) holds decisions and rationale; **these files hold what gets implemented.** If the two disagree, the spec wins and the plan is corrected.

## Layer rules

Each file answers exactly one question. Do not merge layers.

| Layer | File(s) | Question answered |
|---|---|---|
| Product | `product/scope.md` | What problem, in and out of scope, which principles bind us |
| Feature | `features/FR-0NN_*.md` | What must the system do — one feature per file |
| Architecture | `../00_plan/MASTER_BUILD_PLAN.md` §2, §5, §7, §20 + challenge artefact 10 (C4) and 11 (ADRs) | Where does code belong |
| Technical design | `api/api_contracts.md`, `api/*.schema.json`, `data/data_model.md`, `data/state_transitions.md` | Exactly how must it behave — payloads, entities, states, validation, errors |
| Cross-cutting | `nfrs.md`, `poc_vs_production.md` | What must hold regardless of feature, and what is not production |
| Testing | `testing/ac_test_plan.md` | Which test proves which acceptance criterion |
| Tasks | `../02_tasks/task-0NN_*.md` | What code needs writing, and which specs to load for it |

Architecture is settled **before** technical design. Contracts do not lock until the architecture review is `pass` or `conditional`.

## ID scheme

`AP-n` architecture principle · `FR-0NN` feature · `BR-0NN` business rule · `AC-FR0NN-NN` acceptance criterion · `TASK-0NN` implementation task · `TC-INJ-###` inject test · `AMB-NN` ambiguity · `PUB-NN` challenge fixture · `INJ-0NN` challenge inject.

Required chain, audited by the traceability validator in both directions:

```
AP → FR → BR → AC → TASK → test → evidence path
```

## Lifecycle

Every capability moves through six stages, defined in full in plan §30.5. Each feature spec records its current stage in its header.

| # | Stage | Output | Exit gate |
|---|---|---|---|
| 1 | Define the spec | Spec v1.0 + BR/AC register rows | Quality checklist passes; thresholds numeric or declared Unknown |
| 2 | Validate and align | Approved spec, reviewer recorded | Second-pair-of-eyes review by the accountable role |
| 3 | Design from the spec | ADR, contracts, data model | Architecture review `pass` or `conditional` |
| 4 | Implement to the spec | Working build, one task at a time | Structural reopen `cleared`; build gates pass |
| 5 | Test against the spec | Verified ACs, evidence, eval results | Release thresholds met; nothing silently skipped |
| 6 | Evolve the spec | Spec vNext | Change class approved; regression green |

Stage 6 returns to stage 1, never to stage 4. Learning found during implementation is written into the spec **before** it is written into the code.

## Review gates

1. **Spec quality review** — second pair of eyes per feature spec, against the checklist below (stage 2).
2. **Architecture review** — `pass` or `conditional` before contracts and the data model lock (stage 3).
3. **Structural reopen** — `cleared` before tasks are cut. A task blocked by an open ambiguity is marked `blocked` and not started (stage 4).
4. **Drift** — an architecture change produces an ADR, never a silent merge (stage 6).

## Spec quality checklist

- [ ] One job per file; the question it answers is stated at the top
- [ ] In scope and out of scope both listed
- [ ] Authority and advisory limits stated — what this feature may never decide
- [ ] Exceptions and error cases included, not just the happy path
- [ ] Acceptance criteria verifiable by a test, phrased so a machine can check them
- [ ] Assumptions separated from open questions
- [ ] Ubiquitous language consistent with `data/RELATIONSHIP_MODEL.csv` and the ontology
- [ ] Every threshold numeric, or a declared Unknown with an owner in `registers/spec_ambiguities.md`
- [ ] Traceability row present: FR → BR → AC → task → test
- [ ] No unmarked orphans in the gap audit
- [ ] Evidence handling states source, authority, effective date and hash treatment

## Status

| Artefact | Stage | Status |
|---|---|---|
| `product/scope.md` | 1 | Authored |
| `features/FEATURE_INDEX.md` | 1 | Authored |
| `features/FR-001` … `FR-014` | 1 — Defined | **All fourteen authored**, awaiting stage 2 validation |
| `api/advisory_nonexecuting.schema.json` | 3 | Authored (team contract, AMB-01) |
| `api/api_contracts.md` | 3 | Authored — locks after architecture review |
| `data/data_model.md` | 3 | Authored — locks after architecture review |
| `data/state_transitions.md` | 3 | Authored — locks after architecture review |
| `nfrs.md` | 1 | Authored — 20 requirements, each with a measurement |
| `poc_vs_production.md` | 1 | Authored — every component labelled |
| `registers/*` | 1 | Authored, including `traceability_gap_audit.md` |
| `testing/ac_test_plan.md` | 5 | Authored for all twelve features, 143 ACs, all statuses `Not started` |

The spec set is **complete**: fourteen features, 128 business rules, 177 acceptance criteria, 35 tasks, no unmapped criterion and no unowned inject. `registers/traceability_gap_audit.md` shows no unmarked gaps.

No feature has passed stage 2, so no implementation task may start under the stage-4 gate. Stage 2 is a human act — a spec drafted with AI assistance cannot approve itself, which is the entire purpose of the gate. Clearing stage 2 for FR-001 is the shortest path to unblocking TASK-008 and TASK-009; TASK-001 through TASK-007 are infrastructure and are not gated on a feature spec.

## Migration

At Phase 0 this tree moves to the new repo as `{NEW_REPO}/specs/` with `product/`, `features/`, `api/`, `data/`, `testing/`, `registers/` and the two cross-cutting files preserved, and `../02_tasks/` becomes `{NEW_REPO}/tasks/`. Both directories are defined in plan §2. Nothing here is challenge evidence; all of it is team-authored.
