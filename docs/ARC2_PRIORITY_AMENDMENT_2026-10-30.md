# ARC2 priority amendment — decision 30 October 2026

Cici authorized three additional official runs after current B1, for five total
including completed B0. Work and Astra agreed this sequence before any B1 score
was observed. This durable record was restored on 31 October Georgia time after
the interrupted work session; B1 was still Notebook Running, approximately6h,
with no score. The original29 October protocol is preserved unchanged.

| Priority/order | Run | Configuration | Research value |
| --- | --- | --- | --- |
| 1, completed | B0 | LR5e-5, Python hash unpinned | Historical port/feasibility baseline; official31.81 |
| 2, current | B1 | LR5e-5, Python hash42 | Controlled full-rate reference |
| 3, next | Z1 | LR0.0, Python hash42; training computations retained | Full-rate versus null-update contrast |
| 4 | B1 repeat | Exact same scientific implementation as B1 | Observe variability with unchanged reference code |
| 5 | Z repeat | Exact same scientific implementation as Z1 | Observe whether the contrast persists; two runs per condition if all finish |

The reason is research value under scarce calendar/platform capacity, not
selection by leaderboard scores. The previously planned half-rate H arm is
deferred: it would add another unreplicated condition while primary contrast
variability remains unknown. No future score changes this declared sequence.
Retain negative/equal results and failures; a failure is not a zero score.

If only Z1 finishes, B1/Z1 give a single descriptive contrast. The B1 repeat
adds a reference variability observation. The Z repeat gives two observations
per condition. Even two per condition do not support reliable statistical
significance or proof of mechanism. Equal aggregate scores can hide different
solved outputs; hidden per-task effects must not be inferred.

Z removes per-task parameter updates, not all learning/reasoning. It still
sees the same demonstration pairs, uses the same prompts/augmentation and
executes trainer/optimizer computations. Hold model, nominal training work,
hash seed, decoder, environment and global deadline fixed. Realized search
paths and compute/time allocation can still differ; the contrast concerns the
complete constrained pipeline, not an isolated measure of learning capacity.

## Engineering gate — now passed

The separate bounded real-model check completed successfully on30 October:
Kaggle Version1 / scriptVersionId363962649, displayed317.1s. It executed all128
trainer steps;506 optimizer-state entries also recorded128 steps. Both
optimizer groups had LR0; weight decay0; training loss0.7502095103263855.
All506 adapter tensors /528564224 elements were finite and exactly equal to
cloned initial adapter values immediately after reset and after training.
No decoding/inference or official submission was performed by this check.

See `evidence/zero-update-check-20261030/`: rendered saved code/receipt,
training invariant, and exact executed Z driver. The saved cells are a DOM
transcription of the identified immutable Kaggle version, not a raw notebook
download. Their full source is preserved and matched the previously reviewed
generated artifact. The rebuilt probe notebook SHA256 remains
`b2c90c21f8bdb979ed1a0668e3d1dd49404bd20d4e470db04643c2e0c3760aa1`.
The official Z notebook remains
`7b9a5c374d04cdbc959b925c4f4e21e3ba7fd6e9459e3958d8f6fd753ca0aec9`.
Astra reviewed the implementation and the actual PASS receipt; another GPU
check is unnecessary. Ordinary CPU integrity/packaging checks remain.

The official Z generated solver differs from B1 by exactly one guarded
learning-rate literal. Probe instrumentation is confined to the separate
engineering check and is absent from the official Z payload. Repeat carriers
are byte-identical to their references. Build-time hash guards preserve B0/B1
and bind Z to the source exercised by the successful real-model check.

Prepare three private saved versions in advance, preserving all three inputs,
L4x4, Internet OFF and original environment. Do not interrupt B1. Final official
Submit remains Cici's action. Five completed runs is a target, not a guarantee;
daily/pending limits and scoring completion determine which can finish.
