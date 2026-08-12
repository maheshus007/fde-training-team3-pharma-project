# Technical Spec — Dependency Rules

**Question this file answers:** Exactly which imports are legal?

| Field | Entry |
|---|---|
| Spec ID | MT3 |
| Version / date | 1.0 / 2026-08-12 |

## Allowed import matrix

| Importer \ Importee | shared | batch | pv | supply | runtime |
|---|---|---|---|---|---|
| shared | yes | no | no | no | no |
| batch | yes | yes* | no | no | no |
| pv | yes | no | yes* | no | no |
| supply | yes | no | no | yes* | no |
| runtime | yes | yes | yes | yes | yes* |

\* same-package relative imports only.

## Forbidden patterns (fail boundary test)

```python
# inside aegis/batch/**
import aegis.pv
from aegis.supply import ...

# inside aegis/shared/**
from aegis.batch.workflow import reconcile_batch
import aegis.runtime

# inside aegis/batch|pv|supply/**
import aegis.runtime
```

## App layer

`submission/app/**` is outside `aegis` and may import `aegis.runtime`, `aegis.batch`, `aegis.pv`, `aegis.supply`, `aegis.shared`.

## Detection

Parse each `submission/src/aegis/**/*.py` with `ast`; collect `Import` / `ImportFrom` modules starting with `aegis.`; apply matrix.
