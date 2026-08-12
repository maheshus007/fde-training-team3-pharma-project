# M-001 — Package skeleton and file move

## Specs to load

- [`../technical/package-layout.md`](../technical/package-layout.md)
- [`../technical/file-migration-map.md`](../technical/file-migration-map.md)
- [`../features/package-boundaries.md`](../features/package-boundaries.md)
- [`../features/shared-kernel.md`](../features/shared-kernel.md)
- [`../features/workflow-packages.md`](../features/workflow-packages.md)

## Deliverable

1. Create `submission/src/aegis/{shared,batch,pv,supply,runtime}/` with `__init__.py` files.
2. Move modules per migration map; re-export public APIs from package `__init__.py`.
3. Delete old flat `submission/src/*.py` modules (no shims).
4. Do **not** create `aegis/agents/`.

## Done when

- [ ] Target tree matches MT1
- [ ] Old flat workflow/shared modules gone
- [ ] Public signatures unchanged
