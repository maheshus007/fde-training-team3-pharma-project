# M-004 — Retarget app (demo + Taipy)

## Specs to load

- [`../technical/file-migration-map.md`](../technical/file-migration-map.md)
- [`../features/composition-root.md`](../features/composition-root.md)

## Deliverable

Update:

- `submission/app/demo.py`
- `submission/app/taipy_app.py`

Replace bare `import workflow_*` / flat shared imports with `aegis.runtime` (preferred) or `aegis.*` public imports.
Keep `sys.path` insert pointing at `submission/src`.

## Done when

- [ ] No `import workflow_batch|pv|supply` in `submission/app/`
- [ ] Demo still prints AI-disabled advisory JSON
