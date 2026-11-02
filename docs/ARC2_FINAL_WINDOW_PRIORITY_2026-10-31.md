# ARC2 final-window priority — 31 October 2026, Georgia time

Cici asked which candidate should have the next official opportunity if runs 3
and 4 each take about 24 hours and a fifth completion becomes difficult. She
also reserved the evening of 2 November for GitHub, Zenodo and writeups.
Research information is the primary objective; score is secondary.

Work and an independent Astra review recommend preserving the 30 October
order: **Z1, exact B1 repeat, exact Z repeat**. This reconsideration occurred
after B1's public score was known and without accessing Z1's official result.
It is a score-independent confirmation of the existing sequence, not a
score-selected reorder. No candidate code, saved Kaggle version, or official
submission was changed by this planning review.

| Run | Scientific condition | Priority and information |
| --- | --- | --- |
| 1, B0 | LR 5e-5, hash unpinned; public 31.81 | Historical port result; keep separate from the controlled comparison |
| 2, B1 | LR 5e-5, hash42; public 30.97 | Trained reference before Z1 |
| 3, Z1 | LR 0, hash42; trainer computations retained | First null-update observation |
| 4, exact B1 repeat | Identical to B1 | Preferred next run: trained reference after Z1 and an unchanged-code repeat |
| 5, exact Z repeat | Identical to Z1 | Next opportunity: test repeatability of the null-update observation |

## Why B1 repeat is next

The controlled sequence becomes B1 -> Z1 -> B1 repeat: updates enabled,
disabled, enabled. A later trained reference helps assess whether the Z1
contrast coincides with a broader change in execution conditions. Repeating Z
first would establish repeatability for the new condition but would leave
the trained reference entirely before the two Z observations. This temporal
bracketing is the reason for retaining B1 first under the documented platform
concerns; neither allocation is universally most informative without assumptions.

If the two B1 scores are close, the original reference has been reproduced on
one later run. If they differ materially, unchanged-code sensitivity becomes
part of the findings. Either observation informs interpretation of Z1. A stable
B1 does not prove that an unusual Z1 outcome was caused by parameter updates:
an isolated Z outcome, abrupt platform variation, and condition-specific
execution differences remain possible. Two B1 runs and one Z are descriptive
evidence, not a reliable variance estimate or a significance/mechanism test.
B0 is not an exact B1 replicate because its hash setting differs. Hash42 does
not control every source of randomness. A failed/invalid execution is recorded
separately from a valid zero score.

The half-rate arm remains deferred: it would introduce a third unreplicated
condition while the central full-rate/null-update comparison is still sparse.
Repeating B1 is not an algorithmic improvement or a promise of a higher score.

## Publication window

Prepare the code inventory, provenance, result tables, GitHub documentation,
Zenodo deposit material and the three writeup drafts during the current wait.
Reserve 2 November evening for checking links, final results and associations,
and publication preparation. Kaggle execution can continue server-side while
these materials are prepared. Keep result fields explicit as pending until
verified; incorporate completed results without rewriting their provenance.

The four-run evidence package should be usable even if run 5 cannot complete.
Run 5 remains the exact Z repeat when the actual remaining time and platform
limits allow. The 24-hour durations are planning scenarios, not promised
turnaround times. Final official Submit remains Cici's action.

The saved private carriers, exact version labels and descriptions remain in
[the prepared-candidate handoff](ARC2_PREPARED_CANDIDATES_2026-10-31.md).
