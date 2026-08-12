# Spec-Driven Modular Monolith Plan (Validated)

| Field | Value |
|---|---|
| Version / date | 1.1 / 2026-08-12 |
| Status | Accepted (see [`VALIDATION.md`](VALIDATION.md)) |
| Scope root | `submission/` only |
| Framework | PRD → Feature specs → Technical specs → Architecture → Tasks |
| Downstream | [`../../specs/`](../../specs/) agentic track (after this completes) |

## Locked decisions

1. **Architecture style:** modular monolith — one deployable process (CLI / Taipy / tests).
2. **Packages:** `aegis.shared`, `aegis.batch`, `aegis.pv`, `aegis.supply`, `aegis.runtime`.
3. **Not in this track:** `aegis.agents` (V-FIX-03).
4. **No shims:** delete flat `submission/src/workflow_*.py` etc.; update all call sites.
5. **Signatures unchanged:** `reconcile_batch`, `build_pv_response`, `build_supply_response`.
6. **Composition root:** `aegis.runtime` preferred for app entry (V-FIX-01).
7. **Enforcement:** AST/import boundary test — not optional.
8. **ADR:** ADR-013 in `submission/artefacts/11_ADR_REGISTER.md`.

## Dependency rule (non-negotiable)

| From | May import | Must not import |
|---|---|---|
| `batch` / `pv` / `supply` | `shared` | each other, `runtime`, `app` |
| `shared` | stdlib / local shared only | workflows, `runtime`, `app` |
| `runtime` | `shared` + one/more workflows | `app` |
| `app` | `runtime` (preferred) or public workflow/`shared` exports | deep module internals |

## Spec index

| Layer | Path |
|---|---|
| PRD | [`../product/prd.md`](../product/prd.md) |
| Features | [`../features/`](../features/) |
| Technical | [`../technical/`](../technical/) |
| Architecture | [`../architecture/modular-system.md`](../architecture/modular-system.md) |
| Tasks | [`../tasks/`](../tasks/) |

## Implementation order

```
M-001 package skeleton + file move
  → M-002 spec sign-off
  → M-003 runtime composition helpers
  → M-004 retarget app (demo, taipy)
  → M-005 retarget unit tests
  → M-006 retarget scripts + graders
  → M-007 boundary test
  → M-008 ADR-013 + C4 note
  → M-009 verify tests + AI-disabled demo
```

## Out of scope

- Microservices / HTTP between workflows
- Rewriting workflow business logic
- Next.js dashboard refactor
- Agentic loop / tool gateway / envelope (see `submission/specs/`)
- Edits outside `submission/`

## Success criteria

- Package ownership clear for batch, PV, supply, shared, runtime
- Zero workflow↔workflow and shared→workflow imports (test-enforced)
- Existing contract / prohibited-action / auth / tool-trust tests pass
- `python submission/app/demo.py --ai-disabled` works
- Single deployable preserved
