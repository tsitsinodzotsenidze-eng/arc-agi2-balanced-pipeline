# ARC2 B0 result and predeclared B1 implementation

## B0 official observation

On 30 October 2026, the authenticated Kaggle Submissions page and its details
modal showed **Succeeded / Public Score 31.81** for `ARC2 2026 NVARC Candidate`,
Version 2, scriptVersionId **363494251**. The UI submission timestamp was
29 October 05:53:02 PDT = 12:53:02 UTC = 16:53:02 Georgia time. Exact completion
time, hidden per-task predictions, and hidden inference/runtime breakdown were
not exposed. The transcription is in `evidence/arc2-b0-20261030/official-result.json`.

This clears the official full-submission execution feasibility gate. It does
not identify a recovery mechanism, count solved tasks, or establish novelty.
The submission is an attributed NVARC v10 baseline port. Queue/status duration
cannot be reported as model-compute time. Packaging placeholders remain
separate from the real hidden rerun output and official score.

## B1 implements the existing protocol

The 29 October protocol is preserved unchanged. B1 uses the same model,
learning rate **5e-5**, source ZIP, driver, training/decoding settings and first
cell. Only the driver-launch environment gains `PYTHONHASHSEED=42`, set before
the child Python interpreter starts. Its starter and spawned workers inherit
that environment; the final rescoring interpreter is the same seeded driver.
Setting the variable late inside a running Python process would be insufficient.

`nvarc_port/build_b1.py` hashes the completed B0 notebook before making this
single guarded launch replacement. It emits a separate notebook and complete
Cell 2 code export. It does not regenerate the B0 ZIP or modify B0 artifacts.
B1 is a controlled full-rate reference, not an exact B0 replication or an
isolated measurement of hash randomization; GPU nondeterminism and scheduling
variability remain. Later Z/H comparisons retain the original predeclared scope.

| Artifact | SHA256 |
| --- | --- |
| Completed B0 local carrier | `468d6c653869b60203c09fc1bb5db95cf1b96061a72d82c17684b730237aadb0` |
| B1 generated notebook | `926432d561121dea7914dab459374a693c08c29dc61d1105b72905625ab190e1` |
| B1 complete Cell 2 | `d416fda5ab705b0554270245221151055683dc7a1d23e9da9592a41fd754ae66` |
| Unchanged embedded driver | `1eec5bb8db719e45d2e07af80b24db9b50d2214254b79445384d4852486f5fd4` |

## Validation and Kaggle preparation

All **76 tests passed** on the local Python 3.12 host. Four new CPU checks cover
the unchanged first cell/settings and exact source bundle, full learning rate,
a rejected altered baseline, and actual child/spawn-worker hash inheritance
with a deliberately conflicting parent seed 999. This is a wiring check, not
a neural benchmark or a claim that the local host is the Kaggle runtime.
Astra independently read the implementation and approved its protocol scope;
another GPU model smoke is unnecessary for this launch-only change.

Kaggle preparation uses Copy & Edit of the successful B0 saved version, then
renames the private copy to `ARC2 2026 NVARC B1 Hash42`. Only Cell 2 is replaced.
Full editor selection/clipboard text matched all 33,527 characters exactly.
The three attached inputs remain: 2026 competition, author BF16 model V1 and
dependency utility notebook. L4 x4, Internet OFF, and Pin to original environment
were visibly confirmed. Save & Run All was requested with **Run without an
accelerator for this session**; this package run performs no model inference.
The notebook's competition accelerator remains L4 x4.

The packaging version `B1 full LR5e-5 hash42 offline 2026-10-30` completed
successfully in **124.9s**, Version 1 / scriptVersionId **363939870**. Logs
confirm the unchanged driver/source-manifest hashes, correct model mount,
dependency patch verified, and explicitly labeled packaging-only output.
The log image link resolves to the same previously preserved Docker digest
`320043e14c68293f1c946585b9257123385205a58af4b94b17d31868cae4e868`;
its generic link label says Latest Container Image despite the editor's
Pin to original environment selection. The saved logs also label the requested
accelerator L4 x4; actual resource allocation for the packaging override is
not inferred from that label. No model inference was invoked by packaging.

The official submission form is prepared with this exact version,
`submission.json`, and the B1 provenance description. The form displays one
daily submission remaining. **Final Submit has not been clicked**; this is
not evidence of B1 official submission. The user performs that final action.
Saved version: https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-b1-hash42/log?scriptVersionId=363939870
