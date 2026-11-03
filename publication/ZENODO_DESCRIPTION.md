# Zenodo metadata — final reviewed ARC-AGI-2 export (pre-publication draft)
**Prepared:** 3 November 2026  
**Record status:** Existing **draft** `https://zenodo.org/uploads/23895859`. Reserved DOI `10.5281/zenodo.23895859` **is not yet registered as a published version DOI**. This file does not authorize publishing the deposit or claim it exists publicly.

**Title:** ARC-AGI-2: NVARC parameter-update sensitivity and repeatability — competition carriers, provenance and results (2026)

**Creator:** Dzotsenidze, Tsitsino  
**Resource type:** Software (research source and evidence archive)  
**Publication date:** Set to actual publication date after verification  
**Version:** Assign from the final reviewed export (do not reuse the unmodified 2 November or pre-Z-result v2 ZIP labels)  
**Publisher:** Zenodo

## Description — ready to adapt to the actual final manifest

This archived technical record documents an **attributed ARC Prize 2026 ARC-AGI-2 implementation, update-sensitivity and repeatability study** by Tsitsino Dzotsenidze. The underlying NVARC solver was developed by **Ivan Sorokin and Jean-Francois Puget** (NVIDIA KGMoN), with earlier ARChitects lineage. The contribution here is the documented 2026 port, a controlled comparison of test-time parameter-update policies, exact-local-source repeat submissions, bounded parameter-invariance engineering evidence, and traceable saved-version and research provenance; the NVARC solution itself is **not** claimed as a new invention.

The initial reference uses learning rate `5e-5` and `PYTHONHASHSEED=42` (B1); the null-update condition uses learning rate `0` with the same hash-seed setting while retaining trainer and optimizer computations, model and decoder policy (Z1). B1 Repeat and Z Repeat use locally byte-identical notebooks to B1 and Z1, respectively. Historical B0/V2 lacks a pinned Python hash seed and is reported separately.

**Observed rounded public Kaggle scores:** B0/V2 **31.81** (saved script `363494251`); B1 **30.97** (`363939870`); Z1 **9.58** (`364031423`); B1 Repeat **30.56** (`364031921`), **Succeeded (after deadline)**; Z Repeat **9.58** (`364032699`), **Succeeded (after deadline)**. The B1–Z1 public-score difference is **21.39** points initially and **20.98** in the repeat pair. Both repeat results are **post-deadline research observations**, not timely final competition entrants. Z1 and Z Repeat have equal **displayed two-decimal aggregate** scores, which does not establish identical predictions. The differences are descriptive, not proof of statistical significance, broad repeatability or a uniquely identified causal mechanism. Final private leaderboard results and exact scoring-completion timestamps are **unknown**.

A separate bounded real-model engineering check completed **128 zero-learning-rate training steps**, with **506 inspected adapter tensors** finite and unchanged, but ended before decoding. It is **not** a benchmark-accuracy result.

The selected deposit is to contain source carrier notebooks, retained versions of upstream notebooks with required notices, selected dated protocols, hash manifests, static verification receipts, and machine-readable public result observations. It **excludes** model weights, installed third-party distributions, hidden evaluation tasks and hidden per-task predictions. Full rerunning requires separately authorized external inputs and a compatible pinned Kaggle GPU runtime; successful static/CI checks do not demonstrate hidden benchmark reproduction.

**License and rights:** the primary original Kaggle NVARC Notebook Version 10 publicly displays Apache-2.0; a signed-in artifact-specific inspection dated **28 October 2026** recorded Apache-2.0 for the specific Unsloth dependency Notebook Version 2 and Qwen model Version 1, whose current license fields were **not independently reread** in the latest check. Attribution and third-party terms remain applicable. The repository license is not a blanket relicense for any model, dependencies, or external materials. Consult `publication/THIRD_PARTY_NOTICES.md`, `nvarc_port/NOTICE` and the archive's source-hash manifest.

**Repository:** https://github.com/tsitsinodzotsenidze-eng/arc-agi2-balanced-pipeline

**Research relationship:** This ARC-AGI-2 technical archive is separate from the ARC-AGI-3 recovery-study deposit and the combined academic manuscript *Two Worlds, One Challenge: How AI Solves Unfamiliar Problems*.

## Final publication controls for Work

1. Use **the existing Zenodo draft**, do not create a duplicate DOI.
2. Review and select the actual final ZIP built from the **approved documentation commit**. Check full manifest coverage and per-file hashes against that commit; preserve previous ZIPs unchanged.
3. Verify README, source rights and selected archive scope. If the two remaining license fields cannot be reverified, keep the exact dated qualification rather than asserting contemporary independent verification.
4. Link a **real GitHub public Release** when one exists, not the unpublished private repository as a purported public source archive.
5. Save draft, inspect Preview, confirm public visibility and rights, obtain author approval, then publish and verify the landing page and version/concept DOIs. Until then, this is a **metadata draft**, not a citable publication.
