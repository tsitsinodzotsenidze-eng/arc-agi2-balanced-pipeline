# Reproduction and external inputs

## Source identities

Use the five self-contained `nvarc_port/*SUBMISSION.ipynb` carriers named in
`CURRENT_RESULTS.json`. All local saved notebooks have empty outputs. B1 and
B1 repeat have identical bytes; Z1 and Z repeat have identical bytes. Each
official Kaggle saved version has its own ID. The archive does not claim
byte identity with raw Kaggle exports or include hidden result predictions.

Source notebook v10 SHA-256:
`506b85db66f9949022e87935ccb06a73fd78cb690883bd600bfb5c7d36c2b3af`.
Dependency notebook v2 SHA-256:
`60f44fd0ab45a7b28a466714744039191b585e222a5c7ee7467bc936314dc1d8`.
Both exact source notebooks and `SOURCE_HASHES.json` are retained in
`nvarc_port/vendor/` and `nvarc_port/` respectively.

## Required external assets and environment

- Competition: `arc-prize-2026-arc-agi-2`, source ID133469.
- Model: `sorokin/qwen3_4b_grids15_sft139/Transformers/bfloat16/1`, model
  instance version627758. Model weights are excluded from the archive.
- Dependency notebook: `sorokin/pip-install-unsloth-flash-patch`, Version2,
  kernelVersion272622465. Its built distributions are excluded; obtain the
  authorized original output and preserve each package's own notices.
- Python3.11, four L4 GPUs, Internet OFF, original image ID31090, observed
  digest `gcr.io/kaggle-gpu-images/python@sha256:320043e14c68293f1c946585b9257123385205a58af4b94b17d31868cae4e868`.
- Runtime checks expect Torch2.8/CUDA12.8, Unsloth2025.9.7,
  UnslothZoo2025.9.9 and FlashAttention2.8.2. Do not infer compatibility
  with a current default Kaggle image from notebook metadata alone.

Saved metadata requests these resources; dated live preflight receipts record
what was actually inspected. Runtime compatibility depends on obtaining the
external inputs. This archive is a source/evidence package, not a bundled
model image or claim of a new independent complete rerun.

## Execution modes

Ordinary execution performs package/input inspection and explicitly labeled
placeholder export. Those `[[0]]` outputs are file-selection aids, not model
predictions. Model inference occurs through the genuine competition-rerun
gateway; the carrier does not spoof that status. Bounded synthetic smoke and
the LR0 invariance probe are separate development checks, not official scores.

The first cell starts the existing 12-hour-minus-600-second deadline. B1/Z
set `PYTHONHASHSEED=42` before the child driver launches. Z keeps trainer and
optimizer computations and sets LR0. The original model and decoder policy
are retained. Running a new inference experiment requires separately planned
compute; none was launched to prepare this publication checkpoint.

## Validation already available

The research branch's existing pytest workflow passed on Python3.10 and3.11.
Archive preparation checks JSON/AST structure, notebook identities, retained
source hashes and archive manifests. These checks do not execute embedded
neural code, deserialize model objects or establish hidden benchmark accuracy.

See `THIRD_PARTY_NOTICES.md` for attribution and dated license observations.
