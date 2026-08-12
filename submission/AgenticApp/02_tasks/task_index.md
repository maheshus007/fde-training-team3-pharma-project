# Task index

Each task is one sitting's work with an explicit spec list. Load only the listed specs — that is the point of having them.

A task is `blocked` if an ambiguity affecting it is open. Blocked tasks are not started.

## Phase 0 — Scaffold and governance

| Task | Goal | Specs to load | Depends on | Status |
|---|---|---|---|---|
| **TASK-001** | Repo scaffold, structure manifest, stdlib import gate, interpreter guard | plan §2, §4; `01_specs/README.md` | — | Ready |
| **TASK-002** | Fixture copy-set generator, hash verification, provenance record | plan §3.2; AMB-09 | TASK-001 | Ready |
| **TASK-003** | Canonical serialisation and derived identifiers | plan §28; AMB-03, AMB-04 | TASK-001 | Ready |
| **TASK-004** | Contract package: four challenge schemas, advisory contract, validator, deny-list | `01_specs/api/api_contracts.md`; AMB-01 | TASK-001, TASK-003 | Ready |
| **TASK-005** | Kernel: request lifecycle, execution-time authorisation, audit trail | plan §7, §11; AP-2 | TASK-003, TASK-004 | Ready |
| **TASK-006** | Six CLI commands, runtime modes, `ai_disabled` path | plan §8, §4 | TASK-005 | Ready |
| **TASK-007** | Evidence item builder with provenance and source-hash integrity | `01_specs/api/api_contracts.md` §3; AMB-02 | TASK-004 | Ready |

**Phase 0 exit:** clean clone runs `python -m aegis test` offline with zero installs; contract, deny-list, determinism and copy-set tests green.

## Phase 1 — Ontology, graph, Workflow A

| Task | Goal | Specs to load | Depends on | Status |
|---|---|---|---|---|
| **TASK-008** | Ontology: units, terminology versions, identity tiers, temporal model, trust status | `01_specs/features/FR-001` §5; plan §5.2, §29.1, §29.5 | TASK-007 | Ready |
| **TASK-009** | Batch engine: contradictions, gaps, abstentions, `readiness_state` | `01_specs/features/FR-001` | TASK-008 | Ready |
| **TASK-010** | Untrusted-document handling and instruction detection | FR-001 BR-009; plan §5.4 | TASK-008 | Ready |
| **TASK-015** | Bounded graph projection with provenance and forbidden-edge guard | plan §5.3, §5.4, §29.4 | TASK-008 | Ready |

## Phase 2–3 — Gates and Workflows B, C

| Task | Goal | Specs to load | Depends on | Status |
|---|---|---|---|---|
| **TASK-011** | Duplicate candidate engine with fixed strategy and scores | `01_specs/registers/matching_confidence_checklist.md` §2; FR-002 BR-014 | TASK-008 | Ready |
| **TASK-012** | PV engine: source facts, clocks, terminology, listedness | `01_specs/features/FR-002` | TASK-011 | Ready |
| **TASK-013** | Privacy and purpose gates: consent, residency, DSR versus hold, sensitive segments, per-purpose pseudonymisation | FR-002 BR-012/012a/017; `01_specs/data/data_model.md` §1; plan §23 | TASK-005 | Ready |
| **TASK-014** | Supply engine: options, constraints, holds, approvals | `01_specs/features/FR-003` | TASK-015 | Ready |
| **TASK-016** | Checkpoint freshness and idempotent replay | FR-003 BR-030; plan §20.4 | TASK-006 | Ready |

| **TASK-017** | Interface contract reconciliation: version resolution, UCUM validation, approved-mapping register | `01_specs/features/FR-011` | TASK-008 | Ready |
| **TASK-018** | Clinical protocol applicability: site approval precedence, reference-range contradictions | `01_specs/features/FR-010` | TASK-008 | Ready |
| **TASK-019** | Regulatory records: identity conflict, labelling divergence, commitments, sequence gaps | `01_specs/features/FR-012` | TASK-008 | Ready |

## Phase 4 — Orchestration and continuity

| Task | Goal | Specs to load | Depends on | Status |
|---|---|---|---|---|
| **TASK-020** | `OrchestratorPort`, declared step graph, stdlib runner, budgets | `01_specs/features/FR-006`; `01_specs/data/state_transitions.md` §3; plan §20 | TASK-016 | Ready |
| **TASK-021** | LangGraph adapter with byte-parity proof against the stdlib runner | FR-006 BR-056; plan §20.2 | TASK-020 | Ready |
| **TASK-022** | Continuity: outage tolerance reading, substitution refusal, kill switch, manual runbooks | `01_specs/features/FR-009` | TASK-006 | Ready |
| **TASK-023** | Tool manifest signing and verification at execution time | FR-005 BR-048a | TASK-005 | Ready |

## Phase 5–6 — Console, FinOps, evals and compliance

| Task | Goal | Specs to load | Depends on | Status |
|---|---|---|---|---|
| **TASK-024** | Advisory API surface for the console; no rule below the API | `01_specs/api/api_contracts.md`; FR-008 BR-064 | TASK-020 | Ready |
| **TASK-025** | Next.js console: four core screens, forced evidence view, segregation of duties | `01_specs/features/FR-008`; `../nfrs.md` NFR-14, NFR-15 | TASK-024 | Ready |
| **TASK-026** | FinOps: token accounting, wallet ceilings, cost per successful task, missing-cost gaps | `01_specs/features/FR-007` | TASK-020 | Ready |
| **TASK-027** | Eval harness: datasets, property and trajectory graders, thresholds | plan §25; `evals/thresholds.yaml` | TASK-009, TASK-012, TASK-014 | Ready |
| **TASK-028** | Compliance tripwires: EU AI Act and ISO 42001 control map as executable checks | plan §22, §23 | TASK-027 | Ready |
| **TASK-029** | Inject fan-out: remaining coverage rows, evidence export, submission bridge | plan §3.3, §15 | TASK-027 | Ready |

## Azure OpenAI advisory layer and evidence store

| Task | Goal | Specs to load | Depends on | Status |
|---|---|---|---|---|
| **TASK-030** | `AzureOpenAIAdapter` behind `InferencePort`: managed identity, pinned deployment and version, residency pre-check, filter capture | `01_specs/features/FR-013`; plan §34.4 | TASK-020, TASK-033 | Ready |
| **TASK-031** | Output guard G-1…G-5 with rejection recording | FR-013 BR-102/103/104; plan §34.3 | TASK-004 | Ready |
| **TASK-032** | Cassette record-and-replay, plus the deterministic groundedness grader | FR-013 BR-110; `../nfrs.md` NFR-21, NFR-22 | TASK-030 | Ready |
| **TASK-033** | Evidence store: append-only chain writer, verifier, retrieval command | `01_specs/features/FR-014`; plan §35 | TASK-005 | Ready |
| **TASK-034** | Retention and hold engine: 90-day prompt-log expiry, live hold check, expiry as an event | FR-014 BR-119/121/122 | TASK-033, TASK-013 | Ready |
| **TASK-035** | Azure Blob WORM adapter for `cloud` mode | FR-014 BR-117; plan §35.4 | TASK-033 | Ready |

TASK-033 is a dependency of TASK-030 rather than the reverse: the store must exist before anything is allowed to call a model, because a call with nowhere to record it is a call this system does not make (BR-116).

All fourteen features are authored, so every task above has a spec behind it. Tasks remain gated on stage-2 approval of the feature they implement.

## Working agreement

One task per sitting. Write the failing test first, from the acceptance criteria — not from the implementation you intend to write. Update `01_specs/testing/ac_test_plan.md` and the inject coverage row before closing the task. The AI-change record is generated by the session hooks; review it rather than write it.
