"""Shim — canonical: aegis-sdd/apps/web/main.py."""
from __future__ import annotations

import sys
from pathlib import Path

_SUBMISSION = Path(__file__).resolve().parents[1]
if str(_SUBMISSION) not in sys.path:
    sys.path.insert(0, str(_SUBMISSION))

from src._canon import load_canon  # noqa: E402

_mod = load_canon("aegis_sdd_web_main", "aegis-sdd/apps/web/main.py")

# Taipy binds variables from this module's locals when Gui is built under __main__.
for _name in dir(_mod):
    if _name.startswith("_") and _name not in {"_submit"}:
        continue
    globals()[_name] = getattr(_mod, _name)

PAGES = _mod.PAGES
HOST = _mod.HOST
PORT = _mod.PORT
ack_enabled = _mod.ack_enabled
submit_batch = _mod.submit_batch
submit_pv = _mod.submit_pv
submit_supply = _mod.submit_supply
acknowledge_review = _mod.acknowledge_review
create_gui = _mod.create_gui
run = _mod.run

if __name__ == "__main__":
    from taipy.gui import Gui

    if hasattr(_mod, "prepare_runtime"):
        _mod.prepare_runtime()
    Gui(pages=PAGES).run(host=HOST, port=PORT, use_reloader=False, title="AEGIS HITL")
