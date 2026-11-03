# Source attribution, artifact-specific licenses and publication boundaries
**Updated:** 3 November 2026

## Research and upstream credit

Original NVARC solution: **Ivan Sorokin and Jean-Francois Puget** (NVIDIA KGMoN), with acknowledged underlying ARChitects lineage. See the [original NVARC repository](https://github.com/1ytic/NVARC). This research contributes an **attributed ARC Prize 2026 execution port**, a controlled update-sensitivity comparison, source-identical repeats, bounded engineering checks and provenance documentation; it **does not claim invention of NVARC**.

| External artifact | Exact reference | Rights evidence as of this review |
| --- | --- | --- |
| NVARC author Notebook, **Version 10** | [`sorokin/arc2-qwen3-unsloth-flash-lora-batch4-queue`](https://www.kaggle.com/code/sorokin/arc2-qwen3-unsloth-flash-lora-batch4-queue); retained source: `nvarc_port/vendor/author-v10.ipynb` | **Apache-2.0** was directly readable on the public Kaggle Version 10 page during the recent review; 28 October signed-in artifact check also recorded Apache-2.0. |
| Dependency Notebook, **Version 2** | [`sorokin/pip-install-unsloth-flash-patch`](https://www.kaggle.com/code/sorokin/pip-install-unsloth-flash-patch); retained source: `nvarc_port/vendor/dependency-v2.ipynb` | **Apache-2.0 according to the 28 October signed-in Kaggle license-field record**, `nvarc_port/NOTICE`. Its specific current public license field was **not independently readable** in the latest check. |
| External Qwen3 model, **Transformers/bfloat16/1** | [`sorokin/qwen3_4b_grids15_sft139`](https://www.kaggle.com/models/sorokin/qwen3_4b_grids15_sft139/transformers/bfloat16/1); **weights excluded** | **Apache-2.0 according to the 28 October signed-in Kaggle license-field record**. Its specific current public license field was **not independently readable** in the latest check; this is not a new model-license certification. |

The original 28 October observation is preserved in `nvarc_port/NOTICE`. Recorded vendored Notebook SHA-256 hashes are preserved in `nvarc_port/SOURCE_HASHES.json`. The upstream GitHub root `LICENSE` was not found in a separate check; this does **not** negate a specific Kaggle artifact's declared license and is not a substitute for examining that declaration. The model's upstream terms and any downstream re-distribution rights should not be inferred only from a notebook label.

## Rights and packaging policy

- Apache License 2.0 full text is retained at `nvarc_port/LICENSE`. Our authorized original wrappers and publication text are released under that license; any included upstream notebook-derived material keeps its **own attribution and applicable notices**.
- Do not interpret a repository license as relicensing third-party Notebook source, model weights, pretrained assets, installers, FlashAttention, Unsloth packages or runtime dependencies. Installed package distributions and model weights are **not** included in the selected deposit.
- **Before public release**, Work should check the two version-specific license fields again in a signed-in Kaggle session if public licensing scope depends on them. Preserve a dated receipt or explicitly state that the 28 October inspection is the latest direct evidence.
- The historical symbolic scaffold remains separate. The proposed Zenodo source/evidence package is scoped to the NVARC research carriers and selected receipts rather than every repository file.
- Kaggle/ARC Prize competition-specific solution-disclosure requirements and third-party redistributability are **separate compliance questions**; this audit is not a blanket certification of either.

See [the independent 3 November source and evidence review](INDEPENDENT_SOURCE_EVIDENCE_AUDIT_2026-11-03.md) and [the reproduction instructions](REPRODUCING.md).
