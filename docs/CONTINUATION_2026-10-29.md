# Continuation checkpoint — 29 October 2026

## Preserved work

- Upstream base commit: `01347aa067486bc5f5a95d50aa243a5a2877a74e`.
- Symbolic v1 protocol, source/data freeze, both prediction files, audits and
  metrics are retained unchanged. Both arms scored 0/167 outputs on 120 public
  retrospective tasks. Do not submit this grammar as a meaningful candidate or
  tune it against the revealed evaluation targets.
- An attributed, separately named NVARC carrier preserves author v10 and
  dependency v2 with SHA256 receipts, Apache-2.0 license and NOTICE. It is
  preparation only: no author weights opened by inspection code, no model
  initialization/training/inference, official ARC2 submission or publication.
- Root ran the complete test suite after input-inspection preparation: **69 passed**,
  including ten CPU-only wrapper checks. Generated modules compile without importing
  torch/Unsloth. Packaging notebook GPU metadata is disabled.
- The paper/HCI inventory is stored separately from this code repository.
  No Zenodo deposit, new paper repository, visibility change or main merge.

## Independent port review and next gate

Astra's second read-only review found author LoRA/generation/ranking policy,
decoder keys/schema and label-free aggregation consistent. Worker completion
and process-group timeout guards are present. This is not full-runtime proof.

The explicit synthetic smoke mode, fixed challenge-only manifest, bounded
deadline, separate output, dependency-patch checks and missing-attempt
diagnostics have now been implemented and CPU-tested. No model was executed.

Remaining gates before a controlled GPU smoke run:

1. Preserve explicit smoke mode and packaging default; never spoof Kaggle rerun
   status. The smoke input is one synthetic task with two test inputs, with no
   test labels. Default budget is 900 seconds, maximum 1800 seconds.
2. Inspect actual Kaggle Python/Torch/CUDA and L4 x4 availability before model
   loading. Current carrier requires Python3.11, Torch2.8 and CUDA12.8 because
   of the attached Flash Attention binary. Stop on mismatch.
3. Attach dependency kernel version272622465 (v2). The wrapper now verifies
   exact added-code blocks from the hash-preserved upstream patch, and records
   the mounted Qwen3 file hash. This does not establish the identity of every
   transitive dependency. Missing attempt slots now appear in diagnostics.

## Actual Kaggle CPU preflight and copy gate

Root created a separate private `ARC2 NVARC Runtime Preflight CPU` notebook,
set Accelerator=None and Internet=OFF, and ran only runtime-inspection code.
The observed CPU image has Python3.13.15, torch2.11.0+cpu, transformers5.16.1;
Unsloth/zoo/Flash Attention are absent. See
`../evidence/runtime-preflight-20261029/cpu_observed.json`.
This CPU image is incompatible with the pinned author binary; it is not proof
about the GPU image. The completed interactive CPU session was stopped.
The quick-saved notebook version retains code, not its interactive outputs;
the JSON here is explicitly a transcription of the observed UI output.

The initial author-model Copy & Edit route displayed a binding ARC Prize2025
rules dialog. It was declined. That route is abandoned; no 2025 agreement or
2025 competition input is needed for the actual carrier.

## Resolved environment-copy path

Both exact upstream notebooks specify `dockerImageVersionId:31090`. Copying the
dependency-v2 utility notebook, which has no competition/data inputs, succeeds
without an old-competition rules prompt and preserves the original image.
A separate private pinned-runtime probe replaced all copied code with our own
inspection code, InternetOFF. A brief T4x2 session observed Python3.11.13 and
the exact author Docker digest. Base torch is2.6.0+cu124 / CUDA12.4 and
transformers4.52.4; author inference may obtain torch2.8 from the attached
dependency output. This still requires verification after mounting that output.
No author model code, model loading or package installation was executed in
this probe. The GPU session was stopped after the completed inspection.

The real private candidate is `ARC2 2026 NVARC Candidate`. Import of the generated
carrier metadata honored all three inputs together: ARC Prize2026 ARC-AGI-2
(source133469), dependency kernelVersion272622465, model version627758.
Accelerator=None, InternetOFF and the original image pin were visibly verified.
The first actual Kaggle CPU packaging run passed (0.193s, returncode0), compiling
the attributed modules without importing torch/Unsloth or executing the model.
The next package includes pure-stdlib mounted-input inspection, to record actual
dependency paths, package metadata and Qwen3 patch identity before model use.

## Durable saved package and pending smoke action

Saved candidate Version1 is successful (71.7s total Kaggle run):
https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-candidate?scriptVersionId=363290856

Its package-only inspection verifies the actual dependency root already used
by the wrapper, the exact required Qwen3 patch blocks and model config path.
Mounted metadata contains torch2.8.0, transformers4.55.4, Unsloth2025.9.7,
zoo2025.9.9, Flash Attention2.8.2 and NVIDIA CUDA runtime12.8.90. Thus the
base-image torch2.6 observation is not the complete attached runtime. Package
metadata and patch verification do not establish successful GPU imports or
model execution. See `receipt_provenance.md` beside the retained receipt.

The builder now also emits a separately named smoke notebook. The former
pinned-runtime probe draft was reused as private `ARC2 2026 NVARC Smoke Check`:
https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-smoke-check/edit

The UI visibly has mode=smoke, budget900s, all three current inputs, GPU L4 x4,
InternetOFF, original image pin, and Draft Session OFF. It has not been run or
submitted. The saved candidate Version1 remains package-only. Before its
first third-party model/binary execution, obtain the required browser action-
time confirmation; no old-competition rule acceptance is required.

Any smoke result is an engineering compatibility check. NVARC training includes
public-evaluation-derived material; those tasks cannot establish fresh neural
generalization. Preserve author credit and separate this baseline from the
ARC3 Recovery study. Official final Submit remains a human action.
