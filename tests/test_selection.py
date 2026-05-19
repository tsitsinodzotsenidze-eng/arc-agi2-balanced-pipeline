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
