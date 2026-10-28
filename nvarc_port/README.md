# NVARC 2026 port candidate (unvalidated)

This is an attributed baseline carrier, not a new algorithm. No GPU/model run
has been performed. Ordinary notebook execution packages and compiles only;
it does not import torch/Unsloth or request model weights. Only actual Kaggle
competition-rerun mode triggers execution. Do not submit until independently
reviewed and the runtime compatibility blocker is resolved.

`python -m unittest discover -s nvarc_port -p test_wrapper.py -v` runs CPU-only
wrapper checks. `python nvarc_port/driver.py --workdir /tmp/a-new-port-directory`
packages modules without executing them. Work directories must be fresh.

The self-contained `NVARC_2026_PORT_CANDIDATE.ipynb` includes driver/source
bytes; regenerate with `python nvarc_port/build_notebook.py` after any edits.
Its first cell starts the 12h-minus-600s deadline. Attached inputs must be the
2026 competition, author BF16 model version1 and dependency notebook version2.
GPU is disabled in the packaging notebook metadata. A later, separately
reviewed execution version must explicitly select L4 x4 in Kaggle settings.
The dependency source is prebuilt output; no online pip install is attempted.
Explicit challenge/model/dependency overrides are supported by the driver.

Execution fails unless Python3.11, Torch2.8, CUDA12.8, four L4 GPUs and the pinned
Unsloth/Flash Attention versions are present. It also fails on worker errors,
unfinished tasks, invalid output or zero generated candidates. Partial missing
candidate outputs retain the author's [[0]] fallback and are explicitly listed
in diagnostics.json. Do not describe submission completeness as inference
coverage. The original ranking and LoRA settings are preserved. All test
labels are rejected, and no label-based selector benchmark runs.

The driver checks hash-preserved vendor sources and applies guarded carrier
changes. It never executes notebook cells wholesale. Only the four attributed
Python modules run after the explicit rerun gateway and preflight. Generated
pickle files are read only from the fresh worker output directory. See NOTICE,
LICENSE and SOURCE_HASHES.json for provenance.

## Explicit smoke mode

The notebook's first cell now offers `PORT_MODE = 'package'` (default) or
`'smoke'`. Accelerator remains disabled in saved metadata. A reviewed GPU smoke
requires explicit accelerator selection and mode change; neither is performed
by this preparation. CLI equivalent: `--mode smoke --smoke-seconds 900`.
Competition execution is `--mode competition` and still requires genuine
Kaggle rerun status. No mode sets or spoofs that status.

Smoke uses only the bundled hash-checked manifest: one synthetic identity task
with two demonstration pairs and two test inputs, no test outputs. It is a
runtime/plumbing check, not accuracy evaluation. Default deadline900s, maximum
1800s; notebook deadline starts in its first cell. Output is
`smoke-predictions.json`, never `submission.json`. Model generation, adaptation,
ranking and four-worker settings remain the author's unchanged policies.

Dependency requirement: author notebook version2 / attached kernelVersion
272622465. Before importing the model stack, exact added-code blocks from its
hash-preserved Qwen3 patch must appear in the mounted qwen3.py. Diagnostics
record both upstream patch SHA256 and mounted file SHA256. This checks patch
content, not the identity of every transitive dependency; actual runtime must
still satisfy the pinned version/ABI checks. Diagnostics now enumerate missing
attempt_1/attempt_2 slots, including a lone candidate's second fallback.

A new Kaggle CPU image was independently observed by root as Python3.13.15 /
Torch2.11.0+cpu. That is incompatible with this pinned carrier; it does not
establish the GPU image's ABI. Preserve/verify the author's environment rather
than substituting package versions heuristically. No GPU run has occurred.
