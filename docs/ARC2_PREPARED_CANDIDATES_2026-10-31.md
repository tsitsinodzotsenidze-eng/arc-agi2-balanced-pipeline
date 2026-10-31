# ARC2 prepared candidates — 31 October 2026 Georgia time

The final-window review with Astra preserves the order below even if only four
official runs finish. B1 repeat is the preferred next run after Z1; Z repeat
remains fifth. Cici reserves 2 November evening for publication preparation.
See [the recorded rationale](ARC2_FINAL_WINDOW_PRIORITY_2026-10-31.md).

All three future private carriers have completed packaging successfully. Their rendered saved code cells match the durable source artifacts exactly. These short packaging runs produce a file-selection placeholder, not predictions or performance evidence. The hidden competition rerun selects the inference path. No additional official submission was made by the agent.

At the 31 October follow-up, B1 (script 363939870) is officially Succeeded at public score 30.97. B0 remains Succeeded at 31.81. The earlier packaging receipt preserves the historical observation while B1 was still running. The separate real-model null-update check passed in 317.1 seconds (script 363962649): all 128 trainer/optimizer steps completed and all 506 adapter tensors remained finite and exactly unchanged. It stopped before decoding.

| Planned order | Carrier | Saved version name | Script version | Packaging |
| --- | --- | --- | --- | --- |
| 3 | [ARC2 2026 NVARC Z1 Zero Update](https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-z1-zero-update/output?scriptVersionId=364031423&select=submission.json) | Z1 LR0 hash42 offline 2026-10-31 | 364031423 (V1) | Succeeded, 70.1 s |
| 4 | [ARC2 2026 NVARC B1 Repeat](https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-b1-repeat/output?scriptVersionId=364031921&select=submission.json) | B1 repeat LR5e-5 hash42 2026-10-31 | 364031921 (V1) | Succeeded, 57.6 s |
| 5 | [ARC2 2026 NVARC Z Repeat](https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-z-repeat/output?scriptVersionId=364032699&select=submission.json) | Z repeat LR0 hash42 2026-10-31 | 364032699 (V1) | Succeeded, 118.9 s |

Use the order Z1 → B1 repeat → Z repeat. The B1 and Z repeat code is identical to its corresponding reference. Keep the original attributed model/decoder, hash42, all three inputs, L4x4 metadata, Internet OFF and pinned original image. The CPU-only save override was explicitly selected for each packaging session. The resulting logs retain the expected original container digest.

## Human submission handoff

Only continue when B1 has finished and Kaggle permits another submission. Do not cancel B1 or submit a packaging file through an unrelated upload path.

1. Open the next carrier link above and choose its menu → Submit to Competition.
2. Select the exact saved version listed above and output `submission.json`; use the corresponding description below.
3. Cici reviews the selection and clicks final Submit. The agent does not perform that action.

| Carrier | Description |
| --- | --- |
| Z1 | Z1 predeclared null-update contrast: attributed NVARC v10 port; LR 0; hash42; trainer computations retained; original model/decoder policy; pinned offline runtime; L4x4. Separate real-model parameter-invariance check passed. |
| B1 repeat | Exact B1 reference repeat: attributed NVARC v10 port; LR 5e-5; hash42; unchanged code, model and decoder; pinned offline runtime; L4x4. Predeclared run-variability observation. |
| Z repeat | Exact Z1 null-update repeat: attributed NVARC v10 port; LR 0; hash42; unchanged code, model and decoder; pinned offline runtime; L4x4. Predeclared replication of the B1 versus Z contrast. |

## Interpretation

Z preserves examples, prompting, augmentation and training computations while nulling per-task parameter updates. It does not remove all learning or reasoning. Interpret the complete pipeline under the same nominal time constraint; realized search and time allocation can differ. B1/Z1 alone are one descriptive contrast. Two runs per condition remain too few for reliable significance or mechanism claims. Preserve equal/negative results and failures. Five completed official runs is a target subject to platform and calendar limits.

Exact saved-version source hashes, input inspection and packaging receipts are in `evidence/KAGGLE_PREPARED_CANDIDATES_2026-10-31.json`. This is a labeled UI transcription, not a backend download. The source/probe checkpoint preceding this handoff is commit `d2767814074d0b8b18821841febf210c4eec1596`.

## 31 October live preflight and human handoff

The immutable Z1 Version 1 / script 364031423 was re-read from Kaggle. Both rendered source cells match the preserved artifact exactly; its saved logs retain the original container digest and L4x4. The model V1, competition input and verified dependency inspection match the earlier packaging receipt. The official submission form selects `ARC2 2026 NVARC Z1 Zero Update`, exact version label `Z1 LR0 hash42 offline 2026-10-31`, and `submission.json`; the predeclared description is filled. Kaggle reports one daily submission remaining at this observation. Final Submit remains the human action and has not been performed by the agent. No candidate code or configuration was changed after observing B1 score.

B1 is 0.84 public-score points below historical B0. This is an observed difference between single runs with different hash settings, not an identified causal hash effect. The prospectively declared next contrast remains B1 versus Z1, followed by the two exact reference repeats. See `evidence/ARC2_B1_RESULT_Z1_PREFLIGHT_2026-10-31.json` for the result and form UI transcription, source hashes and packaging receipt.
