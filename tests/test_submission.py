import json
from pathlib import Path

import pytest

from arc_agi2_pipeline.core.types import Candidate
from arc_agi2_pipeline.submission import (
    build_submission_payload,
    validate_submission_payload,
    write_submission,
)


def test_build_submission_payload_zero_candidates_returns_empty_payload():
    assert build_submission_payload([]) == {}


def test_submission_payload_shape():
    c1 = Candidate(candidate_id="1", task_id="abc", test_index=0, grid=[[1]], generator_name="g")
    c2 = Candidate(candidate_id="2", task_id="abc", test_index=0, grid=[[2]], generator_name="g")
    payload = build_submission_payload([c1, c2])

    assert "abc" in payload
    assert payload["abc"][0]["attempt_1"] == [[1]]
    assert payload["abc"][0]["attempt_2"] == [[2]]


def test_build_submission_payload_uses_first_two_candidates_only():
    c1 = Candidate(candidate_id="1", task_id="abc", test_index=0, grid=[[1]], generator_name="g")
    c2 = Candidate(candidate_id="2", task_id="abc", test_index=0, grid=[[2]], generator_name="g")
    c3 = Candidate(candidate_id="3", task_id="abc", test_index=0, grid=[[3]], generator_name="g")

    payload = build_submission_payload([c1, c2, c3])
    assert payload["abc"][0]["attempt_1"] == [[1]]
    assert payload["abc"][0]["attempt_2"] == [[2]]


def test_build_submission_payload_warns_when_more_than_two_candidates(caplog):
    c1 = Candidate(candidate_id="1", task_id="abc", test_index=0, grid=[[1]], generator_name="g")
    c2 = Candidate(candidate_id="2", task_id="abc", test_index=0, grid=[[2]], generator_name="g")
    c3 = Candidate(candidate_id="3", task_id="abc", test_index=0, grid=[[3]], generator_name="g")

    with caplog.at_level("WARNING"):
        payload = build_submission_payload([c1, c2, c3])

    assert payload["abc"][0]["attempt_1"] == [[1]]
    assert payload["abc"][0]["attempt_2"] == [[2]]
    assert "uses only the first two" in caplog.text


def test_build_submission_payload_rejects_single_candidate_for_test_index():
    c1 = Candidate(candidate_id="1", task_id="abc", test_index=0, grid=[[1]], generator_name="g")
    with pytest.raises(ValueError, match="requires at least 2 candidates"):
        build_submission_payload([c1])


def test_submission_validation_valid_payload_passes():
    payload = {"x": [{"attempt_1": [[0, 1], [2, 3]], "attempt_2": [[4, 5], [6, 7]]}]}
    validate_submission_payload(payload)


def test_submission_validation_accepts_boundary_values_0_and_9():
    payload = {"x": [{"attempt_1": [[0, 9]], "attempt_2": [[9, 0]]}]}
    validate_submission_payload(payload)


def test_submission_validation_rejects_non_rectangular_attempt():
    payload = {"x": [{"attempt_1": [[1], [1, 2]], "attempt_2": [[0]]}]}
    with pytest.raises(ValueError, match="rectangular"):
        validate_submission_payload(payload)


def test_submission_validation_rejects_empty_row_in_grid():
    payload = {"x": [{"attempt_1": [[1], []], "attempt_2": [[0]]}]}
    with pytest.raises(ValueError, match="rows must each be a non-empty list"):
        validate_submission_payload(payload)


def test_submission_validation_rejects_non_integer_cell():
    payload = {"x": [{"attempt_1": [[1.2]], "attempt_2": [[0]]}]}
    with pytest.raises(ValueError, match="must be an integer"):
        validate_submission_payload(payload)


def test_submission_validation_rejects_out_of_range_cell():
    payload = {"x": [{"attempt_1": [[10]], "attempt_2": [[0]]}]}
    with pytest.raises(ValueError, match=r"\[0, 9\]"):
        validate_submission_payload(payload)


def test_submission_validation_rejects_missing_attempt_key():
    payload = {"x": [{"attempt_1": [[1]]}]}
    with pytest.raises(ValueError, match="missing keys"):
        validate_submission_payload(payload)


def test_submission_validation_rejects_unknown_extra_key():
    payload = {"x": [{"attempt_1": [[1]], "attempt_2": [[2]], "attempt_3": [[3]]}]}
    with pytest.raises(ValueError, match="unknown keys"):
        validate_submission_payload(payload)


def test_build_submission_payload_groups_by_task_and_sorted_test_index():
    candidates = [
        Candidate(candidate_id="a1", task_id="task_b", test_index=1, grid=[[1]], generator_name="g"),
        Candidate(candidate_id="a2", task_id="task_b", test_index=1, grid=[[2]], generator_name="g"),
        Candidate(candidate_id="b1", task_id="task_b", test_index=0, grid=[[3]], generator_name="g"),
        Candidate(candidate_id="b2", task_id="task_b", test_index=0, grid=[[4]], generator_name="g"),
        Candidate(candidate_id="c1", task_id="task_a", test_index=0, grid=[[5]], generator_name="g"),
        Candidate(candidate_id="c2", task_id="task_a", test_index=0, grid=[[6]], generator_name="g"),
    ]

    payload = build_submission_payload(candidates)

    assert set(payload.keys()) == {"task_a", "task_b"}
    assert payload["task_b"][0]["attempt_1"] == [[3]]
    assert payload["task_b"][0]["attempt_2"] == [[4]]
    assert payload["task_b"][1]["attempt_1"] == [[1]]
    assert payload["task_b"][1]["attempt_2"] == [[2]]
    assert payload["task_a"][0]["attempt_1"] == [[5]]
    assert payload["task_a"][0]["attempt_2"] == [[6]]


def test_write_submission_round_trip(tmp_path: Path):
    payload = {
        "task_x": [{"attempt_1": [[1, 2]], "attempt_2": [[2, 1]]}],
        "task_y": [{"attempt_1": [[3]], "attempt_2": [[4]]}],
    }
    output_path = tmp_path / "submission.json"

    write_submission(payload, output_path)

    with output_path.open("r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded == payload
    assert not output_path.with_suffix(".json.tmp").exists()
