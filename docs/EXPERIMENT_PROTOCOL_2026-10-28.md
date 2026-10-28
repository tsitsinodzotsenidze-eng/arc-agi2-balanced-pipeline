# ARC-AGI-2 bounded symbolic study — protocol v1

Declared 28 October 2026 before running the public evaluation benchmark.
Source base: GitHub main commit `01347aa067486bc5f5a95d50aa243a5a2877a74e`.
This is a deliberately limited CPU baseline, not a competitive-performance claim.

## Question and single comparison

Compare maximum geometric program depth 1 versus depth 2. Both arms use the
same primitives, jointly fitted color map, exact demonstration-fit gate,
deterministic ranking, output deduplication and fallbacks. Identity geometry
(depth 0) is included in both arms. A fixed program budget, not a wall-clock
timeout, defines search. Intermediate and final grids must be within 30x30.

Primitives: seven nonidentity D4 transforms; bounding box of cells differing
from each fixed color 0..9; bounding box excluding the per-grid dominant color
(ties choose smallest color); nearest-neighbor expansion by 2 or 3; whole-grid
tiling with row/column multipliers in {2,3}. An empty foreground rejects a crop.
Color maps are fitted jointly across ALL demonstration pairs after geometry.
Conflicts reject the program. Unseen test colors are unchanged. Ranking is
(geometric depth, number of changed color-map entries, lexical operator tuple,
lexical color-map tuple). No task-id-specific logic or test targets are used.

Keep the first two distinct valid predicted grids per test. One unique verified
prediction is duplicated. If no program produces a valid test prediction,
use identity and first demonstration output, explicitly marked unverified.
Exact training consistency is resubstitution fit, not a generalization score.

## Data and evaluation

Use the official ARC-AGI-2 public repository pinned to commit
`f3283f727488ad98fe575ea6a5ac981e4a188e49`, without changing the task cohort.
Run all 120 public evaluation tasks (167 test outputs at that revision) once
per arm. Prepare separate challenges and solutions; pass only challenges and
ArcTask objects to the solver. Read labels solely in the scoring process after
both arms have produced predictions. No target inspection to design programs.

Describe this as a public retrospective benchmark, not a pristine unseen
holdout: historical ARC exposure and public-data familiarity cannot be
excluded. Do not tune on evaluation results then claim fresh validation on
the same set. Identity with Kaggle's 2026 public bundle is not yet established.
Official competition scoring is separate and requires a human submission.

Primary metric: exact top-2 matches per test output / all167 test outputs.
Also report top-1, all-test-correct tasks /120, demonstration-fit coverage,
verified/fallback outputs, elapsed wall time, and paired wins and losses.
Include zero-score cases. Freeze configuration and source SHA256 manifest
before execution. Preserve original results if a later fix is necessary.

## Publication path

ARC2 code stays here; ARC3 agent/Recovery results stay in arc-agi3-agent-strategy.
A separate paper repository will own text, analysis and figures linked to
exact code versions. Retain fuller methods, controls, limitations and evidence
for a later journal manuscript; Kaggle's short writeup is a separate rendering.
Zenodo should archive reviewed releases and link code, data and paper versions.
This protocol does not perform publication, DOI creation, GPU runs or submission.
