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
- Root ran the complete test suite after packaging: **64 passed**, including
  five CPU-only wrapper checks. Generated modules compile without importing
  torch/Unsloth. Packaging notebook GPU metadata is disabled.
- The paper/HCI inventory is stored separately from this code repository.
  No Zenodo deposit, new paper repository, visibility change or main merge.

## Independent port review and next gate

Astra's second read-only review found author LoRA/generation/ranking policy,
decoder keys/schema and label-free aggregation consistent. Worker completion
and process-group timeout guards are present. This is not full-runtime proof.

Before a controlled GPU smoke run:

1. Add explicit ordinary-run smoke mode with a fixed challenge-only manifest,
   short deadline and separate outputs. Default stays packaging; full hidden
   competition-rerun mode remains gated. Never spoof Kaggle rerun status.
2. Inspect actual Kaggle Python/Torch/CUDA and L4 x4 availability before model
   loading. Current carrier requires Python3.11, Torch2.8 and CUDA12.8 because
   of the attached Flash Attention binary. Stop on mismatch.
3. Pin dependency kernel version272622465 (v2) and verify the mounted Qwen3
   patch by hash or exact patch content, not only package versions. Improve
   diagnostics to count missing attempts, including the author's second [[0]]
   fallback when only one answer exists.

Any smoke result is an engineering compatibility check. NVARC training includes
public-evaluation-derived material; those tasks cannot establish fresh neural
generalization. Preserve author credit and separate this baseline from the
ARC3 Recovery study. Official final Submit remains a human action.
