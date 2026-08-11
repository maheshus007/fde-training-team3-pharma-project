"""T-017: setup/run/test/evaluate/reset name gate; reset is scoped to runtime stores."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from reset import RESET_SUBDIRS, reset_runtime_stores  # noqa: E402


class ScriptNameTests(unittest.TestCase):
    def test_required_script_names_exist(self) -> None:
        names = {path.name.lower() for path in (ROOT / "scripts").glob("*") if path.is_file()}
        for required in ("setup", "run", "test", "evaluate", "reset"):
            self.assertTrue(any(required in name for name in names), required)


class ResetScopeTests(unittest.TestCase):
    def test_reset_deletes_only_runtime_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "keep.json").write_text("{}", encoding="utf-8")
            for name in RESET_SUBDIRS:
                folder = root / name
                folder.mkdir()
                (folder / ".gitkeep").write_text("", encoding="utf-8")
                (folder / "runtime.json").write_text(json.dumps({"x": 1}), encoding="utf-8")
            deleted = reset_runtime_stores(root)
            self.assertEqual(deleted, 4)
            self.assertTrue((root / "keep.json").is_file())
            for name in RESET_SUBDIRS:
                self.assertTrue((root / name / ".gitkeep").is_file())
                self.assertFalse((root / name / "runtime.json").is_file())
