"""Split public files without displaying targets; this is NOT inference code."""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def prepare(source: Path, dest: Path) -> dict:
    actual_commit = subprocess.check_output(
        ["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
    if actual_commit != "f3283f727488ad98fe575ea6a5ac981e4a188e49":
        raise ValueError("Public data checkout does not match the pinned commit")
    if subprocess.check_output(["git", "-C", str(source), "status", "--porcelain", "--", "."], text=True).strip():
        raise ValueError("Public data checkout has modified task files")
    challenges, solutions, hashes = {}, {}, {}
    for path in sorted(source.glob("*.json")):
        data = path.read_bytes()
        raw = json.loads(data)
        challenges[path.stem] = {
            "train": raw["train"], "test": [{"input": t["input"]} for t in raw["test"]],
        }
        solutions[path.stem] = [t["output"] for t in raw["test"]]
        hashes[path.name] = hashlib.sha256(data).hexdigest()
    if not challenges:
        raise ValueError("No public task files")
    dest.mkdir(parents=True, exist_ok=True)
    for name, data in [("challenges.json", challenges), ("solutions.json", solutions)]:
        (dest / name).write_text(json.dumps(data, sort_keys=True) + "\n", encoding="utf-8")
    manifest = {
        "source_commit": actual_commit,
        "tasks": len(challenges), "test_outputs": sum(len(t["test"]) for t in challenges.values()),
        "source_files_sha256": hashes,
        "challenges_sha256": hashlib.sha256((dest / "challenges.json").read_bytes()).hexdigest(),
        "solutions_sha256": hashlib.sha256((dest / "solutions.json").read_bytes()).hexdigest(),
    }
    (dest / "data-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return {k: v for k, v in manifest.items() if k != "source_files_sha256"}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--source-dir", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(prepare(args.source_dir, args.output_dir), sort_keys=True))
