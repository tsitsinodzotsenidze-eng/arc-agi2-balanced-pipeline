# Zenodo metadata draft

Title: ARC-AGI-2: NVARC update-sensitivity study — competition carriers, provenance and replication record (2026)

Creator: Dzotsenidze, Tsitsino

Resource type: Software

Version: to be assigned to the next post-Z-result export; previous draft 2026-checkpoint-2

## Description

ARC Prize2026 — ARC-AGI-2: an attributed NVARC port and update-sensitivity
study. Creator of the port, study and archive: Tsitsino Dzotsenidze. Upstream
NVARC authors: Ivan Sorokin and Jean-Francois Puget (NVIDIA KGMoN), with
underlying ARChitects lineage. This is a replication/implementation study,
not a claim of a new solver.

The study compares a full-rate reference (LR5e-5, hash42) with a null-update
condition (LR0, hash42), followed by exact source repeats. Null-update training
retains trainer and optimizer computations. A separate synthetic engineering
check completed128 steps while all506 inspected adapter tensors remained
finite and unchanged; it stopped before decoding and is not accuracy evidence.

Observed rounded official public scores: B0/V2 31.81 (script363494251),
B1 30.97 (363939870), Z1 9.58 (364031423). On 3 November B1 Repeat
(script364031921) displayed 30.56, exact status Succeeded (after deadline).
Z Repeat (364032699) also succeeded after deadline with displayed public9.58,
matching Z1 at two-decimal precision. The updating-minus-zero-update gaps
are21.39 initially and20.98 in the repeat pair. Both after-deadline results
are research evidence, not claimed timely final candidates. B0 has an
unpinned hash seed and is retained as a historical reference. The B1-Z1
contrast recurs descriptively across two observations per configuration;
a unique causal mechanism, statistical significance, general repeatability
and final private leaderboard results are not established.

The source/evidence archive preserves self-contained carrier notebooks,
exact vendored source notebooks, dated design amendments, attribution,
selected engineering receipts and machine-readable current results. Model
weights, built dependency distributions and hidden evaluation tasks or
predictions are excluded. Re-execution requires separately obtained authorized
inputs and the pinned compatible GPU runtime. Apache-2.0 applies to the
included NVARC material as described in the retained notices; external assets
keep their own terms. This technical archive is separate from the joint
ARC-AGI-2/ARC-AGI-3 manuscript.

Repository: https://github.com/tsitsinodzotsenidze-eng/arc-agi2-balanced-pipeline

Publication status: preparation draft. A reserved DOI does not establish
publication. The exact source commit and archive checksum will be recorded
before publication. Repeat outcomes will be appended only after verification.
