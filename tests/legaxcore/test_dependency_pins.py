import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools/check_protocol_dependencies.py"
spec = importlib.util.spec_from_file_location("legax_dependency_check", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class DependencyPinsTest(unittest.TestCase):
    def test_real_baseline_matches_lockfile(self):
        self.assertEqual(checker.validate(ROOT), [])

    def test_detects_version_drift(self):
        pins = json.loads((ROOT / "legaxcore/dependency-pins.json").read_text(encoding="utf-8"))
        lock = json.loads((ROOT / "composer.lock").read_text(encoding="utf-8"))
        composer = json.loads((ROOT / "composer.json").read_text(encoding="utf-8"))
        target = "pocketmine/bedrock-protocol"
        for pkg in lock["packages"]:
            if pkg["name"] == target:
                pkg["version"] = "999.0.0"
                break
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "legaxcore").mkdir()
            (root / "legaxcore/dependency-pins.json").write_text(json.dumps(pins), encoding="utf-8")
            (root / "composer.lock").write_text(json.dumps(lock), encoding="utf-8")
            (root / "composer.json").write_text(json.dumps(composer), encoding="utf-8")
            self.assertTrue(any("versao do lock" in e for e in checker.validate(root)))


if __name__ == "__main__":
    unittest.main()
