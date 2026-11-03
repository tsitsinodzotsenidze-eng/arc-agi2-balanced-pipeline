# Parameter Updates and Repeatability in an Attributed NVARC Port for ARC-AGI-2

**ARC Prize 2026 — ARC-AGI-2 Solution Writeup**\
**Author:** Tsitsino Dzotsenidze\
**Status:** Research draft — all five public results recorded; final private leaderboard results unknown

## Research question

This study investigates the relationship between test-time parameter updates and observed ARC-AGI-2 performance. Specifically, it asks whether the performance contrast between a configuration that permits parameter updates and a zero-learning-rate configuration persists across repeated evaluations.

The project builds on an attributed port of the NVARC solution developed by **Ivan Sorokin and Jean-Francois Puget**. It is not presented as an independently invented solver.

## Method and experimental configurations

The study compares configurations based on the NVARC solution's Qwen3-based inference and adaptation workflow.

**B1 Hash42** retains the specified learning rate of 5 × 10⁻⁵ and uses `PYTHONHASHSEED=42`.

**Z1 Zero Update** sets the learning rate to zero while retaining trainer and optimizer computations, the original model and decoder policy, and the specified hash seed. This design aims to distinguish the role of intended parameter updates from the continued execution of the surrounding training workflow.

Two repeat submissions were prepared:

- **B1 Repeat:** byte-identical source code to B1 Hash42.
- **Z Repeat:** byte-identical source code to Z1 Zero Update.

Identical source code does not establish identical runtime trajectories or eliminate all possible execution variability.

The earlier **B0/V2** submission is retained as a historical reference rather than a matched control because its Python hash seed was not fixed.

## Observed public results

| Configuration     | Kaggle scriptVersionId | Public score         | Status                   |
| ----------------- | ---------------------- | -------------------- | ------------------------ |
| B0/V2, historical | 363494251              | 31.81                | Succeeded                |
| B1 Hash42         | 363939870              | 30.97                | Succeeded                |
| Z1 Zero Update    | 364031423              | 9.58                 | Succeeded                |
| B1 Repeat         | 364031921              | 30.56                | Succeeded (after deadline) |
| Z Repeat          | 364032699              | 9.58                 | Succeeded (after deadline) |

B1 Repeat produced a displayed public score of 30.56, compared with 30.97 for the original B1 Hash42 submission, a difference of 0.41 points. Its evaluation completed after the official competition deadline; therefore, this observation is distinguished from deadline-eligible competition results.

Z Repeat produced a displayed public score of 9.58, matching Z1 at the displayed two-decimal precision. Kaggle labels this result `Succeeded (after deadline)`. The original B1–Z1 difference is 21.39 public-score points; the B1 Repeat–Z Repeat difference is 20.98 points. Agreement of rounded aggregate scores does not establish identical task-level predictions.

## Independent engineering verification

A separate check completed 128 steps and inspected 506 adapter tensors. All inspected tensors remained finite and unchanged.

This check supports parameter invariance within the observed execution segment. It terminated before decoding and therefore does not establish prediction accuracy or full end-to-end behavioral equivalence.

## Interpretation

The observed public scores show a substantial descriptive difference between B1 Hash42 and Z1 Zero Update. However, one initial observation per configuration does not support a claim of statistical significance or a fully identified causal mechanism.

The B1 Repeat result provides an additional observation of the updating configuration under byte-identical source code. Z Repeat supplies the corresponding observation of the zero-update configuration: the two B1 scores are 30.97 and 30.56, and both displayed Z scores are 9.58.

The substantial contrast recurs across the two recorded evaluations per configuration. This is descriptive replication at the rounded public-score level; two observations per configuration do not establish a reliable variance estimate, statistical significance, general repeatability or a uniquely identified causal mechanism. Possible runtime variability and other uncontrolled differences must still be considered.

Missing, interrupted, or post-deadline evaluations will be reported transparently rather than retrospectively excluded.

## Provenance, attribution and reproducibility

The original NVARC work is credited to Ivan Sorokin and Jean-Francois Puget.

Primary source: [NVARC research repository](https://github.com/1ytic/NVARC).

Original submission notebook: [arc2-qwen3-unsloth-flash-lora-batch4-queue](https://www.kaggle.com/code/sorokin/arc2-qwen3-unsloth-flash-lora-batch4-queue).

Saved Kaggle versions, parameter settings, source hashes, runtime evidence and licensing notices are preserved in the [project GitHub repository](https://github.com/tsitsinodzotsenidze-eng/arc-agi2-balanced-pipeline). The corresponding Zenodo record remains a preparation draft with reserved DOI 10.5281/zenodo.23895859; publication is not claimed.

The archive will distinguish original NVARC material, attributed modifications, development diagnostics, deadline-eligible submissions and post-deadline research observations.

## Research contribution

The contribution is a documented, comparative study of parameter-update configurations in an attributed ARC-AGI-2 solver, including explicit repeat submissions and reproducibility evidence.

The results are preliminary. They provide an empirical basis for studying adaptation and run-to-run stability, not proof that a single parameter-update mechanism explains the entire observed score difference.
