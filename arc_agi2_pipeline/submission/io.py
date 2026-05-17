from __future__ import annotations

import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Sequence

from arc_agi2_pipeline.core.types import Candidate

_ALLOWED_ATTEMPT_KEYS = {"attempt_1", "attempt_2"}
_LOG = logging.getLogger(__name__)


def _validate_grid(grid: list, *, field_name: str) -> None:
    if not isinstance(grid, list) or not grid:
        raise ValueError(f"{field_name} must be a non-empty list of rows.")
    if not all(isinstance(row, list) and row for row in grid):
        raise ValueError(f"{field_name} rows must each be a non-empty list.")

    row_len = len(grid[0])
    if any(len(row) != row_len for row in grid):
        raise ValueError(f"{field_name} must be rectangular (all rows same length).")

    for r_i, row in enumerate(grid):
        for c_i, value in enumerate(row):
            if not isinstance(value, int):
                raise ValueError(f"{field_name}[{r_i}][{c_i}] must be an integer.")
            if value < 0 or value > 9:
                raise ValueError(f"{field_name}[{r_i}][{c_i}] must be in ARC color range [0, 9].")


def build_submission_payload(candidates: Sequence[Candidate]) -> Dict[str, List[dict]]:
    """Build submission payload from pre-ranked candidates.

    Contract:
    - For empty/debug runs, an empty candidate list returns `{}`. This is not
      sufficient for final competition completeness; completeness must be
      validated separately against the expected task list.
    - Requires at least 2 candidates for each (task_id, test_index).
    - Uses the first two candidates in supplied list order as attempt_1/attempt_2.
    - Callers must sort/rank candidates upstream before calling this function.
    - Extra candidates beyond the first two are intentionally ignored at IO layer.
    """
    grouped: Dict[str, Dict[int, List[Candidate]]] = defaultdict(lambda: defaultdict(list))
    for c in candidates:
        grouped[c.task_id][c.test_index].append(c)

    payload: Dict[str, List[dict]] = {}
    for task_id, by_test in grouped.items():
        outputs: List[dict] = []
        for test_index in sorted(by_test.keys()):
            attempts = [c.grid for c in by_test[test_index]]
            if len(attempts) < 2:
                raise ValueError(
                    f"Task {task_id}[{test_index}] requires at least 2 candidates to produce "
                    "both attempt_1 and attempt_2 with valid grids."
                )
            if len(attempts) > 2:
                _LOG.warning(
                    "Task %s[%d] received %d candidates; build_submission_payload uses only the first two. "
                    "Rank/select upstream before IO payload construction.",
                    task_id,
                    test_index,
                    len(attempts),
                )
            output = {
                "attempt_1": attempts[0],
                "attempt_2": attempts[1],
            }
            outputs.append(output)
        payload[task_id] = outputs
    return payload


def validate_submission_payload(payload: Dict[str, List[dict]]) -> None:
    if not isinstance(payload, dict):
        raise ValueError("Submission payload must be a dictionary.")

    for task_id, test_outputs in payload.items():
        if not isinstance(task_id, str):
            raise ValueError("Task ids must be strings.")
        if not isinstance(test_outputs, list):
            raise ValueError(f"Task {task_id}: outputs must be a list.")

        for i, output in enumerate(test_outputs):
            if not isinstance(output, dict):
                raise ValueError(f"Task {task_id}: each test output must be a dict.")

            keys = set(output.keys())
            if keys != _ALLOWED_ATTEMPT_KEYS:
                missing = sorted(_ALLOWED_ATTEMPT_KEYS - keys)
                extra = sorted(keys - _ALLOWED_ATTEMPT_KEYS)
                details = []
                if missing:
                    details.append(f"missing keys: {missing}")
                if extra:
                    details.append(f"unknown keys: {extra}")
                raise ValueError(
                    f"Task {task_id}[{i}]: output keys must be exactly {sorted(_ALLOWED_ATTEMPT_KEYS)} ({'; '.join(details)})."
                )

            _validate_grid(output["attempt_1"], field_name=f"{task_id}[{i}].attempt_1")
            _validate_grid(output["attempt_2"], field_name=f"{task_id}[{i}].attempt_2")


def write_submission(payload: Dict[str, List[dict]], output_path: Path) -> None:
    validate_submission_payload(payload)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = output_path.with_suffix(f"{output_path.suffix}.tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        # Keep key order deterministic for reproducible diffs and stable submission files.
        json.dump(payload, f, sort_keys=True)
    tmp_path.replace(output_path)
