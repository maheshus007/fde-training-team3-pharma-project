# AEGIS-PHARMA app

## CLI (stdlib — assessed mode)

```powershell
python submission\app\demo.py
python submission\app\demo.py --ai-disabled
```

## Taipy UI (optional)

Python 3.14 cannot install `taipy-gui`'s pinned `pandas<=2.2.2`. Use `--no-deps` then the rest of this file:

```powershell
python -m pip install --no-deps taipy-gui==4.0.2
python -m pip install -r submission\app\requirements-ui.txt
cd submission\app
python taipy_app.py
```

Opens http://127.0.0.1:5000 with pages for Overview, Batch, PV, Supply, and Gates.  
Workflow outputs render as clickable trees (no raw JSON). Defaults match the defence demo IDs (`NCB204-B24071`, `PV-1001/1014/1009`, `NCS310-S26033`).

Assessed offline mode (`setup` / `run` / `test` / `evaluate`) does **not** require Taipy.
