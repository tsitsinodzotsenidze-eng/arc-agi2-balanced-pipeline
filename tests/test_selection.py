import pytest

from arc_agi2_pipeline.core.types import ArcTask, Candidate, PipelineContext, ScoredCandidate
from arc_agi2_pipeline.selection import TopKSelector


def _task(test_count: int = 1) -> ArcTask:
    return ArcTask(task_id="task", train=[], test_inputs=[[[0]] for _ in range(test_count)])


def _candidate(candidate_id: str, grid: list[list[int]], score: float = 1.0) -> ScoredCandidate:
    return ScoredCandidate(
        candidate=Candidate(
            candidate_id=candidate_id,
            task_id="task",
            test_index=0,
            grid=grid,
            generator_name="test",
        ),
        score=score,
        passed=True,
    )


def test_selector_prefers_grid_unique_second_attempt_over_duplicate_grid():
    scored = [
        _candidate("c3", [[1]], score=0.95),
        _candidate("c2", [[2]], score=0.90),
        _candidate("c1", [[1]], score=1.00),
    ]

    selected = TopKSelector().select(
        _task(), scored, max_attempts=2, context=PipelineContext(run_id="test")
    )

    assert [candidate.candidate_id for candidate in selected] == ["c1", "c2"]
    assert [candidate.grid for candidate in selected] == [[[1]], [[2]]]


def test_selector_falls_back_to_duplicate_grid_when_no_grid_unique_alternative_exists():
    scored = [
        _candidate("c2", [[1]], score=0.90),
        _candidate("c1", [[1]], score=1.00),
    ]

    selected = TopKSelector().select(
        _task(), scored, max_attempts=2, context=PipelineContext(run_id="test")
    )

    assert [candidate.candidate_id for candidate in selected] == ["c1", "c2"]
    assert [candidate.grid for candidate in selected] == [[[1]], [[1]]]


def test_selector_breaks_score_ties_deterministically_by_candidate_id_descending():
    scored = [
        _candidate("a", [[1]], score=1.0),
        _candidate("b", [[2]], score=1.0),
    ]

    selected = TopKSelector().select(
        _task(), scored, max_attempts=2, context=PipelineContext(run_id="test")
    )

    assert [candidate.candidate_id for candidate in selected] == ["b", "a"]


def test_selector_raises_when_max_attempts_is_non_positive():
    scored = [_candidate("c1", [[1]], score=1.0)]

    with pytest.raises(ValueError, match="max_attempts must be positive"):
        TopKSelector().select(_task(), scored, max_attempts=0, context=PipelineContext(run_id="test"))


def test_selector_raises_when_max_attempts_is_negative():
    scored = [_candidate("c1", [[1]], score=1.0)]

    with pytest.raises(ValueError, match="max_attempts must be positive"):
        TopKSelector().select(_task(), scored, max_attempts=-1, context=PipelineContext(run_id="test"))


def test_selector_validates_max_attempts_before_task_shape_or_candidate_indices():
    task = ArcTask(task_id="task", train=[], test_inputs=[])
    scored = [
        ScoredCandidate(
            candidate=Candidate(
                candidate_id="bad",
                task_id="task",
                test_index=99,
                grid=[[1]],
                generator_name="test",
            ),
            score=1.0,
            passed=True,
        )
    ]
    with pytest.raises(ValueError, match="max_attempts must be positive"):
        TopKSelector().select(task, scored, max_attempts=0, context=PipelineContext(run_id="test"))


def test_selector_validates_negative_max_attempts_before_task_shape_or_candidate_indices():
    task = ArcTask(task_id="task", train=[], test_inputs=[])
    scored = [
        ScoredCandidate(
            candidate=Candidate(
                candidate_id="bad",
                task_id="task",
                test_index=-1,
                grid=[[1]],
                generator_name="test",
            ),
            score=1.0,
            passed=True,
        )
    ]
    with pytest.raises(ValueError, match="max_attempts must be positive"):
        TopKSelector().select(task, scored, max_attempts=-5, context=PipelineContext(run_id="test"))


def test_selector_rejects_empty_test_inputs_for_otherwise_valid_arctask_empty_scored():
    task = ArcTask(task_id="task", train=[], test_inputs=[])
    with pytest.raises(ValueError, match="task must have at least one test input"):
        TopKSelector().select(task, [], max_attempts=1, context=PipelineContext(run_id="test"))


def test_selector_raises_when_task_has_zero_test_inputs_and_non_empty_scored():
    task = ArcTask(task_id="task", train=[], test_inputs=[])
    scored = [_candidate("c1", [[1]], score=1.0)]
    with pytest.raises(ValueError, match="task must have at least one test input"):
        TopKSelector().select(task, scored, max_attempts=1, context=PipelineContext(run_id="test"))


def test_selector_raises_when_candidate_test_index_is_negative():
    task = _task(test_count=2)
    scored = [
        ScoredCandidate(
            candidate=Candidate(
                candidate_id="c1",
                task_id="task",
                test_index=-1,
                grid=[[1]],
                generator_name="test",
            ),
            score=1.0,
            passed=True,
        )
    ]

    with pytest.raises(ValueError, match="invalid test_index"):
        TopKSelector().select(task, scored, max_attempts=1, context=PipelineContext(run_id="test"))


def test_selector_raises_when_candidate_test_index_is_out_of_range():
    task = _task(test_count=2)
    scored = [
        ScoredCandidate(
            candidate=Candidate(
                candidate_id="c1",
                task_id="task",
                test_index=2,
                grid=[[1]],
                generator_name="test",
            ),
            score=1.0,
            passed=True,
        )
    ]

    with pytest.raises(ValueError, match="invalid test_index"):
        TopKSelector().select(task, scored, max_attempts=1, context=PipelineContext(run_id="test"))


def test_selector_accepts_boundary_test_indices_zero_and_highest():
    task = _task(test_count=2)
    scored = [
        ScoredCandidate(
            candidate=Candidate(
                candidate_id="c0",
                task_id="task",
                test_index=0,
                grid=[[1]],
                generator_name="test",
            ),
            score=0.8,
            passed=True,
        ),
        ScoredCandidate(
            candidate=Candidate(
                candidate_id="c1",
                task_id="task",
                test_index=1,
                grid=[[2]],
                generator_name="test",
            ),
            score=0.9,
            passed=True,
        ),
    ]

    selected = TopKSelector().select(task, scored, max_attempts=1, context=PipelineContext(run_id="test"))
    assert [candidate.candidate_id for candidate in selected] == ["c0", "c1"]


def test_selector_raises_on_mixed_valid_and_invalid_test_indices():
    task = _task(test_count=2)
    scored = [
        ScoredCandidate(
            candidate=Candidate(
                candidate_id="valid",
                task_id="task",
                test_index=0,
                grid=[[1]],
                generator_name="test",
            ),
            score=1.0,
            passed=True,
        ),
        ScoredCandidate(
            candidate=Candidate(
                candidate_id="invalid",
                task_id="task",
                test_index=2,
                grid=[[2]],
                generator_name="test",
            ),
            score=0.9,
            passed=True,
        ),
    ]
    with pytest.raises(ValueError, match="invalid test_index"):
        TopKSelector().select(task, scored, max_attempts=1, context=PipelineContext(run_id="test"))


def test_selector_raises_when_invalid_test_index_is_between_valid_candidates():
    task = _task(test_count=2)
    scored = [
        ScoredCandidate(
            candidate=Candidate(
                candidate_id="valid_before",
                task_id="task",
                test_index=0,
                grid=[[1]],
                generator_name="test",
            ),
            score=1.0,
            passed=True,
        ),
        ScoredCandidate(
            candidate=Candidate(
                candidate_id="invalid_middle",
                task_id="task",
                test_index=5,
                grid=[[2]],
                generator_name="test",
            ),
            score=0.9,
            passed=True,
        ),
        ScoredCandidate(
            candidate=Candidate(
                candidate_id="valid_after",
                task_id="task",
                test_index=1,
                grid=[[3]],
                generator_name="test",
            ),
            score=0.8,
            passed=True,
        ),
    ]
    with pytest.raises(ValueError, match="invalid test_index"):
        TopKSelector().select(task, scored, max_attempts=1, context=PipelineContext(run_id="test"))


def test_selector_raises_when_multiple_candidates_are_malformed():
    task = _task(test_count=2)
    scored = [
        ScoredCandidate(
            candidate=Candidate(
                candidate_id="bad_neg",
                task_id="task",
                test_index=-1,
                grid=[[1]],
                generator_name="test",
            ),
            score=1.0,
            passed=True,
        ),
        ScoredCandidate(
            candidate=Candidate(
                candidate_id="bad_oob",
                task_id="task",
                test_index=3,
                grid=[[2]],
                generator_name="test",
            ),
            score=0.9,
            passed=True,
        ),
    ]
    with pytest.raises(ValueError, match="invalid test_index"):
        TopKSelector().select(task, scored, max_attempts=1, context=PipelineContext(run_id="test"))


def test_selector_returns_empty_list_for_valid_task_with_empty_scored():
    selected = TopKSelector().select(
        _task(test_count=2), [], max_attempts=1, context=PipelineContext(run_id="test")
    )
    assert selected == []


def test_selector_handles_multiple_test_inputs_independently():
    task = _task(test_count=2)
    scored = [
        ScoredCandidate(
            candidate=Candidate(
                candidate_id="t0_low",
                task_id="task",
                test_index=0,
                grid=[[1]],
                generator_name="test",
            ),
            score=0.5,
            passed=True,
        ),
        ScoredCandidate(
            candidate=Candidate(
                candidate_id="t0_high",
                task_id="task",
                test_index=0,
                grid=[[2]],
                generator_name="test",
            ),
            score=0.9,
            passed=True,
        ),
        ScoredCandidate(
            candidate=Candidate(
                candidate_id="t1_best",
                task_id="task",
                test_index=1,
                grid=[[3]],
                generator_name="test",
            ),
            score=0.7,
            passed=True,
        ),
    ]
    selected = TopKSelector().select(task, scored, max_attempts=1, context=PipelineContext(run_id="test"))
    assert [candidate.candidate_id for candidate in selected] == ["t0_high", "t1_best"]


def test_selector_regression_valid_behavior_across_ties_grids_and_test_indices():
    task = _task(test_count=2)
    scored = [
        ScoredCandidate(
            candidate=Candidate("t0_b", "task", 0, [[1]], "test"),
            score=1.0,
            passed=True,
        ),
        ScoredCandidate(
            candidate=Candidate("t0_a", "task", 0, [[1]], "test"),
            score=1.0,
            passed=True,
        ),
        ScoredCandidate(
            candidate=Candidate("t0_c", "task", 0, [[2]], "test"),
            score=0.8,
            passed=True,
        ),
        ScoredCandidate(
            candidate=Candidate("t1_y", "task", 1, [[7]], "test"),
            score=1.0,
            passed=True,
        ),
        ScoredCandidate(
            candidate=Candidate("t1_x", "task", 1, [[7]], "test"),
            score=1.0,
            passed=True,
        ),
        ScoredCandidate(
            candidate=Candidate("t1_z", "task", 1, [[8]], "test"),
            score=0.5,
            passed=True,
        ),
    ]
    selected = TopKSelector().select(task, scored, max_attempts=2, context=PipelineContext(run_id="test"))
    assert [candidate.candidate_id for candidate in selected] == ["t0_b", "t0_c", "t1_y", "t1_z"]


def test_selector_does_not_mutate_inputs():
    task = _task(test_count=2)
    original_test_inputs = [[row[:] for row in grid] for grid in task.test_inputs]
    c0 = Candidate("c0", "task", 0, [[1, 2]], "test")
    c1 = Candidate("c1", "task", 1, [[3, 4]], "test")
    scored = [
        ScoredCandidate(candidate=c0, score=0.9, passed=True),
        ScoredCandidate(candidate=c1, score=0.8, passed=True),
    ]
    original_scored_order = [item.candidate.candidate_id for item in scored]
    original_grids = [[row[:] for row in item.candidate.grid] for item in scored]

    selected = TopKSelector().select(task, scored, max_attempts=1, context=PipelineContext(run_id="test"))

    assert [candidate.candidate_id for candidate in selected] == ["c0", "c1"]
    assert task.test_inputs == original_test_inputs
    assert [item.candidate.candidate_id for item in scored] == original_scored_order
    assert [item.candidate.grid for item in scored] == original_grids
