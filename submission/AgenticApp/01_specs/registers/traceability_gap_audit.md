# Traceability and gap audit

**Question this file answers:** is anything unaccounted for? Run before every stage gate. A blank cell is a finding, not a formatting issue.

## 1. Chain integrity

The chain is: **DoD clause → plan section → spec → business rule → acceptance criterion → test → evidence path**.

| Check | Method | Result at v3.5 |
|---|---|---|
| Every BR has ≥1 verifying AC | `business_rules_register.md` gap audit | Pass — 128 rules, 0 orphans |
| Every AC has a test task | `testing/ac_test_plan.md` | Pass — 177 ACs, 177 mapped, 0 silently skipped |
| Every AC is machine-checkable | Manual read for "appropriate", "reasonable", "as needed" | Pass — 0 subjective criteria |
| Every confidence-gated behaviour has a number or a declared Unknown with an owner | `matching_confidence_checklist.md` | Pass — 0 unmarked |
| Every public fixture maps to a feature | `FEATURE_INDEX.md` coverage check | Pass — 15/15 |
| Every fixture's `response_contract` resolves to a schema | `api/api_contracts.md` §1 | Pass — closed by AMB-01 |
| Every inject has an **owning feature** | `FEATURE_INDEX.md` | Pass — 84/84, after FR-012 was created for the orphaned D07 set |
| Every cited inject ID exists | Checked against `data/injects.json` | Pass — the original index cited several IDs that did not match; all corrected |
| Every task has a spec behind it | `02_tasks/task_index.md` | Pass — 35 tasks, 0 speculative |
| Every NFR has a measurement | `nfrs.md` | Pass — 26/26 |
| Generated text cannot reach a regulated field | FR-013 BR-100, BR-101 | Pass by design — proven per fixture by AC-FR013-01 |
| Every component has a maturity label | `poc_vs_production.md` | Pass |

## 2. DoD coverage map

| DoD clause | Where satisfied | Status |
|---|---|---|
| §1 Problem, baseline, no-AI alternative, stop/pivot thresholds | `product/scope.md`; plan §14, §24.4 | Covered |
| §2 Three workflows, contracts, provenance, abstention, audit | FR-001/002/003; `api/api_contracts.md` | Covered |
| §2 Prohibited actions per workflow | BR-007, BR-011, BR-021…BR-023; `data/data_model.md` §5 | Covered |
| §3 Six reproducible commands | Plan §7 | Covered |
| §3 Locked deps or zero-install stdlib mode | NFR-02; TASK-001 stdlib gate | Covered |
| §3 Requirements → architecture → ADR → code → test → evidence | This file; `traceability.csv` seeded at TASK-001 | Covered |
| §3 Brownfield coexistence, migration, rollback, decommissioning | Plan §12 | Covered |
| §4 Intended use, GxP boundary, records/signatures boundary | Plan §11; `state_transitions.md` §4 | Covered |
| §4 Nine attack classes tested | Plan §9.4; `tests/security/` | Covered |
| §4 Purpose limitation, minimisation, retention, consent/withdrawal, **pseudonymisation**, re-identification, cross-border | BR-012, **BR-012a**, plan §20.4, injects 059–064 | Covered — pseudonymisation closed in v3.5 |
| §4 Prohibited actions fail closed; execution-time authZ | AP-2, AP-9; `state_transitions.md` §2, §6 | Covered |
| §5 Golden, edge, adversarial, subgroup, failure, outage, recovery, regression | Plan §9.4, §25 | Covered — "golden" is satisfied by property graders, since no golden answers ship with the challenge (BS-08) |
| §5 Measurable release thresholds that block | `evals/thresholds.yaml`; plan §9.5 | Covered |
| §5 SLI/SLO, capacity, observability, incident, backup/restore, AI-disabled continuity, retirement | Plan §13, §24; NFR-12, NFR-17 | Covered |
| §5 Token/context budgets, avoided inference, human-review cost, cost per successful task | Plan §24.4; NFR-07, NFR-08 | Covered |
| §6 30 artefacts completed or mapped | Plan §3.3 submission bridge | Covered — reconciliation runs each phase |
| §6 Machine-readable test and eval results | `evidence/tests/`, `evidence/quality-gates/` | Covered |
| §6 Manifest with owner, version, status, hash | Plan §3.3 B-3 | Covered |
| §6 No secrets or personal data | NFR-19 | Covered |
| §6 `check_submission_structure.py --final` passes | Plan §3.3, release gate | Covered |
| §7 Defence: happy, edge, attack, outage, recovery, manual paths | Plan Phase 8 | Covered |
| §7 Prove prohibited actions cannot execute | `data_model.md` §5 + negative tests | Covered |
| §7 Go / conditional-go / pivot / pause / stop recommendation | Plan §14 | Covered |

Every clause maps. Mapping is not evidence — status becomes *proven* only when the referenced test runs green and writes to `evidence/`.

## 3. Known open items, carried deliberately

| Item | Why it is open | When it closes |
|---|---|---|
| Declared Unknowns AMB-05a, 05b, 11, 12 | Need a human with domain authority, not a decision the team can make from the evidence | Human-review panel, Phase 6 |
| FR-004, FR-008 and FR-012 have no public fixture | The challenge supplies none for these behaviours. Scenarios are team-derived from `data/` | Never fully — reported as team-derived rather than fixture-verified |
| Stage-2 spec approval | Requires the accountable role to review. An AI-authored spec that approves itself defeats the gate | Before Phase 1 implementation begins |
| Cosmos Gremlin adapter | Optional cloud path; not required by any fixture | Only if a cloud demonstration is requested |

## 4. Findings closed in v3.5

| Finding | Fix |
|---|---|
| `specs/` and `tasks/` referenced by §30.1, `01_specs/README.md` and TASK-001 but absent from the §2 structure | Added to §2; structure manifest would otherwise have drifted on first commit |
| Pseudonymisation named by DoD §4 with no rule, AC or test anywhere in the spec set | BR-012a + AC-FR002-13 + `tests/security/test_pseudonymisation.py` |
| `poc_vs_production.md` required by plan §30.3 but never authored | Authored |
| No data model or state-transition specs, both core technical-design contracts | `data/data_model.md`, `data/state_transitions.md` authored |
| NFRs scattered across plan §13, §24, §9.5 with no single measurable register | `nfrs.md` authored, 20 rows each with a measurement |
| PUB-12 filed under FR-009 "continuity" although it is a LIMS v1-versus-v2 interface reconciliation | Split into **FR-011**; a spec written under the wrong feature would not have matched the fixture |
| Dimension D07 — injects 045 to 050 — had no owning feature | **FR-012** authored; the injects were mapped to test classes but no feature claimed the behaviour |
| Feature index cited inject IDs that did not exist or meant something else | All IDs verified against `data/injects.json` and corrected across every spec |
