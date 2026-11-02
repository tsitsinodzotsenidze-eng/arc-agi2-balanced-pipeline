# ARC-AGI-2: An Attributed Replication Study of Parameter Updates in NVARC

Interim technical draft, 2 November2026. Repeat results remain pending
verification. This file is not an officially submitted competition writeup.

## Research question

We examine the relationship between test-time parameter updates and observed
ARC-AGI-2 public leaderboard performance in an attributed port of the NVARC
solution developed by Ivan Sorokin and Jean-Francois Puget. The question is
whether a contrast between an updating configuration and a null-update
configuration recurs across exact-source repeat submissions.

## Method

B1 uses LR5e-5 with `PYTHONHASHSEED=42`. Z1 uses LR0 and hash42 while retaining
trainer and optimizer computations. The model, nominal training workflow and
decoder policy are preserved. B1 repeat is byte-identical in local source to
B1; Z repeat is byte-identical to Z1. Source identity does not guarantee
identical GPU execution or realized compute.

A separate synthetic engineering probe completed128 steps and found all506
inspected adapter tensors finite and exactly unchanged. It ended before
decoding and does not establish benchmark accuracy.

## Observed results

- B0/V2:31.81, script363494251; historical reference with unpinned hash seed.
- B1:30.97, script363939870.
- Z1:9.58, script364031423.
- B1 repeat:script364031921, pending verification.
- Z repeat:script364032699, pending verification.

These are rounded public scores. Final private scores are unknown. Short
ordinary notebook packaging runs are not official scoring runs.

## Interpretation

The B1-Z1 difference of21.39 points motivates replication but does not by
itself identify a causal mechanism or statistical significance. Repeat
outcomes assess the stability of the observed contrast under the recorded
configurations. Both repeat results, including non-completion, will remain
visible. B0 is reported separately because its hash conditions differ.
Aggregate scores do not reveal hidden task-level effects or execution
coverage. The earlier symbolic pilot and ARC-AGI-3 recovery experiments
remain separate evidence streams in the joint manuscript.
