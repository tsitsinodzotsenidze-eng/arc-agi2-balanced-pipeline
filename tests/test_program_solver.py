import copy
import json
import socket

import pytest

from arc_agi2_pipeline.core.types import ArcPair, ArcTask
from arc_agi2_pipeline.data.loader import load_tasks_from_bundle, parse_task
from arc_agi2_pipeline.generators.programs import OPS, apply_op, fit_program, grid_key, solve_task
from arc_agi2_pipeline.pipeline.runner import run
from arc_agi2_pipeline.submission import validate_submission_against_tasks, validate_submission_payload
from scripts.evaluate_public import score


def test_d4_has_eight_distinct_views_and_inverse_rotation():
    g = [[0, 1, 2], [3, 4, 5]]
    views = [g] + [apply_op(g, op) for op in (
        'rot90', 'rot180', 'rot270', 'flip_h', 'flip_v', 'transpose', 'anti_transpose')]
    assert len({grid_key(v) for v in views}) == 8
    assert apply_op(apply_op(g, 'rot90'), 'rot270') == g
    assert apply_op(g, 'rot90') == [[3, 0], [4, 1], [5, 2]]
    assert apply_op(g, 'anti_transpose') == [[5, 2], [4, 1], [3, 0]]


def test_color_map_is_joint_across_examples():
    task = ArcTask('conflict', [ArcPair([[1]], [[2]]), ArcPair([[1]], [[3]])], [[[1]]])
    assert fit_program(task, ()) is None
    pred, audit = solve_task(task)
    assert audit['train_consistent_programs'] == 0
    assert [x['source'] for x in audit['selected'][0]] == ['fallback_identity', 'fallback_first_train_output']
    assert pred == [[[[1]], [[2]]]]


def test_color_map_preserves_unseen_test_colors_and_inputs():
    task = ArcTask('map', [ArcPair([[1, 0]], [[2, 0]]), ArcPair([[1, 1]], [[2, 2]])], [[[1, 9]]])
    original = copy.deepcopy(task)
    fitted = fit_program(task, ())
    assert fitted.predict([[1, 9]]) == [[2, 9]]
    assert task == original


def test_depth_two_can_crop_then_rotate_with_unseen_test_pattern():
    g1 = [[0, 0, 0, 0, 0], [0, 1, 2, 1, 0], [0, 2, 1, 2, 0], [0, 0, 0, 0, 0]]
    g2 = [[0, 0, 0, 0, 0], [0, 3, 4, 3, 0], [0, 4, 3, 4, 0], [0, 0, 0, 0, 0]]
    test = [[0, 0, 0, 0, 0], [0, 1, 2, 2, 0], [0, 2, 1, 1, 0], [0, 0, 0, 0, 0]]
    def target(g):
        return apply_op(apply_op(g, 'crop_0'), 'rot90')
    task = ArcTask('synthetic', [ArcPair(g1, target(g1)), ArcPair(g2, target(g2))], [test])
    p1, a1 = solve_task(task, 1)
    p2, a2 = solve_task(task, 2)
    assert a1['train_consistent_programs'] == 0
    assert target(test) in p2[0]
    assert a2['train_consistent_programs'] > 0
    assert a1['programs_enumerated'] == 1 + len(OPS)
    assert a2['programs_enumerated'] == 1 + len(OPS) + len(OPS) ** 2


def test_expand_and_tile_differ_and_size_cap_is_enforced():
    g = [[1, 2]]
    assert apply_op(g, 'scale_2') == [[1, 1, 2, 2], [1, 1, 2, 2]]
    assert apply_op(g, 'tile_2_2') == [[1, 2, 1, 2], [1, 2, 1, 2]]
    assert apply_op([[1] * 16], 'scale_2') is None
    assert apply_op([[0]], 'crop_0') is None


@pytest.mark.parametrize('bad', [[[True]], [[1] * 31], [[1]] * 31, [[10]], [[]]])
def test_bundle_rejects_invalid_grid(bad):
    with pytest.raises(ValueError):
        parse_task('bad', {'train': [{'input': bad, 'output': [[1]]}], 'test': [{'input': [[1]]}]})


def test_bundle_preserves_test_order_and_discards_all_test_targets(tmp_path):
    raw = {'z': {'train': [{'input': [[1]], 'output': [[2]]}],
                 'test': [{'input': [[1]], 'output': [[9]]}, {'input': [[9]], 'output': [[8]]}]}}
    path = tmp_path / 'challenges.json'
    path.write_text(json.dumps(raw))
    loaded = load_tasks_from_bundle(path)
    raw['z']['test'][0]['output'] = [[0]]
    raw['z']['test'][1]['output'] = [[0]]
    path.write_text(json.dumps(raw))
    changed = load_tasks_from_bundle(path)
    assert loaded[0].test_inputs == [[[1]], [[9]]]
    assert loaded == changed
    assert solve_task(loaded[0])[0] == solve_task(changed[0])[0]


def test_offline_entry_writes_both_attempts_every_test_and_audit(tmp_path, monkeypatch):
    def blocked(*args, **kwargs):
        raise AssertionError('Network must not be used')
    monkeypatch.setattr(socket, 'socket', blocked)
    raw = {'b': {'train': [{'input': [[1]], 'output': [[2]]}],
                 'test': [{'input': [[1]]}, {'input': [[9]]}]}}
    challenges = tmp_path / 'bundle.json'
    challenges.write_text(json.dumps(raw))
    output, audit = tmp_path / 'out' / 'submission.json', tmp_path / 'audit.json'
    run(None, output, challenges_json=challenges, max_depth=1, audit_path=audit)
    payload = json.loads(output.read_text())
    validate_submission_against_tasks(load_tasks_from_bundle(challenges), payload)
    assert len(payload['b']) == 2
    assert payload['b'][0] == {'attempt_1': [[2]], 'attempt_2': [[2]]}
    assert payload['b'][1] == {'attempt_1': [[9]], 'attempt_2': [[9]]}
    assert json.loads(audit.read_text())['tasks']['b']['selected'][0][1]['source'] == 'duplicate_verified'
    with pytest.raises(ValueError):
        run(None, output, challenges_json=challenges, max_attempts=1)


def test_submission_rejects_bool_and_oversize():
    for grid in ([[True]], [[1] * 31]):
        with pytest.raises(ValueError):
            validate_submission_payload({'x': [{'attempt_1': grid, 'attempt_2': [[0]]}]})


def test_metric_keeps_output_and_all_tests_task_denominators_separate():
    payload = {
        'a': [{'attempt_1': [[1]], 'attempt_2': [[1]]}, {'attempt_1': [[0]], 'attempt_2': [[0]]}],
        'b': [{'attempt_1': [[0]], 'attempt_2': [[3]]}],
    }
    solutions = {'a': [[[1]], [[2]]], 'b': [[[3]]]}
    audit = {'tasks': {k: {'train_consistent_programs': 0,
        'selected': [[{'source': 'fallback_identity'}] for _ in v]} for k, v in solutions.items()}}
    result = score(payload, solutions, audit)
    assert result['top1_outputs'] == 1
    assert result['top2_outputs'] == 2
    assert result['test_outputs'] == 3
    assert result['all_tests_top2_tasks'] == 1
    assert result['tasks'] == 2
    assert result['verified_outputs'] == 0
