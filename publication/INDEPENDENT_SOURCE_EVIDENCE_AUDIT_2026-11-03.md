# Independent ARC-AGI-2 source, evidence and publication-readiness check
**Checked:** 3 November 2026 (Georgia time)  
**Prepared by:** Chat Amunia for Work/Astra review  
**Scope:** Read-only evidence inspection and editorial review. No reruns, code changes, GPU allocation, new submissions, Zenodo actions, or publication approval.

## A. Five saved competition carriers and observed public results

| Arm | Saved `scriptVersionId` | Learning policy / role | Rounded public score | Exact displayed Kaggle outcome |
| --- | --- | --- | ---: | --- |
| B0 / V2 | [363494251](https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-candidate?scriptVersionId=363494251) | LR=5e-5; *unpinned* Python hash seed; historical reference | **31.81** | Succeeded |
| B1 Hash42 | [363939870](https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-b1-hash42?scriptVersionId=363939870) | LR=5e-5; hash42; updating reference | **30.97** | Succeeded |
| Z1 Zero Update | [364031423](https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-z1-zero-update?scriptVersionId=364031423) | LR=0; hash42; trainer/optimizer computations retained | **9.58** | Succeeded |
| B1 Repeat | [364031921](https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-b1-repeat?scriptVersionId=364031921) | Exact local B1 notebook repeat | **30.56** | Succeeded (after deadline) |
| Z Repeat | [364032699](https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-z-repeat?scriptVersionId=364032699) | Exact local Z1 notebook repeat | **9.58** | Succeeded (after deadline) |

**Verification basis:** the signed-in Kaggle Submissions screen as shown in the 3 November screenshot and the repository's `publication/CURRENT_RESULTS.json`, `publication/RESULT_OBSERVATION_2026-11-03.json` and `publication/Z_REPEAT_RESULT_OBSERVATION_2026-11-03.json`. The visible 06:43 Georgian Windows clock is an **observation time**, **not** the Kaggle scoring-completion timestamp. The two after-deadline observations are legitimate descriptive research evidence but must not be represented as deadline-eligible final entrants.

**Independent repository-tree cross-check:** the two B1 notebooks (`NVARC_2026_B1_HASH42_SUBMISSION.ipynb` and `NVARC_2026_B1_REPEAT_SUBMISSION.ipynb`) have the same Git blob SHA `53f412c70a01b6af7745ed41d1a94135a6e3a7c9`. Both Z1 and Z Repeat notebooks have blob SHA `3e64b1a9866ee2ae332e9c0623be0241bd332709`. This supports **byte identity of these stored repository notebooks**, not necessarily exact identity to exported Kaggle binaries, run scheduling, model weights, GPU behavior, task-level predictions or hidden scoring cohorts.

Original updating-minus-zero-update contrast: **30.97 − 9.58 = 21.39** points. Repeat contrast: **30.56 − 9.58 = 20.98** points. B1 repeat shift: **−0.41** points. Z repeat agreement: **0.00** at *displayed two-decimal rounding*. These two observations per condition cannot establish statistical significance, reliable variability, deterministic predictions, a uniquely identified causal mechanism or a population effect. B0/V2 is deliberately not pooled as an exact B1 replicate.

Kaggle's page shows **0/2 manually selected** with automatic-selection wording; the user screenshot indicated B0/V2 and B1 Hash42 as evaluated for final score. Final private scores are not established.

## B. Upstream source/rights recheck

| Upstream asset | Checked now (3 Nov) | What remains a historical observation |
| --- | --- | --- |
| [Sorokin NVARC author notebook](https://www.kaggle.com/code/sorokin/arc2-qwen3-unsloth-flash-lora-batch4-queue), **Version 10** | Kaggle's publicly readable page explicitly labels **Version 10 of 10** and **Apache 2.0** | Signed-in 28 Oct inspection as independently recorded in `nvarc_port/NOTICE` |
| [Sorokin Unsloth dependency notebook](https://www.kaggle.com/code/sorokin/pip-install-unsloth-flash-patch), **Version 2** | Exact target URL found, but public view offered **no readable license field**. No independent present-tense license confirmation. | 28 Oct signed-in inspection reported **Apache 2.0** |
| [Sorokin Qwen3 model](https://www.kaggle.com/models/sorokin/qwen3_4b_grids15_sft139/transformers/bfloat16/1), **Version 1** | Exact model/version URL found, but public view offered **no readable license field**. No independent present-tense license confirmation. | 28 Oct signed-in inspection reported **Apache 2.0** |

[NVARC upstream README](https://github.com/1ytic/NVARC/blob/main/README.md) identifies **Ivan Sorokin and Jean-Francois Puget** as NVARC authors and acknowledges the ARChitects lineage. A root `LICENSE` was **not found** in the upstream GitHub repo when queried. This does **not** override any artifact-specific Kaggle license; conversely, the author-notebook's license does not license the entire GitHub repo, bundled model weights, runtime packages or all dependencies. The notebook Version10 source is retained in `nvarc_port/vendor/author-v10.ipynb`; the dependency Version2 in `nvarc_port/vendor/dependency-v2.ipynb`. Recorded SHA-256 hashes in `nvarc_port/SOURCE_HASHES.json` should be retained alongside the archived source.

**Rights checkpoint before public archive:** Work should independently inspect the signed-in Kaggle license fields for Version2 and model Version1 if rights must be asserted in public metadata, preserve attribution/NOTICE, and exclude external weights and built distributions unless separately authorized. `publication/THIRD_PARTY_NOTICES.md` already states this boundary accurately. No conclusion here certifies all rights or authorizes a blanket relicensing.

## C. Archive and editorial closeout for Work

- The repository was **private** at this review. Private GitHub links are not necessarily usable by public peer reviewers or Zenodo readers; public visibility is a separate, deliberate publication step.
- Existing Zenodo [draft 23895859](https://zenodo.org/uploads/23895859) has reserved DOI `10.5281/zenodo.23895859`; **reserved is not published**.
- The preserved 2 November ZIP is a **pre-result checkpoint**. The later v2 ZIP, according to `publication/RELEASE_STATUS.md`, predates Z Repeat. The final deposit ZIP and its manifest must be freshly reconciled with **both** after-deadline repeat outcomes and actual contents before pressing Publish.
- `publication/CURRENT_RESULTS.json`, `publication/CLAIMS_LEDGER.md`, `publication/RESULTS_AND_LIMITATIONS.md`, `publication/SOLUTION_WRITEUP_DRAFT.md`, `publication/REPRODUCING.md` and `publication/THIRD_PARTY_NOTICES.md` already capture the central story. Avoid replacing them with a parallel, inconsistent source of truth.
- Preserve the source checkpoints and dated protocols unchanged. Once ready: verify selected archive paths and per-file hashes, run existing CI and ZIP integrity checks, separately verify the public GitHub repository/Release, and verify the Zenodo *published* landing page and DOI. This editorial check did not itself perform those actions.
- Do **not** infer final private scores or model-effect significance from public aggregate results. Do **not** imply the earlier symbolic 0/167 pilot produced the NVARC neural scores.

**Review disposition:** Evidence/attribution summary is suitable for Work's release review **subject to** the two not-yet-independently-rechecked license fields, final ZIP reconciliation, public visibility, publication controls and final DOI verification. No new neural run is required for this documentary audit.
