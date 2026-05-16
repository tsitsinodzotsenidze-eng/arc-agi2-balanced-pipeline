import json

import pytest

from arc_agi2_pipeline.data.loader import load_task_file


def test_load_task_file(tmp_path):
    task_path = tmp_path / "sample_task.json"
    raw = {
        "train": [{"input": [[0]], "output": [[1]]}],
        "test": [{"input": [[2]]}],
    }
    task_path.write_text(json.dumps(raw), encoding="utf-8")

    task = load_task_file(task_path)

    assert task.task_id == "sample_task"
    assert task.train[0].input == [[0]]
    assert task.test_inputs[0] == [[2]]


def test_load_task_file_rejects_non_rectangular_grid(tmp_path):
    task_path = tmp_path / "bad.json"
    raw = {"train": [{"input": [[0], []], "output": [[1]]}], "test": [{"input": [[2]]}]}
    task_path.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(ValueError):
        load_task_file(task_path)
