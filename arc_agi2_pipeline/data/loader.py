from __future__ import annotations

import json
from pathlib import Path
from typing import List

from arc_agi2_pipeline.core.types import ArcPair, ArcTask


def _validate_grid(grid: list, *, field_name: str) -> None:
    if not isinstance(grid, list) or not grid:
        raise ValueError(f"{field_name} must be a non-empty list.")
    if not all(isinstance(row, list) and row for row in grid):
        raise ValueError(f"{field_name} rows must be non-empty lists.")
    row_len = len(grid[0])
    if len(grid) > 30 or row_len > 30:
        raise ValueError(f"{field_name} dimensions must be at most 30 by 30.")
    if any(len(row) != row_len for row in grid):
        raise ValueError(f"{field_name} must be rectangular.")
    if any(any(type(v) is not int or v < 0 or v > 9 for v in row) for row in grid):
        raise ValueError(f"{field_name} cells must be integers in [0, 9].")


def _parse_pair(raw: dict, index: int) -> ArcPair:
    if not isinstance(raw, dict):
        raise ValueError(f"train[{index}] must be an object.")
    if "input" not in raw or "output" not in raw:
        raise ValueError(f"train[{index}] requires input/output.")
    _validate_grid(raw["input"], field_name=f"train[{index}].input")
    _validate_grid(raw["output"], field_name=f"train[{index}].output")
    return ArcPair(input=raw["input"], output=raw["output"])


def load_task_file(path: Path) -> ArcTask:
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    return parse_task(path.stem, raw, source_path=str(path))


def parse_task(task_id: str, raw: dict, source_path: str | None = None) -> ArcTask:
    if not isinstance(task_id, str) or not task_id or not isinstance(raw, dict):
        raise ValueError("Tasks require a nonempty string id and JSON object.")
    if "train" not in raw or "test" not in raw:
        raise ValueError(f"{task_id}: task must include train and test.")

    if not isinstance(raw["train"], list) or not raw["train"]:
        raise ValueError(f"{task_id}: train must be a nonempty list.")
    if not isinstance(raw["test"], list) or not raw["test"]:
        raise ValueError(f"{task_id}: test must be a nonempty list.")
    train = [_parse_pair(example, i) for i, example in enumerate(raw.get("train", []))]

    test_inputs = []
    for i, example in enumerate(raw.get("test", [])):
        if not isinstance(example, dict) or "input" not in example:
            raise ValueError(f"test[{i}] requires input.")
        _validate_grid(example["input"], field_name=f"test[{i}].input")
        test_inputs.append(example["input"])

    return ArcTask(task_id=task_id, train=train, test_inputs=test_inputs, source_path=source_path)


def load_tasks_from_bundle(path: Path) -> List[ArcTask]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not raw:
        raise ValueError("Challenges bundle must be a nonempty task-id object.")
    return [parse_task(task_id, raw[task_id], str(path)) for task_id in sorted(raw)]


def load_tasks_from_dir(tasks_dir: Path) -> List[ArcTask]:
    task_files = sorted(tasks_dir.glob("*.json"))
    if not task_files:
        raise ValueError(f"No task files found in {tasks_dir}")
    return [load_task_file(p) for p in task_files]
