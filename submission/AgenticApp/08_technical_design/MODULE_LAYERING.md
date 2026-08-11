# SRS — Module / layering rules (Prompt 08)

Aligns to C4_CODE_SKETCH.

**Product tree (SDD / Cursor-native SDLC scaffold):** `submission/aegis-sdd/`  
**Scoring shims (package `--final`):** keep `submission/src`, `app`, `tests`, `scripts`, `runbooks` as thin re-exports. Do **not** add a second copy of business logic.

Do not invent packages outside this map. Do not create `aegis-sdd` outside `submission/`. No nested `git init` unless explicitly requested.

```text
submission/aegis-sdd/          # product repository (image SDLC layout)
  apps/web/                    # Taipy HITL (FR-F)
  services/api/                # service façade
  services/worker/             # orchestrator
  services/integration/        # adapters (stub / Azure / memory / Gremlin)
  packages/domain/             # engines, ontology, policy_guard
  packages/contracts/          # schema validate
  packages/config/
  packages/observability/      # audit
  packages/test-support/
  tests/                       # unit / contract / integration (copied or run via shim)
  docs/  plans/  quality/  security/  infra/  deploy/  ops/  evidence/  templates/  workshop/

submission/                    # workshop / scoring surface
  src/                         # re-export packages + services (exists today; migrate as tasks land)
  app/                         # re-export apps/web
  tests/                       # package test runner still points here
  scripts/
  runbooks/                    # may symlink ops/runbooks
```

## Enforceable constraints

1. `engines/*` MUST NOT import `adapters.azure_openai` or `adapters.cosmos_gremlin`.  
2. Taipy pages MUST NOT call Azure or Gremlin; only `service.py`.  
3. `service.py` MUST run `contracts.validate` then `policy_guard` before return.  
4. Workflow enum in policy_guard MUST be `supply_options` (fix ADR-AA-012).  
5. Optional HTTP router (if added) MUST be thin: parse JSON → `service.py` → serialize.  
6. Assessment tests MUST pass with Azure packages missing (import adapters lazily).
