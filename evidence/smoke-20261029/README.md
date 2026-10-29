# Synthetic GPU runtime smoke — 29 October 2026 (Georgia time)

The user explicitly authorized the first third-party model/binary execution.
A separate private `ARC2 2026 NVARC Smoke Check` draft ran one fixed synthetic
identity task (two demonstrations, two test inputs; no test-output labels),
with a 900-second budget, L4 x4, Internet OFF and author image 31090.

The model pipeline completed in **429.719 seconds**, return code **0**.
All four worker processes completed; 1/1 tasks and 2/2 test outputs had model
candidates. Each first attempt exactly equals its declared identity input.
Both second-attempt slots contain the author's `[[0]]` fallback; therefore
this is not evidence of two model-generated attempts per output.
Training/decoding for the one task took about 81.7 seconds. Runtime imports
confirmed Python 3.11.13, Torch 2.8.0+cu128, Transformers 4.55.4,
Unsloth 2025.9.7, CUDA 12.8 and Flash Attention 2. The session was stopped.
No official competition submission was made.

## Evidence binding

- `launch.json`: local launch receipt with source/artifact hashes.
- `receipt_from_rendered_output.json`: exact JSON parsed from the read-only
  receipt cell's rendered output after completion.
- `runtime_rendered_log.txt`: text extracted from the editor's rendered output
  blocks. This is a UI export, not an original downloaded backend log.
- Executed driver SHA256:
  `345ce2feb474870fad0976694caf71478441e3ad071aec26028e337487fdf109`.
- The historical executed notebook/driver are preserved at GitHub commit
  `0b4dc87d7ebb8d9ed244d14566b912965d4f2cdd`.

The packaging-only exporter was added **after** this smoke. Current generated
notebooks embed that updated driver; they are not byte-identical to the
historical executed artifact. CPU tests and Astra's separate integration review
cover the exporter, including stale-output removal before genuine rerun
preflight. No second model run was performed to archive outputs.

This is engineering compatibility evidence only, not ARC2 benchmark accuracy,
full hidden-cohort completion, a competition score, or fresh generalization.
