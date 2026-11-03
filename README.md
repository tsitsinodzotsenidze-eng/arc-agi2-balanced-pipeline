# ARC-AGI-2: NVARC update-sensitivity study (2026)

This repository preserves an attributed port of the NVARC solver and a small
study of test-time parameter updates. Creator of the port, study and archive:
Tsitsino Dzotsenidze. Upstream NVARC authors: Ivan Sorokin and Jean-Francois
Puget (NVIDIA KGMoN), with underlying ARChitects lineage. The port is not claimed
as a newly invented solver.

## Current publication checkpoint — 3 November 2026

The official Kaggle Submissions page was inspected after the deadline on
3 November. The scores below are rounded **public** scores, not final private
scores. B1 Repeat completed with an explicit after-deadline label; Z Repeat
was still running. The original 2 November archive is preserved unchanged.

| Arm | Saved scriptVersionId | Configuration | Public score / observed state |
| --- | --- | --- | --- |
| B0 / V2 | 363494251 | LR 5e-5; Python hash seed not pinned | 31.81, Succeeded |
| B1 | 363939870 | LR 5e-5; hash42 | 30.97, Succeeded |
| Z1 | 364031423 | LR 0; hash42; trainer computations retained | 9.58, Succeeded |
| B1 repeat | 364031921 | Exact B1 source repeat | 30.56, Succeeded (after deadline) |
| Z repeat | 364032699 | Exact Z1 source repeat | Pending verification; Running |

The B1-Z1 difference is 21.39 public-score points. B1 Repeat is 0.41 points
below B1 and 20.98 above the single Z1 observation. These are descriptive
contrasts; Z repeat remains pending. Exact source repeats assess stability; identical source
and hash42 do not guarantee deterministic GPU execution. B0 is a historical
reference, not an exact B1 replicate. Unfinished or failed runs are not zero
scores. Packaging runs and their placeholder files are not performance data.

- [Machine-readable current results](publication/CURRENT_RESULTS.json)
- [B1 repeat result and deadline status](publication/B1_REPEAT_RESULT_2026-11-03.md)
- [Results, intended analysis and limitations](publication/RESULTS_AND_LIMITATIONS.md)
- [Reproduction and external dependencies](publication/REPRODUCING.md)
- [Source attribution and license scope](publication/THIRD_PARTY_NOTICES.md)
- [Technical Solution Writeup draft](publication/SOLUTION_WRITEUP_DRAFT.md)
- [Claim-to-evidence ledger](publication/CLAIMS_LEDGER.md)
- [Zenodo description draft](publication/ZENODO_DESCRIPTION.md)
- [Publication status](publication/RELEASE_STATUS.md)

## Study design and preservation

The dated [29 October protocol](docs/ARC2_UPDATE_STRENGTH_PROTOCOL_2026-10-29.md),
[30 October amendment](docs/ARC2_PRIORITY_AMENDMENT_2026-10-30.md), and
[31 October priorities](docs/ARC2_FINAL_WINDOW_PRIORITY_2026-10-31.md) preserve
the design history. A half-rate arm was considered and later deferred in favor
of exact B1 and Z repeats. That history is not rewritten after observing scores.

A separate synthetic engineering probe completed 128 optimizer steps and
found all 506 inspected adapter tensors finite and exactly unchanged at LR0.
It stopped before decoding and is not benchmark-accuracy evidence.

The standalone [NVARC saved carriers](nvarc_port/) contain the submitted source
payloads. The B1 and B1-repeat local notebooks are byte-identical, as are Z1
and Z-repeat. Notebook hashes and Kaggle saved-version IDs are separate
identities; exported Kaggle notebook metadata is not claimed byte-identical.

## Earlier symbolic pilot

The earlier public symbolic depth1/depth2 pilot, reported at
[0/167 test outputs](docs/RESULTS_PUBLIC_V1_2026-10-28.md), remains a distinct
coverage study. It is not the solver responsible for the NVARC Kaggle scores.
Earlier scaffold and preparation notes describe their dated checkpoints;
the current observed official status is the table above.

## Archive scope

The proposed deposit contains NVARC carrier source, exact vendored notebook
sources, original study documents and selected development receipts. Model
weights, installed dependency distributions and hidden evaluation tasks or
predictions are external and are not redistributed in that deposit. Re-running
the model requires separately obtained authorized inputs and a compatible GPU
environment. This checkpoint does not claim a new complete hidden rerun.

Original NVARC wrapper additions and publication documents use Apache-2.0 as
described in [nvarc_port/LICENSE](nvarc_port/LICENSE). Third-party artifacts keep
their own terms and notices. This is not a blanket relicensing of all content
or an assertion that every ARC Prize licensing requirement is satisfied.

This technical record is separate from the joint ARC-AGI-2/ARC-AGI-3 manuscript,
*Two Worlds, One Challenge: How AI Solves Unfamiliar Problems*.
