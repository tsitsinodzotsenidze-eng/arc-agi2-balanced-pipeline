# ARC-AGI-2: Attributed NVARC parameter-update sensitivity and repeatability (2026)

**Research/port author:** Tsitsino Dzotsenidze — [ORCID 0000-0002-9432-1803](https://orcid.org/0000-0002-9432-1803)  
**Original NVARC solver authors:** Ivan Sorokin and Jean-Francois Puget (NVIDIA KGMoN; underlying ARChitects lineage)  
**Status:** Reviewed source/evidence record **published** on 3 November 2026 (UTC). This repository is **Public**; [GitHub Release](https://github.com/tsitsinodzotsenidze-eng/arc-agi2-balanced-pipeline/releases/tag/arc2-2026-final-1) and [Zenodo DOI 10.5281/zenodo.23895859](https://zenodo.org/records/23895859) are live. This is an attributed port and comparative study, not an independently invented solver. Kaggle Solution Writeup publication is a separate step.

## Research question

In an attributed NVARC ARC-AGI-2 carrier, does the observed public-score contrast between test-time parameter updates (`LR=5e-5`) and a zero-learning-rate condition (`LR=0`) recur when source-identical saved carriers are evaluated again?

Z1 retains **trainer and optimizer computations**, model, demonstrations and decoder policy: LR0 does **not** mean computation-free inference. B1/Z1 and both repeats use a child-driver `PYTHONHASHSEED=42`. Original model, nominal training settings and decoder policy are retained. A separate historical baseline B0/V2 had an **unpinned** Python hash seed and is **not** a matched B1 repeat.

The original [29 October protocol](docs/ARC2_UPDATE_STRENGTH_PROTOCOL_2026-10-29.md) and [30 October amendment](docs/ARC2_PRIORITY_AMENDMENT_2026-10-30.md) show the test plan and prioritization of exact-source repeat observations before results were available.

## Observed rounded public Kaggle results (3 November 2026)

| Arm | Saved Kaggle `scriptVersionId` | Learning policy / provenance | Public score | Kaggle status |
| --- | --- | --- | ---: | --- |
| [B0/V2](https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-candidate?scriptVersionId=363494251) | `363494251` | LR=5e-5; **hash not pinned**; historical | **31.81** | Succeeded |
| [B1 Hash42](https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-b1-hash42?scriptVersionId=363939870) | `363939870` | LR=5e-5; hash42; updating reference | **30.97** | Succeeded |
| [Z1 Zero Update](https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-z1-zero-update?scriptVersionId=364031423) | `364031423` | LR=0; hash42; trainer/optimizer retained | **9.58** | Succeeded |
| [B1 Repeat](https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-b1-repeat?scriptVersionId=364031921) | `364031921` | Exact local B1-source repeat | **30.56** | **Succeeded (after deadline)** |
| [Z Repeat](https://www.kaggle.com/code/tsitsinodzotsenidze/arc2-2026-nvarc-z-repeat?scriptVersionId=364032699) | `364032699` | Exact local Z1-source repeat | **9.58** | **Succeeded (after deadline)** |

The updating–zero-update difference was **21.39** points initially and **20.98** in the repeat pair. The B1 repeat changed by **−0.41**, and Z Repeat matched Z1 to the **two-decimal public display precision**. Identical rounded totals are not proof of identical predictions; two observations per configuration do not establish statistical significance, reliable variability, general repeatability or a uniquely identified causal mechanism.

The two repeat evaluations were **successfully scored after the deadline** and are retained as **research observations**, **not** as timely final competition entrants. Kaggle displayed automatic-selection wording: B0/V2 (31.81) and B1 Hash42 (30.97) were shown as evaluated for final score. **Final private scores are not known.** A screenshot timestamp is an **observation time**, not an exact scoring completion time.

## Independent engineering control (not a score)

A bounded zero-learning-rate training probe completed **128 steps** and verified **506 adapter tensors** stayed finite and unchanged in the checked segment. The probe stopped **before decoding**; it is implementation evidence, not prediction accuracy or full hidden-test reproducibility.

## Evidence, reproduction and publication

- [Technical ARC-AGI-2 Solution Writeup — reviewed text](publication/SOLUTION_WRITEUP_DRAFT.md)
- [Machine-readable five-run results](publication/CURRENT_RESULTS.json)
- [Results and interpretation limitations](publication/RESULTS_AND_LIMITATIONS.md)
- [Claim-to-evidence ledger](publication/CLAIMS_LEDGER.md)
- [Independent 3 November evidence/license audit](publication/INDEPENDENT_SOURCE_EVIDENCE_AUDIT_2026-11-03.md)
- [Reproduction constraints and external dependencies](publication/REPRODUCING.md)
- [Upstream attribution and licenses](publication/THIRD_PARTY_NOTICES.md)
- [Zenodo metadata for final reviewed export](publication/ZENODO_DESCRIPTION.md)
- [Publication and archive readiness](publication/RELEASE_STATUS.md)
- [Work static ZIP and source preflight](publication/WORK_ARCHIVE_PREFLIGHT_2026-11-03.json)

The repository stores retained **exact local source** notebooks, hashes, dated protocols and selected receipts. B1 and B1 Repeat local carrier notebooks are byte-identical; the same is true for Z1 and Z Repeat. This does **not** establish identity of Kaggle metadata/runtime execution or hidden task predictions.

Models and weights, built external dependency distributions and hidden evaluation tasks/predictions are **not redistributed** in the published research deposit. Reproduction requires separately authorized inputs and a compatible pinned GPU environment. The original NVARC Version 10 Kaggle Notebook openly lists Apache-2.0; Apache-2.0 for the specific dependency V2 and model V1 references is supported by a **dated 28 October signed-in inspection** and is **not** claimed newly reconfirmed for both. See the notices for the full scope. Earlier symbolic depth1/depth2 0/167 pilot is separate and is not responsible for these NVARC neural scores.

**Published archive:** [Zenodo record](https://zenodo.org/records/23895859), version DOI **10.5281/zenodo.23895859**, version `2026-final-1`; [GitHub Release](https://github.com/tsitsinodzotsenidze-eng/arc-agi2-balanced-pipeline/releases/tag/arc2-2026-final-1). The curated 65-file ZIP is pinned to source commit `84d84e2a5b8bad8459ed1a04511743df0bf257fe`. Its SHA-256 is `96dfc157e13b52091af098a1be2d2e7ebee6b5e1733e55d333b00ffa7aa7456c`. GitHub automatic source archives contain the wider repository and are distinct from this curated deposit. Older checkpoints remain unchanged. See the [publication verification receipt](publication/PUBLICATION_RECEIPT_2026-11-03.json).

The combined ARC-AGI-2 / ARC-AGI-3 academic manuscript, *Two Worlds, One Challenge: How AI Solves Unfamiliar Problems*, and a Kaggle Paper Track submission are **separate** deliverables from this technical record.
