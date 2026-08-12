# Feature — Package Boundaries

**Question this file answers:** What packages exist and what is each for?

| Field | Entry |
|---|---|
| Feature ID | MF1 |
| Version / date | 1.0 / 2026-08-12 |

## Actor

Build / architecture (structure change; no end-user UI change required).

## Preconditions

- Current code under flat `submission/src/`.
- Workflows do not call each other (verified).

## Packages in this track

| Package | Responsibility |
|---|---|
| `aegis.shared` | Cross-cutting contracts, policy, gates, finops, reliability, model selection, clinical utility |
| `aegis.batch` | Deterministic batch evidence workflow |
| `aegis.pv` | Deterministic PV intake workflow |
| `aegis.supply` | Deterministic supply options workflow |
| `aegis.runtime` | Composition helpers (mode select, dispatch to one workflow) |

## Explicitly excluded

| Package | Reason |
|---|---|
| `aegis.agents` | Deferred to `submission/specs/` agentic track |

## Acceptance criteria

- [ ] Five packages exist under `submission/src/aegis/`
- [ ] No `agents/` directory created by this track
- [ ] Each package has `__init__.py`
