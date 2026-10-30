"""One actual synthetic training check, <=600s carrier budget, no decoding."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time

import driver

ROOT = Path(__file__).resolve().parent


def instrument(source):
    if source.count("learning_rate=0.0,") != 1 or "learning_rate=5e-5," in source:
        raise ValueError("Probe must use guarded Z solver")
    source = driver.replace_once(source,
        "from peft import get_peft_model_state_dict, set_peft_model_state_dict",
        "from peft import get_peft_model_state_dict, set_peft_model_state_dict\nfrom zero_update_probe_support import adapter_receipt, finish_receipt")
    source = driver.replace_once(source, "        model = FastLanguageModel.for_training(model)",
        "        zero_reset_receipt = adapter_receipt(model, default_weights, 'after_reset')\n        model = FastLanguageModel.for_training(model)")
    source = driver.replace_once(source, "            del trainer",
        "            zero_receipt = finish_receipt(model, default_weights, trainer, stats, zero_reset_receipt)\n"
        "            with open(os.environ['NVARC_ZERO_AUDIT'], 'w') as audit_file:\n"
        "                __import__('json').dump(zero_receipt, audit_file, indent=2)\n"
        "            return  # Probe ends after real training; no decoding or submission file.\n")
    compile(source, "arc_solver.py", "exec")
    return source


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--end-time", required=True, type=float)
    args = p.parse_args()
    if os.environ.get("KAGGLE_IS_COMPETITION_RERUN", "").lower() in ("1", "true"):
        raise RuntimeError("Engineering check prohibited in competition rerun")
    if os.environ.get("PYTHONHASHSEED") != "42":
        raise RuntimeError("Probe interpreter must start with hash42")
    if not 0 < args.end_time - time.time() <= 600:
        raise RuntimeError("Expired or excessive engineering budget")
    model = driver.resolve_input(None, "/kaggle/input", "**/qwen3_4b_grids15_sft139/transformers/bfloat16/1")
    dep = driver.resolve_input(None, "/kaggle/usr/lib/notebooks", "sorokin/pip_install_unsloth_flash_patch")
    provenance = driver.preflight(model, dep)
    challenge, tasks, manifest = driver.smoke_input()
    if len(tasks) != 1:
        raise RuntimeError("Probe requires exactly one frozen synthetic task")
    work = driver.prepare("/kaggle/working/nvarc-zero-check-runtime")
    solver_path = work / "arc_solver.py"
    official_source = solver_path.read_text()
    probe_source = instrument(official_source)
    solver_path.write_text(probe_source)
    shutil.copyfile(ROOT / "zero_update_probe_support.py", work / "zero_update_probe_support.py")
    (work / "status").mkdir()
    (work / "outputs").mkdir()
    receipt_path = work / "training-invariant.json"
    worker = work / "probe_worker.py"
    worker.write_text("import os\nos.environ['CUDA_VISIBLE_DEVICES']='0'\n"
                      "import torch\ntorch.set_default_device('cpu')\n"
                      "from queue import Queue\nfrom arc_solver import worker\n"
                      "if __name__ == '__main__':\n"
                      f"    q=Queue(); q.put({next(iter(tasks))!r}); q.put(None)\n"
                      f"    worker(0,q,{args.end_time!r})\n")
    env = dict(os.environ, NVARC_CHALLENGES=str(challenge), NVARC_MODEL=str(model),
               NVARC_OUTPUTS=str(work / "outputs"), NVARC_STATUS=str(work / "status"),
               NVARC_ZERO_AUDIT=str(receipt_path), UNSLOTH_DISABLE_STATISTICS="1",
               TRITON_PTXAS_PATH="/usr/local/cuda/bin/ptxas", OMP_NUM_THREADS="12",
               PYTHONPATH=str(dep) + os.pathsep + str(work) + os.pathsep + os.environ.get("PYTHONPATH", ""))
    # Inherit the probe's process group so the notebook watchdog also bounds
    # setup/imports and can terminate every descendant at the first-cell deadline.
    process = subprocess.Popen([sys.executable, str(worker)], cwd=work, env=env)
    try:
        returncode = process.wait(timeout=max(0.1, args.end_time - time.time()))
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        raise RuntimeError("Bounded zero-update training check timed out")
    if returncode or not receipt_path.is_file():
        raise RuntimeError("Zero-update training check failed; no PASS receipt")
    receipt = json.loads(receipt_path.read_text())
    if receipt.get("status") != "PASS" or receipt.get("inference_executed") is not False:
        raise RuntimeError("Invalid engineering receipt")
    receipt.update({"dependency_provenance": provenance, "synthetic_manifest": manifest,
                    "driver_sha256": hashlib.sha256((ROOT / "driver.py").read_bytes()).hexdigest(),
                    "official_z_solver_sha256": hashlib.sha256(official_source.encode()).hexdigest(),
                    "instrumented_probe_solver_sha256": hashlib.sha256(probe_source.encode()).hexdigest(),
                    "probe_support_sha256": hashlib.sha256((ROOT / "zero_update_probe_support.py").read_bytes()).hexdigest(),
                    "hash_seed": 42, "worker_returncode": returncode})
    driver.atomic_json("/kaggle/working/zero-update-check.json", receipt)
    print(json.dumps(receipt, indent=2), flush=True)


if __name__ == "__main__":
    main()
