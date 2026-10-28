# Continuation checkpoint — 29 October 2026

## Preserved work

- Upstream base commit: `01347aa067486bc5f5a95d50aa243a5a2877a74e`.
- Symbolic v1 protocol, source/data freeze, both prediction files, audits and
  metrics are retained unchanged. Both arms scored 0/167 outputs on 120 public
  retrospective tasks. Do not submit this grammar as a meaningful candidate or
  tune it against the revealed evaluation targets.
- An attributed, separately named NVARC carrier preserves author v10 and
  dependency v2 with SHA256 receipts, Apache-2.0 license and NOTICE. It is
  preparation only: no weights downloaded, upstream model stack imported,
  GPU run, official ARC2 submission or publication performed here.
- Root ran the complete test suite after smoke-mode preparation: **68 passed**,
  including nine CPU-only wrapper checks. Generated modules compile without importing
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

Opening the author's Copy & Edit route displays a binding ARC Prize 2025
competition-rules acceptance dialog. No acceptance was given and no author
copy was created. User confirmation is required for that route. The old 2025
dataset is not needed for the planned 2026 inference. Do not treat the rules
prompt as proof that the original runtime can or cannot be preserved by a fork.

Any smoke result is an engineering compatibility check. NVARC training includes
public-evaluation-derived material; those tasks cannot establish fresh neural
generalization. Preserve author credit and separate this baseline from the
ARC3 Recovery study. Official final Submit remains a human action.
