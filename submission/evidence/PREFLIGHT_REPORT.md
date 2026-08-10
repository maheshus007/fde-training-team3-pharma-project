# Preflight Report — Project AEGIS-PHARMA (Team 3)

| Field | Entry |
|---|---|
| Team | Team 3 — Project AEGIS-PHARMA / NovaCura Therapeutics Group |
| Date | 2026-08-10 |
| Platform | Windows 10 (build 10.0.19045) |
| Runtime | Python 3.14.6 |
| Package mode | Offline challenge package (`PACKAGE_SCOPE_AND_ASSUMPTIONS.md`) |
| Status | Preflight complete; environment findings recorded without modifying challenge tools |

## 1. Commands executed

| Command | Result | Observation |
|---|---|---|
| `python --version` | Python 3.14.6 | Meets package assumption of Python 3.10+ (`PACKAGE_SCOPE_AND_ASSUMPTIONS.md`) |
| `python tools/check_submission_structure.py --scaffold` | PASS | Scaffold directories under `submission/` accepted |
| `python starter/baseline_diagnostics.py` | Completed with findings | Four deliberate challenge signals surfaced (see section 3) |
| `python run_capstone.py --check` | Failed | `UnicodeDecodeError` in `tools/verify_package.py` (see section 2) |

## 2. Package verification failure (`run_capstone.py --check`)

Challenge verification aborted while `tools/verify_package.py` attempted to read a non-UTF-8 file:

```
File "...\tools\verify_package.py", line 108, in <module>
  for ref in pat.findall(p.read_text(encoding='utf-8')):
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd5 in position 37: invalid continuation byte
```

Interpretation:

- Fact: package check cannot complete on this host because at least one referenced path is not valid UTF-8 under the verifier's `encoding='utf-8'` read.
- Root-cause inventory (participant scan via `submission/scripts/_find_bad_encoding.py`, read-only): 14 AppleDouble resource-fork sidecar files under `prompts/` named `._*.md` (e.g. `prompts/._01_discovery.md`, `prompts/._PROMPT_LIBRARY.md`) fail UTF-8 decode. Challenge markdown under `prompts/*.md` without the `._` prefix remains readable.
- Boundary: Team 3 does **not** modify challenge tools under `tools/`, `starter/`, or other immutable package areas (`PACKAGE_SCOPE_AND_ASSUMPTIONS.md` immutable/writable rules; workspace rule to work only under `submission/`). Sidecars are not deleted from the challenge tree.
- Treatment: recorded as an environment/package finding. Participant work proceeds using scaffold checks, baseline diagnostics, local evidence inspection, public contract tests (`python tools/test_contracts.py` — PASS on 2026-08-10), and offline deterministic development under `submission/`.
- Follow-up assumption logged as A-001 in `submission/artefacts/ASSUMPTIONS_AND_DECISION_LOG.md`.
- Related public check: `python tools/test_contracts.py` passed all six positive/negative workflow contract fixtures independently of `run_capstone.py --check`.

## 3. Baseline diagnostics findings

`python starter/baseline_diagnostics.py` reported:

| Finding | Linked inject / evidence | Implication for AEGIS design |
|---|---|---|
| Stale entitlement cache | INJ-067; `data/users_entitlements.csv`; `data/access_cache.csv` | Authorization must be checked at execution time; cached entitlements are not trusted |
| Model hash mismatch | INJ-070; `data/model_registry.csv`; `data/model_artifacts.csv` | Only registry-approved model hashes may load; mismatch forces abstain / offline path |
| Unapproved unit mapping | INJ-024; `data/lab_results.csv`; `data/interface_mappings.csv` | Unit conversion requires approved mapping and provenance; silent conversion is prohibited |
| Untrusted knowledge present | INJ-065; `data/knowledge_catalog.csv`; supplier deviation material | Retrieved documents are untrusted data until authority, signature/hash and applicability are verified |

Diagnostics note: "4 obvious findings surfaced. This is not a complete assessment." Team 3 treats these as starting controls, not an exhaustive risk inventory.

## 4. Offline package mode assumptions

From `PACKAGE_SCOPE_AND_ASSUMPTIONS.md`:

1. Fully synthetic and offline-capable; no cloud key, database, internet or instructor service required to inspect evidence or run public fixtures.
2. Challenge-only package: no reference solution, answer key or golden architecture.
3. All 84 injects are disclosed from the start (`case/INTEGRATED_CASE.md` section 7).
4. Deliberate ambiguity (conflicting identifiers, timestamps, authorities, quality states) must not be cleaned without preserving source evidence and recording governed resolution.
5. Participant stack freedom is allowed if locked dependencies, offline/mocked execution, reset/test commands, evidence export and AI-disabled continuity are provided.
6. Writable area is exclusively `submission/`; `case/`, `data/`, `knowledge/`, `source_documents/`, `evaluation/`, `requirements/`, `starter/` and `templates/` are immutable challenge evidence.

## 5. Scoring and regulatory boundaries

Understood from `requirements/SCORING_MODEL.md`, `case/INTEGRATED_CASE.md` and `data/ai_use_boundaries.csv`:

- Scoring total is 180 points across 17 areas; hard gates apply independently of numeric score.
- Work product for scoring lives under `submission/` only.
- Hard-gate prohibitions include autonomous batch release/reject/reprocess/recall, final PV seriousness/causality/expectedness/reportability/signal confirmation, and autonomous reserve/allocate/ship/recall actions.
- Mandatory workflows remain advisory/supportive:
  - Workflow A: batch evidence reconciliation without disposition (`case/INTEGRATED_CASE.md` §4; INJ-006).
  - Workflow B: PV intake and signal support without final safety decisions.
  - Workflow C: supply options without allocate/ship/recall.
- Evidence provenance, authority, effective date, auditability and AI-disabled continuity are non-negotiable (`PACKAGE_SCOPE_AND_ASSUMPTIONS.md`; INJ-082; `data/continuity_requirements.csv`).

## 6. Preflight exit criteria

| Criterion | Status |
|---|---|
| Offline package inspectable locally | Met |
| Submission scaffold accepted | Met (`--scaffold` PASS) |
| Baseline challenge conditions known | Met (four diagnostics findings recorded) |
| Package hash/check tooling failure documented without altering challenge code | Met |
| Team roles, working agreements and Phase 1 discovery artefacts initiated | Met (see `submission/artefacts/`) |

## 7. Residual preflight gaps

| Gap | Impact | Mitigation |
|---|---|---|
| Full `run_capstone.py --check` cannot finish on this Windows/Python 3.14 host due to non-UTF8 decode | Package integrity scan incomplete | Continue with local hash export under `submission/evidence/` when implementation begins; do not patch `tools/verify_package.py` |
| Baseline diagnostics are not a complete assessment | Residual inject risk remains | Systematic inject mapping in later artefacts (05–21) and prohibited-action tests |

---

Prepared by: Team 3 Build / Evaluation leads  
Independent review: GxP/quality lead, Security/privacy lead
