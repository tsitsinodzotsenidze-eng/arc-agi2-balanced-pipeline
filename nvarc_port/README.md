# NVARC 2026 port candidate

The first bounded synthetic GPU smoke completed successfully on 29 October 2026:
one task, both first-attempt outputs equal the declared identity inputs;
second-attempt slots retain the author's [[0]] fallback. Model pipeline
wall time 429.719s. This validates small synthetic runtime plumbing, not ARC2
benchmark accuracy, full hidden-cohort completion or official scoring.
See `../evidence/smoke-20261029/` for the exact executed-source binding.

The builder produces three distinct artifacts:

| Notebook | Ordinary execution | Accelerator request |
| --- | --- | --- |
| `NVARC_2026_PORT_CANDIDATE.ipynb` | CPU package/input inspection | None |
| `NVARC_2026_SMOKE_CHECK.ipynb` | Fixed synthetic smoke, budget900s | L4x4 |
| `NVARC_2026_SUBMISSION_CANDIDATE.ipynb` | Package + labeled submission placeholder | L4x4 |

The submission carrier uses genuine competition-rerun mode for model inference;
ordinary packaging only creates the selectable file. It never reports those
[[0]] placeholders as predictions or evidence of performance. Final official
Submit is a separate human action.

This is an attributed baseline carrier, not a new algorithm. A separate brief
T4x2 session ran only our runtime inspector and was stopped. The later L4x4
synthetic smoke initialized/trained/decoded the model and its session was
stopped after archiving results. Ordinary package-mode notebook
execution packages and compiles only;
it does not import torch/Unsloth or request model weights. Only actual Kaggle
competition-rerun mode or explicit bounded smoke mode triggers model execution.
Astra independently reviewed the carrier and exporter. The tiny smoke resolves
the observed runtime compatibility gate; it does not validate hidden-cohort
completion or predict an official score.

`python -m unittest discover -s nvarc_port -p test_wrapper.py -v` runs CPU-only
wrapper checks. `python nvarc_port/driver.py --workdir /tmp/a-new-port-directory`
packages modules without executing them. Work directories must be fresh.

The self-contained `NVARC_2026_PORT_CANDIDATE.ipynb` includes driver/source
bytes; regenerate with `python nvarc_port/build_notebook.py` after any edits.
Its first cell starts the 12h-minus-600s deadline. Attached inputs must be the
2026 competition, author BF16 model version1 and dependency notebook version2.
GPU is disabled in the packaging notebook metadata. A later, separately
reviewed execution version must explicitly select L4 x4 in Kaggle settings.
The generated metadata names only the 2026 competition (source133469), exact
dependency kernelVersion272622465, model627758 and original Docker image31090.
Both vendored upstream notebooks name image31090. A competition-free copy of
the dependency notebook can preserve this image without attaching ARC2025.
Verify all three inputs and the environment in Kaggle after import; metadata
is a request, not proof that the current UI honored it.
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
Python modules run after the explicit mode gateway and preflight. Generated
pickle files are read only from the fresh worker output directory. See NOTICE,
LICENSE and SOURCE_HASHES.json for provenance.

## Explicit smoke mode

The builder also produces a separately named `NVARC_2026_SMOKE_CHECK.ipynb`:
mode=smoke, budget900s, requested L4 x4, InternetOFF, the same exact three inputs
and image31090. It is for a separate private smoke notebook only. Actual
competition rerun rejects this mode; it must never be submitted for scoring.

The main candidate's first cell offers `PORT_MODE = 'package'` (default) or
`'smoke'`. Accelerator remains disabled in saved metadata. A reviewed GPU smoke
requires explicit accelerator selection and mode change. The separately named
smoke notebook supplies those requested settings. CLI equivalent: `--mode smoke --smoke-seconds 900`.
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
than substituting package versions heuristically. A competition-free dependency
notebook copy successfully preserved Python3.11 and the exact original Docker
digest in a brief runtime-only T4x2 probe. Base torch2.6/CUDA12.4 differed from
the author inference requirements; attached dependency output is inspected
separately before importing its torch2.8 build. The completed synthetic smoke
subsequently verified this import path and GPU execution.

Packaging now includes `--inspect-inputs`: source/package metadata is inspected
only under `/kaggle/input` and `/kaggle/usr/lib/notebooks`. The report records
matching dependency roots, Qwen3 patch receipts, installed-distribution metadata
versions and model config parent paths in
`/kaggle/working/nvarc-input-inspection.json`. It does not import torch,
Unsloth or the model, and does not open weights. This establishes actual mount
locations before any authorized GPU check. Missing/invalid patch candidates
are reported explicitly.

`--export-placeholder` is an explicit package-only option, disabled by default.
It reads only current2026 test challenges and writes schema-valid [[0]] attempts
for file selection, plus `submission-placeholder-provenance.json` with source/
challenge hashes and task/test counts. This is explicitly not inference or
performance evidence. It refuses genuine reruns and test labels. Competition
execution removes any prior target and placeholder receipt before mount checks
or preflight; only validated successful inference writes the real payload,
using atomic replacement. Smoke remains separate. Only `NVARC_2026_SUBMISSION_CANDIDATE.ipynb` enables this flag; the CPU
inspection and synthetic smoke artifacts leave it disabled. Astra reviewed
the builder integration and embedded driver after this change.
