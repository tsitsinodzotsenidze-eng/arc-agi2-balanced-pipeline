"""Offline candidate entry point for per-task files or a Kaggle JSON bundle."""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Sequence

from arc_agi2_pipeline.core.types import ArcTask, Candidate
from arc_agi2_pipeline.data.loader import load_tasks_from_bundle, load_tasks_from_dir
from arc_agi2_pipeline.generators.programs import solve_task
from arc_agi2_pipeline.submission import (
    build_submission_payload, validate_submission_against_tasks, write_submission,
)


def predict_tasks(tasks: Sequence[ArcTask], max_depth: int = 2) -> tuple[dict, dict]:
    if not tasks or len({t.task_id for t in tasks}) != len(tasks):
        raise ValueError("Task list must be nonempty with unique task ids")
    candidates = []
    audits = {}
    for task in tasks:
        started = time.monotonic()
        outputs, audit = solve_task(task, max_depth=max_depth)
        audit["elapsed_seconds"] = time.monotonic() - started
        audits[task.task_id] = audit
        for i, choices in enumerate(outputs):
            for j, grid in enumerate(choices):
                candidates.append(Candidate(
                    candidate_id=f"{task.task_id}:{i}:{j}", task_id=task.task_id,
                    test_index=i, grid=grid, generator_name="symbolic-programs-v1",
                    metadata=audit["selected"][i][j],
                ))
    payload = build_submission_payload(candidates)
    validate_submission_against_tasks(tasks, payload)
    return payload, audits


def run(tasks_dir: Path | None, output_path: Path, max_attempts: int = 2,
        seed: int = 0, *, challenges_json: Path | None = None,
        max_depth: int = 2, audit_path: Path | None = None) -> None:
    if max_attempts != 2:
        raise ValueError("ARC-AGI-2 submissions require both attempt_1 and attempt_2; use exactly two attempts")
    if (tasks_dir is None) == (challenges_json is None):
        raise ValueError("Supply exactly one of tasks_dir or challenges_json")
    tasks = load_tasks_from_dir(tasks_dir) if tasks_dir is not None else load_tasks_from_bundle(challenges_json)
    payload, audits = predict_tasks(tasks, max_depth=max_depth)
    write_submission(payload, output_path)
    if audit_path is not None:
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        audit_path.write_text(json.dumps({
            "seed": seed, "seed_used_by_deterministic_solver": False, "tasks": audits,
        }, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the bounded symbolic ARC2 candidate")
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--tasks-dir", type=Path)
    inputs.add_argument("--challenges-json", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit", type=Path)
    parser.add_argument("--max-depth", type=int, choices=(1, 2), default=2)
    parser.add_argument("--max-attempts", type=int, default=2)
    parser.add_argument("--seed", type=int, default=0)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args.tasks_dir, args.output, args.max_attempts, args.seed,
        challenges_json=args.challenges_json, max_depth=args.max_depth, audit_path=args.audit)
