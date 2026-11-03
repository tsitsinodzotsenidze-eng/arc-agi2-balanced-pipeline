# ARC-AGI-2: Results, study design and interpretation limits
**Updated:** 3 November 2026. **Score source:** authenticated [Kaggle ARC-AGI-2 Submissions page](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/submissions), with dated observations recorded in the repository.

## Descriptive public results

| Condition | First score | Exact-local-source repeat | Repeat status |
| --- | ---: | ---: | --- |
| B1 (LR=5e-5; hash42) | **30.97** (`363939870`) | **30.56** (`364031921`) | **Succeeded (after deadline)** |
| Z1 (LR=0; hash42; trainer/optimizer retained) | **9.58** (`364031423`) | **9.58** (`364032699`) | **Succeeded (after deadline)** |

Historical B0/V2 (`363494251`): public **31.81**, Python hash seed not pinned; **not** an exact B1 replicate or matched control.

- Initial B1–Z1 public-score contrast: **21.39** points.
- B1 Repeat–Z Repeat public-score contrast: **20.98** points.
- B1 Repeat minus B1: **−0.41** points.
- Z Repeat minus Z1: **0.00** **at the displayed two-decimal precision only**.

All are **rounded public** scores, not final private leaderboard scores. The two repeat evaluations were completed and visibly scored but **after the competition deadline**. They are reported as research observations, **not** as deadline-eligible final-score submissions. The Submissions page's automatic-selection wording and screenshot row markings identified B0/V2 (31.81) and B1 Hash42 (30.97) as the entries evaluated for final score; the final private result remains unknown. The precise scoring-completion timestamps are not available. Screenshot-local clock time records first *observation*, not scoring-completion time.

## Experimental question and predeclared chronology

The study tests whether an apparent public-score contrast between the original NVARC update-permitting carrier and a zero-learning-rate carrier recurs when the same stored sources are rerun. The [29 October protocol](../docs/ARC2_UPDATE_STRENGTH_PROTOCOL_2026-10-29.md) defined the nominal training/control settings and disclosed the hash-seed limitation. The [30 October amendment](../docs/ARC2_PRIORITY_AMENDMENT_2026-10-30.md) prioritized exact B1 and Z repeats instead of a third, underpowered half-rate arm. Preserve these historical plans **without retrospective editing**.

The original NVARC solver authors are Ivan Sorokin and Jean-Francois Puget. This project is an **attributed port and comparative study**, not a novel solver. The initial B0 is historical because its Python hash seed was unpinned. For B1 and Z1, `PYTHONHASHSEED=42` is assigned before launching the child driver. Z1 retains trainer and optimizer computations and changes the intended parameter-update learning rate to zero. It is not a zero-workflow / inference-only ablation.

## What exact-source repeats establish

B1/B1-repeat carrier notebooks are byte-identical in the checked local repository; Z1/Z-repeat are likewise byte-identical. This restricts **source** variability. It does not establish byte identity to Kaggle's generated notebook exports, identical predictions, deterministic GPU kernels, identical total realized compute, queue time, hidden evaluation inputs, runtime scheduling or per-task success.

The **aggregate difference recurred descriptively** in two observations per policy. The equality of the two Z public scores is only an equality of displayed rounded aggregates. The sample is too small for a reliable variance estimate, a significance claim, a general repeatability estimate or identification of the causal mechanism of the contrast. A change in learning-rate policy can influence subsequent search and task-budget use, so the complete constrained pipeline—not isolated parameter-update efficacy—is the observed system.

The original predictions, hidden per-task correctness and fine-grained private computation traces are unavailable; do not infer them from aggregate Kaggle scores.

## Separate engineering and older studies

The real-model zero-learning-rate engineering check completed **128 steps** with all **506 inspected adapter tensors** finite and unchanged in that observed segment; it ended **before decoding**. It is parameter-invariance/implementation evidence, **not** benchmark accuracy, prediction equivalence or hidden-task recovery evidence. Its receipts are retained in `evidence/zero-update-check-20261030/`.

The earlier symbolic depth1/depth2 pilot (0/167 outputs in a public retrospective evaluation) and the separate ARC-AGI-3 recovery study are distinct research tracks. Notebook packaging placeholders, abandoned executions and infrastructure failures are not scored as zeros.

## Evidence and continuation

Primary machine-readable record: [CURRENT_RESULTS.json](CURRENT_RESULTS.json); claim-specific sources: [CLAIMS_LEDGER.md](CLAIMS_LEDGER.md), [B1 observation](RESULT_OBSERVATION_2026-11-03.json), [Z observation](Z_REPEAT_RESULT_OBSERVATION_2026-11-03.json); source/rights independent check: [3 November audit](INDEPENDENT_SOURCE_EVIDENCE_AUDIT_2026-11-03.md). The earlier 2 November and 3 November v2 ZIP archives are preserved unchanged. A new final ZIP must be built from the **reviewed final documentation commit**, with both repeats and complete file-hash coverage.

A future research extension could include multiple preregistered repeats, per-task and runtime accounting from authorized sources, and sensitivity analyses separating parameter updates from downstream trajectory/resource effects. **No new neural experiment was performed for this documentation update.**
