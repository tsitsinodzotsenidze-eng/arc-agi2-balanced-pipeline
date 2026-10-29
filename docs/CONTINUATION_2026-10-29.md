# Continuation checkpoint — 29 October 2026

## Preserved research

Upstream base: `01347aa067486bc5f5a95d50aa243a5a2877a74e`.
The frozen symbolic v1 protocol, source/data freeze, predictions, audits and
metrics remain unchanged. Both depth arms scored 0/167 outputs on 120 public
retrospective tasks. This records limited grammar coverage; do not tune this
frozen pilot against its revealed evaluation targets.

The NVARC carrier is an attributed existing baseline, separate from the
symbolic pilot and the ARC3 Recovery study. Exact author v10 and dependency v2
sources, SHA256 receipts, Apache-2.0 license and NOTICE are retained.
The paper/HCI inventory is separate. No Zenodo deposit, new paper repository,
visibility change or main-branch merge has been performed.

## Completed runtime gate

The first separate, authorized, bounded synthetic GPU smoke passed:
429.719 seconds, worker return code 0, 1/1 tasks completed, model candidates
for 2/2 test inputs. Both first attempts equal the fixed identity inputs;
both second attempts are the author's `[[0]]` fallback. All GPU sessions were
stopped afterward. See [evidence](../evidence/smoke-20261029/README.md).

Actual imports confirmed Python 3.11.13, Torch 2.8.0+cu128, Transformers 4.55.4,
Unsloth 2025.9.7, CUDA 12.8 and Flash Attention 2. This resolves the observed
runtime gate only; hidden-cohort completion and official scoring are untested.
The executed historical driver SHA256 is
`345ce2feb474870fad0976694caf71478441e3ad071aec26028e337487fdf109`,
preserved at remote commit `0b4dc87d7ebb8d9ed244d14566b912965d4f2cdd`.
Current generated artifacts contain a later CPU-tested packaging exporter.

## Submission carrier

The private notebook is `ARC2 2026 NVARC Candidate`:
https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-candidate

Version 1 (script363290856) preserved successful CPU packaging/input inspection
but lacked selectable `submission.json`. It must not be presented as ready.
`NVARC_2026_SUBMISSION_CANDIDATE.ipynb` now requests L4 x4, Internet OFF,
image31090 and all three exact inputs: 2026 competition source133469,
dependency kernelVersion272622465 and model version627758.

Its ordinary package run writes a clearly labeled schema-valid `submission.json`
placeholder and separate provenance receipt, for Kaggle file selection only.
A genuine competition rerun ignores that packaging flag, removes stale target
and placeholder receipt before preflight, processes the current challenge
cohort and atomically writes validated inference output on success. It never
spoofs Kaggle rerun status. Smoke output remains separately named.
Astra independently reviewed this builder/exporter integration with no material
blocker. Saved Version2 script363494251 completed successfully in119.5seconds, with
L4x4 and selectable submission.json. Its prepared competition form accepted
the selected version/file, showed one remaining daily attempt and was left
for human final Submit. See `../evidence/submission-package-20261029/`.
This re-import required root to restore the three exact inputs through the UI;
do not assume that import metadata alone will preserve attachments.

## Tests and CI repair

The complete local suite passed 72 tests after the exporter and package-discovery
fix; 13 are CPU-only NVARC wrapper checks. The added exporter checks cover
multi-test cardinality/provenance, refusal of reruns/test labels, stale-output
removal before injected preflight failure and atomic writes.

Three GitHub failure emails referred to PR workflow runs at 04d5cec, 3ed2ef3
and 0b4dc87, not a Kaggle submission. Latest run40767338231 stopped in
`Install test dependencies`, before any tests ran. Setuptools rejected automatic
flat-layout discovery of evidence, nvarc_port and arc_agi2_pipeline. The project
now explicitly includes only `arc_agi2_pipeline*` in its Python distribution;
the attributed notebook carrier/evidence remain separate repository artifacts.
Local editable installation succeeds. Remote run40874952780 passed on commit
7a918d461c039616caa23fb00aa4c427ffc0cd83: Python3.10 and Python3.11 each
passed all72 tests. See `../evidence/ci-20261029.json`.

## Environment-copy history

The initial author-model Copy & Edit route requested binding ARC Prize2025
rules; it was declined. A competition-free dependency-v2 notebook copy
preserved original image31090 without the old competition input or agreement.
A brief runtime-only T4x2 probe observed Python3.11 and the original Docker
image; it was stopped. The base torch2.6/CUDA12.4 observation was superseded
for actual model execution by the attached torch2.8/CUDA12.8 dependency output.
A separate fresh CPU image was Python3.13/Torch2.11 and unsuitable for this pin.
The current carrier uses only the 2026 competition. ARC3 was not modified.

NVARC training includes public-evaluation-derived material, so those public
items cannot establish fresh neural generalization. Preserve source credit.
Official final Submit remains exclusively a human action.
