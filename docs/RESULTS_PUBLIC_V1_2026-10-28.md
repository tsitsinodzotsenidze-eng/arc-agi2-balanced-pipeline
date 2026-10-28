# Public symbolic coverage pilot — 28 October 2026

Decision: retain this reproducible null result; do not use v1 as a meaningful
ARC-AGI-2 competition candidate. This is not an official Kaggle score.

## Frozen comparison

The predeclared protocol compares maximum geometric depth 1 and depth 2,
with identical 24 operators, demonstration-fit gate, color-map fitting, ranking
and fallback policy. Identity geometry is included in both arms, giving 25 and
601 enumerated programs per task. Both predictions were written before the
scoring process opened the separate public solution file.

| Measure | Depth1 | Depth2 |
|---|---:|---:|
| Public evaluation tasks |120|120|
| Test outputs |167|167|
| Exact top1 outputs |0|0|
| Exact top2 outputs |0|0|
| All-test-correct tasks |0|0|
| Tasks with a demonstration-consistent program |0|0|
| Fallback test outputs |167|167|
| Wall seconds on this CPU host |0.225|3.957|

Paired output counts: depth2-only correct 0; depth1-only correct 0;
both correct 0; both incorrect 167. All task/output denominators are retained.
The timing is a local CPU measurement, not a Kaggle runtime prediction.

## Interpretation

The selected shallow geometry/recolor grammar does not cover the demonstration
relations in this public evaluation cohort. Therefore both arms fall back for
every test output. No general statement about symbolic reasoning, neural
solvers, Recovery, or comparative search-depth effectiveness follows.

This is a retrospective public benchmark. Historical public-data exposure
cannot be excluded, and current GitHub public files have not been established
to match Kaggle's 2026 public input bundle. Any future model trained on these
public evaluation puzzles must be labelled accordingly. These results do not
create fresh neural generalization evidence.

## Validation and audit

Root: 59 pytest tests passed, including existing contract tests and new synthetic
checks for geometry, jointly consistent color maps, unseen colors, composition,
output bounds, Boolean rejection, bundle ordering, label exclusion, offline
execution, completeness, and metric denominators. Python 3.12. No GPU used.
Astra independently checked solver contracts and zero-result structure; see
ASTRA_REVIEW_2026-10-28.md. No evaluation-target-driven code revision was made.

Frozen source/data receipt: docs/EXPERIMENT_FREEZE_V1.json
Freeze SHA256: d68221c14d1b0090806d87822c844274606e3ccef87e84f1a6983d5928ebebc3
Pinned source: arcprize/ARC-AGI-2 f3283f727488ad98fe575ea6a5ac981e4a188e49
Raw predictions, per-task audits and paired results: evidence/public-v1/
The original code-base snapshot is 01347aa067486bc5f5a95d50aa243a5a2877a74e.

## Reproduce

Clone the official public data at the pinned commit, then from this repository:

```sh
python -m scripts.prepare_public_benchmark --source-dir /path/to/ARC-AGI-2/data/evaluation --output-dir /path/to/public-v1
python -m scripts.evaluate_public --challenges /path/to/public-v1/challenges.json --solutions /path/to/public-v1/solutions.json --output-dir evidence/public-v1-reproduction --freeze docs/EXPERIMENT_FREEZE_V1.json
```

The evaluator rejects changed sources/data and refuses to overwrite an existing
output directory. Use a new reproduction directory and retain prior results.
The solver has no external dependencies; pytest is needed only for tests.

## Next feasibility gate

Audit an attributed, original-author NVARC working notebook and its exact
model/offline dependencies for ARC 2026 compatibility. This is a source/runtime
feasibility assessment only; neither neural evaluation, a GPU launch, a final
submission, public repository release nor Zenodo publication has occurred.
