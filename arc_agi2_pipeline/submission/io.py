from __future__ import annotations

import json
import logging
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Sequence

from arc_agi2_pipeline.core.types import ArcTask, Candidate

_ALLOWED_ATTEMPT_KEYS = {"attempt_1", "attempt_2"}
_LOG = logging.getLogger(__name__)


def _validate_grid(grid: list, *, field_name: str) -> None:
    if not isinstance(grid, list) or not grid:
        raise ValueError(f"{field_name} must be a non-empty list of rows.")
    if not all(isinstance(row, list) and row for row in grid):
        raise ValueError(f"{field_name} rows must each be a non-empty list.")

    row_len = len(grid[0])
    if len(grid) > 30 or row_len > 30:
        raise ValueError(f"{field_name} dimensions must be at most 30 by 30.")
    if any(len(row) != row_len for row in grid):
        raise ValueError(f"{field_name} must be rectangular (all rows same length).")

    for r_i, row in enumerate(grid):
        for c_i, value in enumerate(row):
            if type(value) is not int:
                raise ValueError(f"{field_name}[{r_i}][{c_i}] must be an integer.")
            if value < 0 or value > 9:
                raise ValueError(
                    f"{field_name}[{r_i}][{c_i}] must be in ARC color range [0, 9]."
                )


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
    grouped: Dict[str, Dict[int, List[Candidate]]] = defaultdict(
        lambda: defaultdict(list)
    )
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


def validate_submission_against_tasks(
    tasks: Sequence[ArcTask],
    payload: Dict[str, List[dict]],
    *,
    allow_extra_task_ids: bool = False,
) -> None:
    """Validate payload completeness against the loaded ARC challenge tasks.

    This enforces final submission completeness in addition to the structural
    payload checks performed by :func:`validate_submission_payload`.
    """
    validate_submission_payload(payload)

    expected_counts = {task.task_id: len(task.test_inputs) for task in tasks}
    expected_ids = set(expected_counts)
    payload_ids = set(payload)

    missing_task_ids = sorted(expected_ids - payload_ids)
    if missing_task_ids:
        raise ValueError(f"Submission payload is missing task ids: {missing_task_ids}.")

    extra_task_ids = sorted(payload_ids - expected_ids)
    if extra_task_ids and not allow_extra_task_ids:
        raise ValueError(
            f"Submission payload contains extra task ids: {extra_task_ids}."
        )

    mismatches = []
    for task_id in sorted(expected_ids & payload_ids):
        expected_count = expected_counts[task_id]
        actual_count = len(payload[task_id])
        if actual_count != expected_count:
            mismatches.append(
                f"{task_id}: expected {expected_count}, got {actual_count}"
            )

    if mismatches:
        raise ValueError(
            "Submission payload has mismatched output counts for task ids: "
            + "; ".join(mismatches)
            + "."
        )


def write_submission(payload: Dict[str, List[dict]], output_path: Path) -> None:
    validate_submission_payload(payload)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=output_path.parent,
            prefix=f".{output_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as f:
            tmp_path = Path(f.name)
            # Keep key order deterministic for reproducible diffs and stable submission files.
            json.dump(payload, f, sort_keys=True)
        tmp_path.replace(output_path)
    except Exception:
        if tmp_path is not None and tmp_path.exists():
            tmp_path.unlink()
        raise
