"""Build the predeclared B1 carrier; preserve the completed B0 artifact byte-for-byte."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE_NAME = "NVARC_2026_SUBMISSION_CANDIDATE.ipynb"
BASE_SHA256 = "468d6c653869b60203c09fc1bb5db95cf1b96061a72d82c17684b730237aadb0"
DRIVER_SHA256 = "1eec5bb8db719e45d2e07af80b24db9b50d2214254b79445384d4852486f5fd4"
OLD_LAUNCH = "subprocess.run(command, check=True)\n"
NEW_LAUNCH = (
    "# B1: pin Python hashing BEFORE starting the driver interpreter.\n"
    "child_env = os.environ.copy()\n"
    "child_env['PYTHONHASHSEED'] = '42'\n"
    "subprocess.run(command, check=True, env=child_env)\n"
)


def build_b1(base_path: Path = ROOT / BASE_NAME) -> dict:
    raw = base_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != BASE_SHA256:
        raise ValueError("Completed B0 carrier changed; review provenance before building B1")
    nb = json.loads(raw)
    source = "".join(nb["cells"][1]["source"])
    if source.count(OLD_LAUNCH) != 1:
        raise ValueError("Expected exactly one B0 driver launch")
    nb["cells"][1]["source"] = source.replace(OLD_LAUNCH, NEW_LAUNCH, 1).splitlines(True)
    nb["metadata"]["nvarc_study"] = {
        "arm": "B1", "learning_rate": 5e-5, "python_hash_seed": 42,
        "baseline_script_version_id": 363494251,
        "baseline_notebook_sha256": BASE_SHA256,
        "driver_sha256": DRIVER_SHA256,
        "protocol": "docs/ARC2_UPDATE_STRENGTH_PROTOCOL_2026-10-29.md",
        "note": "Only the driver-launch hash environment changes; original NVARC policy retained.",
    }
    return nb


def main() -> None:
    nb = build_b1()
    notebook = ROOT / "NVARC_2026_B1_HASH42_SUBMISSION.ipynb"
    cell = ROOT / "B1_Cell2_CodeOnly.py"
    notebook.write_text(json.dumps(nb, indent=1) + "\n")
    cell.write_text("".join(nb["cells"][1]["source"]))
    print(json.dumps({
        "arm": "B1", "learning_rate": 5e-5, "python_hash_seed": 42,
        "notebook": notebook.name,
        "notebook_sha256": hashlib.sha256(notebook.read_bytes()).hexdigest(),
        "cell2_sha256": hashlib.sha256(cell.read_bytes()).hexdigest(),
        "driver_sha256": DRIVER_SHA256,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
