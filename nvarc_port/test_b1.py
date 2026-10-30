"""CPU launch-boundary checks for B1; no model, GPU, or upstream module execution."""
import ast
import base64
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("build_b1", ROOT / "build_b1.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


class B1Tests(unittest.TestCase):
    def test_only_launch_environment_changes(self):
        before = (ROOT / b.BASE_NAME).read_bytes()
        base = json.loads(before)
        nb = b.build_b1()
        self.assertEqual(nb["cells"][0], base["cells"][0])
        self.assertEqual(nb["metadata"]["kaggle"], base["metadata"]["kaggle"])
        source = "".join(nb["cells"][1]["source"])
        self.assertEqual(source.replace(b.NEW_LAUNCH, b.OLD_LAUNCH, 1),
                         "".join(base["cells"][1]["source"]))
        self.assertEqual((ROOT / b.BASE_NAME).read_bytes(), before)

    def test_exact_bundle_and_full_rate_preserved(self):
        nb = b.build_b1()
        tree = ast.parse("".join(nb["cells"][1]["source"]))
        value = next(ast.literal_eval(n.value) for n in tree.body
                     if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)
                     and n.targets[0].id == "bundle")
        with zipfile.ZipFile(io.BytesIO(base64.b64decode(value))) as z:
            for name in z.namelist():
                self.assertEqual(z.read(name), (ROOT / name).read_bytes())
            self.assertEqual(hashlib.sha256(z.read("driver.py")).hexdigest(), b.DRIVER_SHA256)
            author = json.loads(z.read("vendor/author-v10.ipynb"))
        solver = next("".join(c["source"]) for c in author["cells"]
                      if "".join(c["source"]).startswith("%%writefile arc_solver.py"))
        self.assertEqual(solver.count("learning_rate=5e-5,"), 1)
        self.assertIn("seed=hash(bk) % 1024**2", solver)

    def test_generated_launch_pins_driver_and_spawned_workers(self):
        # Execute the actual generated launch boundary against a tiny CPU probe.
        # A different inherited parent seed catches a missing/late env override.
        source = "".join(b.build_b1()["cells"][1]["source"])
        tail = ast.Module(body=ast.parse(source).body[-3:], type_ignores=[])
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            result = root / "result.json"
            probe = root / "probe.py"
            probe.write_text(
                "import json, multiprocessing as mp, os, pathlib, sys\n"
                "def worker(q):\n"
                "    q.put({'seed':os.environ.get('PYTHONHASHSEED'),'hash':hash('B1-boundary-probe')})\n"
                "if __name__ == '__main__':\n"
                "    ctx=mp.get_context('spawn'); q=ctx.Queue(); p=ctx.Process(target=worker,args=(q,))\n"
                "    p.start(); child=q.get(timeout=15); p.join(timeout=15)\n"
                "    assert p.exitcode == 0\n"
                "    pathlib.Path(sys.argv[1]).write_text(json.dumps({'seed':os.environ.get('PYTHONHASHSEED'),'hash':hash('B1-boundary-probe'),'worker':child}))\n"
            )
            with patch.dict(os.environ, {"PYTHONHASHSEED": "999"}):
                exec(compile(tail, "B1-launch-boundary", "exec"),
                     {"os": os, "subprocess": subprocess,
                      "command": [sys.executable, str(probe), str(result)]})
            got = json.loads(result.read_text())
            reference = subprocess.check_output(
                [sys.executable, "-c", "print(hash('B1-boundary-probe'))"],
                env={**os.environ, "PYTHONHASHSEED": "42"}, text=True)
            self.assertEqual(got["seed"], "42")
            self.assertEqual(got["worker"]["seed"], "42")
            self.assertEqual(got["hash"], int(reference))
            self.assertEqual(got["worker"]["hash"], got["hash"])

    def test_changed_baseline_is_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            changed = Path(t) / "base.ipynb"
            changed.write_bytes((ROOT / b.BASE_NAME).read_bytes() + b" ")
            with self.assertRaises(ValueError):
                b.build_b1(changed)


if __name__ == "__main__":
    unittest.main()
