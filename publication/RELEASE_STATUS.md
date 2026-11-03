# ARC-AGI-2 publication status and exact next action
**Updated:** 3 November 2026, Georgia time. **Status:** Documentation for Work review; **publication NOT yet claimed**.

## Preserved immutable research state

- Historical reviewed research PR **#8** merged at `6cb9f96dc4d3e4c2219fd5941849131c44be4760`. CI on the reviewed head passed (workflow `41513603656`).
- Five submitted Kaggle saved versions and their source carriers are unchanged. The [results registry](CURRENT_RESULTS.json) and [independent audit](INDEPENDENT_SOURCE_EVIDENCE_AUDIT_2026-11-03.md) record exact saved version IDs, scores, source identities and status.
- **B1 Repeat 30.56** and **Z Repeat 9.58** both have exact Kaggle status **Succeeded (after deadline)**; both belong in the research archive but are not asserted as timely final entrants. B1/Z1 original contrast **21.39**, repeat contrast **20.98** public-score points. B0/V2 31.81 remains historical, with unpinned hash.
- **Final private leaderboard scores and precise scoring-completion timestamps are unknown.** Screenshot timestamps are observation timestamps.
- Original 2 November source/evidence ZIP, **57 files, 391,413 bytes**, SHA-256 `00936ad565ba6e0a64f1086834488fa112ad53dd28a09ac64346d401c57211b2` — retained unchanged.
- Subsequent v2 ZIP, **393,868 bytes**, SHA-256 `91f4fea6e0f016def4bb6d668f0c43d384b5585cfeffd0e896cf0d31edbcf549` — retained unchanged; this ZIP **predated Z Repeat's observed final result**.
- Work's [static preflight](WORK_ARCHIVE_PREFLIGHT_2026-11-03.json) verified both older ZIPs and matched carrier source hashes. **It did not certify the future final export.**
- Original protocols, source code, carrier notebooks, SHA-256 hashes and dated observation receipts have not been changed by this documentation-only work.

## Existing publication destinations

- GitHub repository: https://github.com/tsitsinodzotsenidze-eng/arc-agi2-balanced-pipeline — **Private** as last independently checked, not an accessible public paper citation yet.
- Zenodo existing draft: https://zenodo.org/uploads/23895859 ; reserved version DOI `10.5281/zenodo.23895859`. **Reserved is not published.** No final archive upload or DOI registration is claimed here.
- ARC-AGI-2 Kaggle Solution Writeup: [revised complete draft](SOLUTION_WRITEUP_DRAFT.md); **publication not claimed**.
- Kaggle Paper Track and *Two Worlds* academic manuscript are separate future deliverables.

## Documentation checkpoint / Work handoff

The author requested all editorial changes on **`publication/arc2-documentation-final-20261103`**, based on `main` commit `1867ac19add31f0b5d87406e644cd6f47a1d71c8` and including a previously drafted independent evidence audit. The PR's final head SHA is the **authoritative documentation snapshot** for Work's next source archive. Recheck the PR head immediately before packaging and use **that exact immutable commit**, not the moving branch label.

**Next for Work (not performed by Chat Amunia):**

1. Review PR diff, full English writeup, rights statements, [claim ledger](CLAIMS_LEDGER.md) and source/score consistency; optionally obtain Astra's independent methodology critique.
2. Check CI, approve/merge the reviewed document commit when authorized; leave submitted model code and history unchanged.
3. Prepare a new final source/evidence ZIP (with **both** after-deadline observations) from the exact reviewed Git commit. Record `SOURCE_SNAPSHOT.json`, complete `SHA256SUMS.json`, file count, bytes and ZIP SHA-256. Preserve older exports.
4. Complete rights review, GitHub public repository/Release verification, then update the **existing Zenodo draft**, upload the matched final ZIP, inspect metadata and author publication decision, and verify the **published** DOI landing page.
5. Prepare and submit the **separate** ARC-AGI-2 Kaggle Solution Writeup and Paper Track entry only through their authorized workflows; never confuse a saved draft with Submit.

**Safety boundary:** This is editorial documentation work only. No GPU experiment, model run, source-carrier change, scoring resubmission, artifact rehash/rebuild, Zenodo mutation, release creation or Kaggle Writeup submission is claimed.
