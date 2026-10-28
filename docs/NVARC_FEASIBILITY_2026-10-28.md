# NVARC source feasibility audit — 28 October 2026

## Decision

Source is recoverable, but **not ready to run unchanged in ARC Prize 2026**.
Conditional feasibility only: resolve the runtime ABI, current mounts and reuse
terms before proposing an offline smoke run. No remote code was imported or
executed, no weights downloaded, and no GPU or evaluation was launched.

## Primary sources retrieved

- Author repository: https://github.com/1ytic/NVARC
- Author notebook: https://www.kaggle.com/code/sorokin/arc2-qwen3-unsloth-flash-lora-batch4-queue
- Read-only API: https://www.kaggle.com/api/v1/kernels/pull/sorokin/arc2-qwen3-unsloth-flash-lora-batch4-queue
- Dependency notebook: https://www.kaggle.com/code/sorokin/pip-install-unsloth-flash-patch
- Model: https://www.kaggle.com/models/sorokin/qwen3_4b_grids15_sft139
- Author methods: https://www.kaggle.com/c/arc-prize-2025/writeups/nvarc

Kaggle API retrieval succeeded without credentials. Author notebook metadata
reports version 10, Internet OFF, NVIDIA L4, lastRunTime
2026-10-25T18:43:46.2255989Z. This timestamp does not establish a successful
current run. Extracted notebook SHA256:
`506b85db66f9949022e87935ccb06a73fd78cb690883bd600bfb5c7d36c2b3af`.
Read-only source copies are outside this repository at
`/tmp/nvarc-source-audit/`; they are not a durable release artifact.

## Exact attached inputs and dependencies

Metadata lists competition `arc-prize-2025`, no datasets, kernel source
`sorokin/pip-install-unsloth-flash-patch`, and model
`sorokin/qwen3_4b_grids15_sft139/Transformers/bfloat16/1`.
The notebook embeds dependency kernelVersion sourceId `272622465` and model
instance version sourceId `627758`. Its model call uses local_files_only=True,
load_in_4bit=False and the old mount
`/kaggle/input/qwen3_4b_grids15_sft139/transformers/bfloat16/1`.

Dependency notebook retrieved as version 2 installs into `/kaggle/working`:
`unsloth==2025.9.7`, `unsloth_zoo==2025.9.9`, `numpy==2.2.6`,
`matplotlib==3.10.6`, `scikit-learn==1.7.2`, plus
`flash_attn-2.8.2+cu128torch2.8-cp311-cp311-linux_x86_64.whl` from
mjun0812/flash-attention-prebuild-wheels release v0.3.14. It patches Unsloth's
Qwen3 attention implementation. Transitive package versions are not fully
locked by these install commands. Its build requires Internet ON; the author
inference carrier attaches the already-built kernel output for offline use.
The cp311 / torch2.8 / CUDA12.8 binary is an explicit compatibility constraint.
Both metadata records name image digest
`320043e14c68293f1c946585b9257123385205a58af4b94b17d31868cae4e868`;
author notebook language metadata says Python 3.11.13.

## Runtime and necessary port work

Notebook writes arc_loader.py, arc_decoder.py, arc_solver.py and starter.py.
Launch command sets UNSLOTH_DISABLE_STATISTICS=1,
TRITON_PTXAS_PATH=/usr/local/cuda/bin/ptxas, OMP_NUM_THREADS=12 and runs
`python starter.py --end-time {global_end_time}`. The deadline is 12 hours minus
600 seconds from notebook start. Four spawned workers each select one GPU and
consume a shared task queue. Per-puzzle adaptation uses BF16 LoRA r256/alpha32,
one epoch, seed42; adapters are reset per task. DFS has a 540-second guard;
puzzle processing checks a 1200-second guard. These are not proof of a hard
end-to-end completion bound: setup/training/worker initialization need checks.

Every competition path still uses `/kaggle/input/arc-prize-2025/`. Rerun mode
reads arc-agi_test_challenges.json; ordinary mode reads evaluation challenges.
Ordinary mode explicitly queues only four task IDs. This is a development
subset, not a hidden-task shortcut, but cannot be retained as full evaluation.
Replace it with an explicit declared smoke subset/full-cohort mode, independent
of task-specific solver logic. Check current 2026 competition and model mount
paths rather than substituting a guessed prefix.

Final aggregation reads `/kaggle/inference_outputs`, selects two attempts, and
writes submission.json. Missing decoded answers default to [[0]]; therefore
file existence alone is not success. Require coverage and worker-exit checks.
Non-rerun aggregation loads evaluation solutions and benchmarks selectors:
disable/separate this branch for label-blind inference and any future frozen
comparison. No new comparison is authorized in this audit.

## Attribution, license and scientific limits

Credit Ivan Sorokin and Jean-Francois Puget / NVARC and the underlying
ARChitects implementation. GitHub repository API returned `license: null`;
the repository license endpoint returned 404. Kaggle pull metadata did not
expose a notebook or model license. Thus exact reuse/redistribution terms are
**unverified**, not presumed permissive. Inspect Kaggle license fields before
vendoring or publishing a derivative.

The authors disclose evaluation-derived synthetic data in the NVARC full
training subset. Scores on the existing 120 public evaluation tasks cannot
establish fresh generalization for this checkpoint. Any later study must state
this exposure and distinguish retrospective results from official hidden tests.

## Verified-license and prepared-carrier addendum

Root independently inspected the signed-in Kaggle UI on 28 October 2026:
main notebook Version10, dependency notebook Version2, and model
Transformers/bfloat16 Version1 each display Apache2.0. Model size is 7.27GB.
The main saved run shows success at1594.8s on L4x4, but processes its four-task
local subset; it is not full2026 runtime evidence. Dependency run shows299.4s
on T4x2. These artifact-specific license observations resolve the earlier
unknown Kaggle reuse fields; GitHub license metadata remains absent.

A separately named candidate is prepared under `nvarc_port/`, with exact
upstream notebooks, source hashes, Apache license/NOTICE, standard-library
gateway, self-contained notebook builder and five passing CPU wrapper tests.
No upstream module was imported or run during preparation. Ordinary notebook
commit only packages/compiles. Actual rerun requires explicit pinned ABI,
model/dependency mount and2026 challenge guards. Full task scheduling replaces
the development subset; label loading/benchmarking is excluded. Worker exits,
processed-task coverage, output coverage and invalid/no-candidate failures are
reported. The first cell establishes12h-minus600s; worker processes are killed
as a group on deadline. Author scientific policy is preserved.

This is a prepared baseline candidate, not a validated model or original
algorithm. Current Kaggle Python/Torch compatibility remains a blocking
preflight question. Root must independently review before any GPU step.
