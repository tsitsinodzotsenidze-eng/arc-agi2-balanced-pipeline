from arc_agi2_pipeline.core.types import ArcPair, ArcTask, Candidate, PipelineContext, ScoredCandidate
from arc_agi2_pipeline.selection import TopKSelector


def test_arc_task_structure():
    pair = ArcPair(input=[[1]], output=[[2]])
    task = ArcTask(task_id="x", train=[pair], test_inputs=[[[3]]])
    assert task.task_id == "x"
    assert task.train[0].output == [[2]]


def test_topk_selector_picks_highest_scores_per_test_index():
    task = ArcTask(task_id="t", train=[], test_inputs=[[[0]], [[0]]])
    c1 = Candidate(candidate_id="c1", task_id="t", test_index=0, grid=[[1]], generator_name="g")
    c2 = Candidate(candidate_id="c2", task_id="t", test_index=0, grid=[[2]], generator_name="g")
    c3 = Candidate(candidate_id="c3", task_id="t", test_index=1, grid=[[3]], generator_name="g")

    scored = [
        ScoredCandidate(candidate=c1, score=0.1, passed=True),
        ScoredCandidate(candidate=c2, score=0.9, passed=True),
        ScoredCandidate(candidate=c3, score=0.5, passed=True),
    ]

    selected = TopKSelector().select(task, scored, max_attempts=1, context=PipelineContext(run_id="r"))
    assert selected == [c2, c3]
