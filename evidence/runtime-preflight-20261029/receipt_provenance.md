# Saved package receipt provenance

Candidate: private `ARC2 2026 NVARC Candidate`, Version1, successful.
Authoritative saved viewer:
https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-candidate?scriptVersionId=363290856

The saved Output tab has `nvarc-input-inspection.json` (8.88kB) and 13 output
files. Runtime is71.7s, CPU/InternetOFF. All three requested inputs are attached.
This is packaging and metadata inspection, not a model benchmark or official
competition submission. No `submission.json` was produced by package mode.

The browser file-download event timed out twice. Instead, root read the saved
notebook's rendered JSON stdout through its visible `pre` element, parsed it
and wrote `input_inspection_from_rendered_output.json`. This preserves the
receipt's JSON values, not a claim of byte-identical downloaded file content.
No private browser/session tokens or account credentials were captured.

The receipt shows exactly one dependency root:
`/kaggle/usr/lib/notebooks/sorokin/pip_install_unsloth_flash_patch`.
Its required Qwen3 patch is verified. Upstream patch SHA256:
`33ac957107cd7e4477163072ea6dff5cb2744f00067e8a7b3aea3c89c91d3ad6`.
Mounted Qwen3 file SHA256:
`0c360b0a7c7ed47c05e113c300791a502c878f3087ab24dfd949855429fe0e30`.

Model config parent:
`/kaggle/input/models/sorokin/qwen3_4b_grids15_sft139/transformers/bfloat16/1`.
Metadata includes torch2.8.0, transformers4.55.4, unsloth2025.9.7,
unsloth_zoo2025.9.9, flash_attn2.8.2 and nvidia-cuda-runtime-cu12 12.8.90.
Actual dynamic-library imports and model execution remain untested.

`pinned_gpu_base_observed.json` and its screenshot record an earlier separate
runtime-only T4x2 probe; that session was stopped. `smoke_ready.jpg` records the
separate unexecuted smoke draft, mode=smoke/budget900s/L4x4/three2026 inputs.
The historical 2025 rules prompt was declined and that fork route abandoned.
