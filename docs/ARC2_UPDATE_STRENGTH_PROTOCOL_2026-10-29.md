# ARC2 per-task update-strength study — protocol v0.1

Recorded 29 October 2026, before any official B0 score was observed by this
work session. Cici requested up to three additional official attempts, with
research value for the paper taking priority over leaderboard optimization.
Astra independently reviewed the exact vendored NVARC v10 source and this
hash-seed-controlled design. This file predeclares intended arms; it is not
evidence that candidate code or GPU validation has been completed.

## Question and attribution

Within the attributed NVARC baseline, how do per-task parameter updates and
their learning-rate amplitude relate to official performance when the nominal
training workload, checkpoint and inference policy are held constant?
This is a replication/implementation and sensitivity study of existing NVARC,
not a new solver. Keep it distinct from the ARC3 Recovery intervention.

## Current run and planned arms

| Arm | Target Georgia date | Learning rate | Python hash seed | Role |
| --- | --- | --- | --- | --- |
| B0 | 29 October, human submitted | 5e-5 | Not pinned by carrier | Historical port/feasibility baseline |
| B1 | 30 October | 5e-5 | 42 | Controlled full-rate reference |
| Z | 31 October | 0.0 | 42 | Null-update control, training computations retained |
| H | 1 November | 2.5e-5 | 42 | Half scheduled learning-rate amplitude |

B0 is `ARC2 2026 NVARC Candidate`, Version 2,
scriptVersionId 363494251. The competition Submissions page was observed on
29 October at about 17:00–17:05 Georgia time showing `Notebook Running`,
about ten minutes after submission. No score was displayed. This observation
confirms submission existence/status only, not completed hidden inference.
The user performed final Submit. This session did not submit or interrupt it.

The three planned arms are chosen now, not selected from future leaderboard
scores. The first observed B0 completion is a feasibility gate; if it exposes a
technical defect, preserve this protocol and append a dated amendment rather
than silently changing it. A failed B0 may require using a slot for repair;
three additional scientific runs are a target, not a guaranteed completion.

## Exact controlled settings

The source has one training epoch, batch size 1, gradient accumulation 1,
LoRA rank 256 / alpha 32, weight decay 0, cosine scheduler, warmup ratio 0.1,
trainer and adapter initialization seeds 42. Training augmentation is n=16,
seed=1; decoding augmentation uses n=2, seed=2. Every task restores the same
initial adapter weights before adaptation. Retain these settings, checkpoint,
tokenizer, BF16 precision, dependency versions, L4 x4, original image 31090,
Internet OFF, challenge source, task coverage rules, decoder/search limits,
selection/ranking policy and first-cell 12-hour-minus-600-second deadline.

Only the declared learning-rate literal differs among B1/Z/H. Use exactly one
source-guarded replacement; archive upstream, wrapper, generated source and
notebook hashes and record the actual run/version/settings for each arm.
Do not replace a running or submitted saved version. Prepare separate named
carriers while preserving all three verified input attachments.

A material randomization source is rescoring augmentation:
`seed=hash(bk) % 1024**2`. The original baseline does not pin PYTHONHASHSEED.
For B1/Z/H, set `PYTHONHASHSEED=42` in the child environment BEFORE launching
the Python driver, inherited by all workers. Assigning it inside an already
running interpreter does not reseed that interpreter. B1 versus B0 is not an
exact replication or an isolated estimate of hashing: both hashing and run
variability can contribute. GPU nondeterminism/dynamic task scheduling remain.

Z must still initialize the trainer and execute the same training examples,
steps and optimizer machinery. It is not a compute-free adaptation-off arm.
Before official use, a bounded engineering check must verify that restored
adapter parameters remain unchanged after zero-rate training. H halves the
learning-rate schedule amplitude; it does not halve epochs or training time.
Actual wall time, generated candidates and decoding time can differ by arm.
This design holds nominal training work constant, not total realized compute.

## Outcomes and claim boundaries

Primary available outcome: official public leaderboard score for each
successful saved-version submission, with exact score provenance. Record
terminal success/failure separately; a failed or unfinished run is not score0.
Record observed submission/scoring timestamps and any available runtime or
coverage receipts. Kaggle's displayed submission durations are obfuscated;
queueing/scoring time is not model-compute time. Never infer missing hidden
per-task predictions or diagnostics if the platform does not expose them.

Descriptive contrasts: B1 minus Z (updates versus null updates), H minus B1
(lower versus full amplitude), H minus Z. With one official run per controlled
arm, do not claim statistical significance, a reliable dose-response curve,
paired per-task effects, or broad generalization. Directional/negative results
are retained with equal care. Aggregate hidden scores alone cannot explain a
mechanism. Both attempt slots and generated-candidate/fallback counts remain
separate wherever diagnostics are available.

The checkpoint training contains public-evaluation-derived material. Reusing
those public evaluation tasks cannot establish fresh neural generalization.
The earlier symbolic v1 0/167 pilot remains frozen and separate. Synthetic
smoke success is runtime evidence, not an official score or benchmark result.

## Calendar and handoff

Official limits checked in this conversation: one submission per day; up to
two final submissions. Final deadline: 2 November 2026 23:59 UTC, equivalent
to 3 November 03:59 Georgia time. Scoring must finish by that instant.
Target three daytime submissions on 30 October, 31 October and 1 November.
Reserve 2 November for closure or necessary recovery, rather than adding a
new exploratory arm. Final submission selection and all final Submit clicks
remain human actions. No automated future monitoring is established here.

For the paper, retain each hypothesis, immutable source/configuration,
predeclared difference, engineering checks and actual observed outcome.
ARC2 and ARC3 can share a discussion of adaptation under resource limits;
their scores, interventions and evidence remain distinct experiments.
