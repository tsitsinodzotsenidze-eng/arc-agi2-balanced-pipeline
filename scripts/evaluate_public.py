"""Run both frozen arms before opening labels; public retrospective benchmark."""
from __future__ import annotations
import argparse
import hashlib
import json
import time
from pathlib import Path

from arc_agi2_pipeline.pipeline.runner import run


def score(payload: dict, solutions: dict, audit: dict) -> dict:
    if set(payload) != set(solutions):
        raise ValueError("Predictions and solutions must contain the same task ids")
    rows, out1, out2, task2, total, verified, fit_tasks = [], 0, 0, 0, 0, 0, 0
    for task_id in sorted(solutions):
        answers = solutions[task_id]
        if len(payload[task_id]) != len(answers):
            raise ValueError(f"Test-count mismatch: {task_id}")
        a = audit["tasks"][task_id]
        fit_tasks += a["train_consistent_programs"] > 0
        tests = []
        for i, target in enumerate(answers):
            prediction = payload[task_id][i]
            p1 = prediction["attempt_1"] == target
            p2 = p1 or prediction["attempt_2"] == target
            total += 1
            out1 += p1
            out2 += p2
            has_verified = a["selected"][i][0]["source"] == "train_consistent_program"
            verified += has_verified
            tests.append({"test_index": i, "top1": p1, "top2": p2, "verified": has_verified})
        passed = all(t["top2"] for t in tests)
        task2 += passed
        rows.append({"task_id": task_id, "all_tests_top2": passed, "tests": tests})
    return {
        "tasks": len(rows), "test_outputs": total, "top1_outputs": out1, "top2_outputs": out2,
        "top1_fraction": out1 / total, "top2_fraction": out2 / total,
        "all_tests_top2_tasks": task2, "all_tests_top2_fraction": task2 / len(rows),
        "train_fit_tasks": fit_tasks, "verified_outputs": verified,
        "fallback_outputs": total - verified, "per_task": rows,
    }


def evaluate(challenges: Path, solutions_path: Path, output: Path, freeze: Path) -> dict:
    receipt = json.loads(freeze.read_text())
    root = Path(__file__).resolve().parents[1]
    for name, expected in receipt["source_sha256"].items():
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"Source changed after protocol freeze: {name}")
    expected_data = receipt["data"]
    for label, path in [("challenges_sha256", challenges), ("solutions_sha256", solutions_path)]:
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected_data[label]:
            raise ValueError(f"Data changed after protocol freeze: {label}")
    challenge_data = json.loads(challenges.read_text())
    if len(challenge_data) != expected_data["tasks"] or sum(
            len(t["test"]) for t in challenge_data.values()) != expected_data["test_outputs"]:
        raise ValueError("Challenge cohort differs from the protocol freeze")
    output.mkdir(parents=True, exist_ok=False)
    times = {}
    for depth in (1, 2):
        started = time.monotonic()
        run(None, output / f"depth{depth}-predictions.json", challenges_json=challenges,
            max_depth=depth, audit_path=output / f"depth{depth}-audit.json")
        times[depth] = time.monotonic() - started
    # Both predictions now exist; inference has never received this label path.
    solutions = json.loads(solutions_path.read_text())
    if len(solutions) != expected_data["tasks"] or sum(map(len, solutions.values())) != expected_data["test_outputs"]:
        raise ValueError("Solution cohort differs from the protocol freeze")
    results = {}
    for depth in (1, 2):
        payload = json.loads((output / f"depth{depth}-predictions.json").read_text())
        audit = json.loads((output / f"depth{depth}-audit.json").read_text())
        results[f"depth{depth}"] = score(payload, solutions, audit)
        results[f"depth{depth}"]["elapsed_seconds"] = times[depth]
    by_depth = [{(r["task_id"], t["test_index"]): t["top2"]
        for r in results[f"depth{d}"]["per_task"] for t in r["tests"]} for d in (1, 2)]
    first, second = by_depth
    paired = {
        "depth2_only_correct_outputs": sum(second[k] and not first[k] for k in first),
        "depth1_only_correct_outputs": sum(first[k] and not second[k] for k in first),
        "both_correct_outputs": sum(first[k] and second[k] for k in first),
        "both_wrong_outputs": sum(not first[k] and not second[k] for k in first),
    }
    report = {
        "benchmark": "public retrospective ARC-AGI-2; not official Kaggle score",
        "freeze_sha256": hashlib.sha256(freeze.read_bytes()).hexdigest(),
        "challenges_sha256": hashlib.sha256(challenges.read_bytes()).hexdigest(),
        "solutions_sha256": hashlib.sha256(solutions_path.read_bytes()).hexdigest(),
        "arms": results, "paired": paired,
    }
    (output / "results.json").write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    return {"arms": {k: {n: v for n, v in a.items() if n != "per_task"}
            for k, a in results.items()}, "paired": paired}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--challenges", type=Path, required=True)
    p.add_argument("--solutions", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--freeze", type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(evaluate(args.challenges, args.solutions, args.output_dir, args.freeze), indent=2))
