# TASK-001 — Repo scaffold, structure manifest and build gates

**Goal:** create the new repository skeleton so that every later task lands in a place that already exists, and so the two constraints everything else depends on — stdlib-only core and a pinned interpreter — are enforced from the first commit rather than asserted later.

## Specs to load

`00_plan/MASTER_BUILD_PLAN.md` §2 (structure), §4 (runtime modes and dependency policy) · `01_specs/README.md` · `01_specs/product/scope.md` (AP-5, AP-6).

Nothing else. Do not read the feature specs for this task.

## Out of scope

Any domain logic. Any workflow engine. Any dependency install. The Cursor hooks and `mcp.json` (TASK-001b, cut separately once the repo exists).

## Steps

1. Create `aegis-sdd` at the location in plan §19 decision 1, outside the challenge package.
2. Create the directory tree from plan §2 exactly, with `.gitkeep` in otherwise empty directories.
3. Write root files: `README.md`, `REPO_MAP.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`, `.env.example` (names only), `LICENSE`, `.gitignore`.
4. Generate `STRUCTURE_MANIFEST.json` from the tree — generated, never hand-edited.
5. Implement the **stdlib import gate** in `quality/static-analysis/`: walk `packages/`, parse each module with `ast`, and fail on any import outside the standard library or the deny-list `langgraph, langchain, redis, mcp, fastapi, httpx, requests, networkx, rdflib`.
6. Implement the **interpreter guard**: refuse to run outside CPython ≥ 3.11, < 3.14, with a clear message naming the detected version.
7. Implement the **banned-nondeterminism gate**: fail if `packages/` references `uuid4`, `random`, `time.time`, or `datetime.now`.
8. Copy the plan into `plans/active/`, `01_specs/` into `specs/` and `02_tasks/` into `tasks/` — all three defined in plan §2.

## Acceptance checks

- The tree matches plan §2; `STRUCTURE_MANIFEST.json` regenerates identically on a second run.
- Adding `import requests` to any module under `packages/` fails the gate, with the offending file and line named.
- Adding `uuid4()` to a module under `packages/` fails the nondeterminism gate.
- Running under Python 3.10 exits non-zero with the version message; running under 3.11 and 3.12 succeeds.
- No file contains a credential, token or real hostname.

## Test expectations

`quality/static-analysis/test_no_third_party.py` — positive and negative cases, including a deliberately violating fixture module.
`tests/unit/test_setup_guard.py` — version boundary cases.
`tests/unit/test_structure_manifest.py` — regeneration is stable.

## Done when

A clean clone runs the gates offline with zero installs, all three gate tests pass, and `git status` shows no untracked generated files.
