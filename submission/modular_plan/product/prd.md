# PRD — Modular Monolith Restructure

**Question this file answers:** What problem are we solving by modularizing?

| Field | Entry |
|---|---|
| Version / date | 1.0 / 2026-08-12 |
| Audience | Architecture, build, evaluation leads |
| Status | Accepted for implementation |

## Problem

AEGIS-PHARMA submission code is a **flat monolith** (`submission/src/*.py`). Three workflows are logically independent, but nothing enforces boundaries. App/tests use `sys.path` hacks and bare/`src.*` imports. This blocks clean agentic layering and makes accidental coupling likely as the codebase grows.

## Users

| Persona | Need |
|---|---|
| Build / implementation lead | Clear place to put workflow vs shared code |
| Architecture lead | Reviewable dependency rules |
| Evaluation lead | Stable public APIs for tests/graders |
| Future agent track | Composition root + shared kernel to hang assist on |

## Goals

1. Encode existing independence as packages with a hard import rule.
2. Keep one deployable and offline AI-disabled path.
3. Preserve workflow response behaviour and package contract validation.
4. Prepare (but do not implement) space for a later `aegis.agents` package.

## Non-goals

- Splitting into microservices
- Changing advisory/prohibited AI-use boundaries
- Rewriting batch/PV/supply business logic
- Implementing the agent loop (see `submission/specs/`)

## Success metrics

| Metric | Target |
|---|---|
| Workflow cross-imports | 0 (automated) |
| Shared → workflow imports | 0 (automated) |
| Existing unit tests | All pass |
| AI-disabled demo | Runs |
| Deployables | Still 1 process |

## Deliberately omitted

Exact file moves, import tables, package `__init__` exports — see technical and architecture specs.
