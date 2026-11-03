# Parameter Updates and Repeatability in an Attributed NVARC Port for ARC-AGI-2

**ARC Prize 2026 — ARC-AGI-2 technical Solution Writeup (publication-ready draft)**  
**Author:** Tsitsino Dzotsenidze — ORCID `0000-0002-9432-1803`  
**Date:** 3 November 2026  
**Status:** Reviewed text; accompanying GitHub/Zenodo source/evidence record published. Kaggle Writeup publication **not yet claimed**.

## Research question and attribution

The research task is to examine performance under parameter-update policies while retaining the surrounding trainer and optimizer workflow. Does the public-score advantage of an update-permitting configuration over a zero-learning-rate configuration persist across repeated evaluations of the specified NVARC port?

The directional hypothesis is that the update-permitting configuration achieves higher public scores than the zero-learning-rate configuration in both the initial and repeated evaluations. This manuscript formulation clarifies the research question; the original dated protocol and amendments remain the record of when experimental decisions were made.

This project is an implementation, update-sensitivity and repeatability study of the NVARC system developed by **Ivan Sorokin and Jean-Francois Puget** (NVIDIA KGMoN), with its acknowledged ARChitects lineage. We do **not** claim to have invented NVARC or its underlying solver. Our distinct contributions are a documented ARC Prize 2026 execution port, a dated update-strength study with a controlled hash seed, exact-source repeat carriers, a bounded independent parameter-invariance probe, and a source-linked record of public results and limitations.

Primary original sources: [NVARC authors' research repository](https://github.com/1ytic/NVARC) and [Sorokin's original Kaggle Notebook, Version 10](https://www.kaggle.com/code/sorokin/arc2-qwen3-unsloth-flash-lora-batch4-queue). The relevant external dependency Notebook is [Version 2](https://www.kaggle.com/code/sorokin/pip-install-unsloth-flash-patch); model reference: [qwen3_4b_grids15_sft139 / Transformers / bfloat16 / 1](https://www.kaggle.com/models/sorokin/qwen3_4b_grids15_sft139/transformers/bfloat16/1).

## Design and intervention

The principal comparison uses the same attributed Qwen3-based NVARC carrier and nominal training and inference policy, with `PYTHONHASHSEED=42` set in the child-driver environment before launch:

- **B1 (updating reference):** learning rate `5e-5`.
- **Z1 (zero-update contrast):** learning rate `0`. The trainer, optimizer, demonstrations, adaptation workflow, model and decoder remain in place; Z1 is **not** an inference-only or no-computation arm.
- **B1 Repeat and Z Repeat:** separately submitted saved versions built from byte-identical local notebook source to B1 and Z1, respectively. They assess run-to-run stability of the **observed aggregate contrast**, not determinism of individual predictions.

A preceding **B0/V2** carrier is retained as a historical implementation/feasibility result. Its Python hash seed was not pinned, so it is **not** an exact B1 replicate or a matched experimental control.

The dated [29 October protocol](../docs/ARC2_UPDATE_STRENGTH_PROTOCOL_2026-10-29.md) and [30 October priority amendment](../docs/ARC2_PRIORITY_AMENDMENT_2026-10-30.md) preserve decisions made before the repeat scores were observed. A proposed half-rate arm was deliberately deferred in favor of source-identical B1 and Z repeat submissions; that decision is not a post hoc response to the scores.

## Observed official public-score display

The signed-in Kaggle [ARC-AGI-2 Submissions page](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/submissions) displayed the following **rounded public** scores and statuses. Version IDs identify the saved Kaggle submissions, not local Git blob hashes:

| Arm | Saved `scriptVersionId` | Learning policy | Public score | Kaggle status |
| --- | --- | --- | ---: | --- |
| [B0/V2](https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-candidate?scriptVersionId=363494251) | `363494251` | `5e-5`, hash seed unpinned | **31.81** | Succeeded |
| [B1 Hash42](https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-b1-hash42?scriptVersionId=363939870) | `363939870` | `5e-5`, hash42 | **30.97** | Succeeded |
| [Z1 Zero Update](https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-z1-zero-update?scriptVersionId=364031423) | `364031423` | `0`, hash42 | **9.58** | Succeeded |
| [B1 Repeat](https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-b1-repeat?scriptVersionId=364031921) | `364031921` | `5e-5`, hash42, exact local B1 source repeat | **30.56** | **Succeeded (after deadline)** |
| [Z Repeat](https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-z-repeat?scriptVersionId=364032699) | `364032699` | `0`, hash42, exact local Z1 source repeat | **9.58** | **Succeeded (after deadline)** |

The original B1–Z1 difference is **21.39 public-score points** (30.97 − 9.58). The repeat B1–Z difference is **20.98 points** (30.56 − 9.58). B1 Repeat differs from B1 by **−0.41** points; Z Repeat matches Z1 **at the two-decimal precision displayed by Kaggle**. Equal rounded aggregate scores do **not** imply the same predictions on individual tasks.

**The deadline distinction is material.** The two repeats were *accepted and scored* by Kaggle but explicitly marked **“Succeeded (after deadline)”**. Their values are retained as research observations, **not** represented as timely final competition submissions. The displayed final-selection message indicates automatic selection from eligible best-scoring entries; B0/V2 (31.81) and B1 Hash42 (30.97) were the candidates shown as evaluated for final score. Final **private** scores and exact scoring-completion timestamps are unknown. The time visible on a screenshot is a time of *observation*, not proof of when scoring finished.

## Independent engineering control (not a benchmark score)

A separate real-model, bounded **zero-learning-rate invariance check** completed **128 training steps**. The check examined **506 adapter tensors** (528,564,224 elements), all finite and unchanged relative to the recorded reference values on that workload. Trainer and optimizer machinery executed with learning rate zero. **The probe stopped before decoding**, did not score ARC predictions and is not a substitute for a complete competition rerun. Its evidence resides in `evidence/zero-update-check-20261030/`, including the invariant receipt and executed driver.

## What the repeated results do and do not establish

The update-permitting policy yielded substantially higher **observed rounded public scores** than the zero-learning-rate policy in the initial comparison and in the exact-source repeats. In that limited, descriptive sense, **the aggregate contrast recurred across two observations per configuration**.

This is **not** evidence of a statistically significant difference, a trustworthy variance estimate, identical hidden-test predictions, a unique causal mechanism, or general repeatability beyond the observed runs. Hash42 and source identity reduce specific configuration ambiguities but do not ensure identical GPU scheduling, total realized compute, hidden scoring trajectories or deterministic model execution. Changing the learning rate may change downstream trajectories, compute allocation and which candidates are evaluated within a fixed budget. Without hidden task-level observations, the aggregate difference cannot independently identify the causal path. The historical B0/V2 result remains separate because it lacks a pinned hash seed.

The separate earlier symbolic depth-1/depth-2 pilot, reported as **0/167** public test outputs, is a different study and did not produce these NVARC neural scores. Placeholder packaging outputs, interrupted runs and infrastructure errors are not assigned performance scores.

## Reproducibility, rights and archive scope

The source/evidence record preserves locally byte-identical repeat notebooks, five immutable Kaggle saved-version IDs, source SHA-256 records, dated protocols, score observations, bounded engineering receipts and explicit claim limits. The archive **does not** include model weights, packaged third-party distributions, hidden evaluation tasks or hidden per-task predictions. Rerunning requires obtaining authorized external assets and the compatible pinned GPU runtime; a repository CI pass does not demonstrate hidden evaluation reproducibility.

The original NVARC authors are credited throughout. The main upstream Version 10 Notebook publicly displays Apache-2.0; the dependency Version 2 and model Version 1 Apache-2.0 labels are documented from a **28 October 2026 authenticated Kaggle inspection**, and were not independently reverified in the present check. Licenses of third-party dependencies and model assets remain their own. See [third-party notices](THIRD_PARTY_NOTICES.md) and the [independent publication audit](INDEPENDENT_SOURCE_EVIDENCE_AUDIT_2026-11-03.md).

**Research record:** [public GitHub Release](https://github.com/tsitsinodzotsenidze-eng/arc-agi2-balanced-pipeline/releases/tag/arc2-2026-final-1); [published Zenodo record](https://zenodo.org/records/23895859), DOI **10.5281/zenodo.23895859**, version `2026-final-1`. The curated archive preserves the reviewed source snapshot at `84d84e2a5b8bad8459ed1a04511743df0bf257fe`; preparation-time status statements inside that immutable snapshot are superseded by the publication receipt in the current repository. The separate integrated ARC-AGI-2/ARC-AGI-3 academic manuscript is not this Kaggle Solution Writeup.

## Conclusion and next analysis

Repeated evaluations showed substantially higher public scores with parameter updates enabled than with a zero learning rate, while trainer and optimizer computations were retained. The observed contrasts were **21.39** and **20.98 public-score points**. The updating configuration scored **30.97** and **30.56**, whereas the zero-learning-rate configuration scored **9.58** in both evaluations at Kaggle's displayed precision. These observations support the directional hypothesis in the tested implementation and establish a recurring empirical contrast between the two update policies.

The study therefore provides evidence of performance sensitivity to the update policy beyond the mere presence of an executing training workflow. It does not isolate a unique mechanism: parameter changes can also alter subsequent generation, candidate ranking and budget use. Task-level and runtime traces, together with additional matched repetitions, would help distinguish these pathways and assess generalization. With two observations per configuration, the result remains a bounded empirical finding rather than a statistical-significance claim or a guarantee of repeatability in other settings.

The contribution is an attributed comparison of update policies with source-identical repeat carriers, bounded parameter-invariance evidence and traceable provenance. It supplies an empirical foundation for the wider research question of when an adaptation procedure improves problem solving under unfamiliar conditions.
