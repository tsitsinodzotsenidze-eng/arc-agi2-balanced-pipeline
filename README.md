# ARC-AGI-2 Strong Balanced Competitive Pipeline

## Current checkpoint — 28 October 2026

The repository now includes a bounded, standard-library symbolic program
solver and a Kaggle bundled-challenges adapter. One predeclared public pilot
compared geometric depth 1 versus depth 2: both scored **0/167 test outputs**
on 120 public evaluation tasks, with no demonstration-consistent programs.
This records a grammar-coverage limit; v1 is **not ready as a meaningful
competition candidate**. A separate attributed [NVARC port](nvarc_port/README.md)
is packaged, with runtime validation still pending.

- [Frozen protocol](docs/EXPERIMENT_PROTOCOL_2026-10-28.md)
- [Results and reproduction](docs/RESULTS_PUBLIC_V1_2026-10-28.md)
- [Source/data freeze](docs/EXPERIMENT_FREEZE_V1.json)
- [Public data provenance](docs/DATA_PROVENANCE.md)
- [Raw results](evidence/public-v1/results.json)
- [Continuation checkpoint](docs/CONTINUATION_2026-10-29.md)

Tests: `python -m pytest -q` — 68 passed, including nine CPU-only NVARC wrapper
checks, on Python 3.12. Solver inference is CPU-only,
offline, and receives no test-output labels. Official competition submission
is a separate human action; none was performed for this work.

Run a Kaggle-style bundle:

```sh
python -m arc_agi2_pipeline.pipeline.runner --challenges-json /path/to/arc-agi_test_challenges.json --output submission.json --audit audit.json --max-depth 2
```

The earlier architecture roadmap below is retained as planned future work.
The legacy model hook, search/augmentation hooks and structural verifier are
not used by the new explicit train-consistent program entrypoint.

This repository is a **serious architecture scaffold** for an ARC-AGI-2 balanced competitive system intended to improve hidden-task solve probability over time.

It is designed to scale into a full stack with:
- model-based hypothesis generation
- symbolic/rule-based generation
- augmentation and inverse transforms
- per-puzzle adaptation
- search/beam expansion
- verification/scoring
- candidate selection
- strict submission validation

## Current Status

This phase establishes production-grade structure and contracts before heavy dependencies:
- typed core data contracts with provenance-ready candidates
- protocol-based generator/verifier/selector interfaces
- schema-validating ARC task loading
- deterministic runner context (run id + seed)
- strict submission payload validation and deterministic output writing
- executable end-to-end orchestration path

## Repository Layout

- `arc_agi2_pipeline/core/`: canonical task/candidate types and interfaces.
- `arc_agi2_pipeline/data/`: validated ARC JSON loading.
- `arc_agi2_pipeline/generators/`: model-interface and symbolic-rule generators.
- `arc_agi2_pipeline/augmentation/`: augmentation and inverse-transform hooks.
- `arc_agi2_pipeline/adaptation/`: per-puzzle adaptation hooks.
- `arc_agi2_pipeline/search/`: candidate-space expansion hooks.
- `arc_agi2_pipeline/verification/`: deterministic structural scoring scaffold.
- `arc_agi2_pipeline/selection/`: ranked per-test attempt selection.
- `arc_agi2_pipeline/submission/`: payload building, validation, and writing.
- `arc_agi2_pipeline/pipeline/`: orchestration entrypoint.
- `tests/`: foundational correctness tests.
- `docs/`: staged implementation plan.

## Intended Flow

`load data → generate candidates → verify/score → select attempts → write submission`

## Run

```bash
python -m arc_agi2_pipeline.pipeline.runner \
  --tasks-dir /path/to/arc_tasks \
  --output submission.json \
  --seed 0
```

## Test

```bash
pytest
```

## Non-goals for this phase

- no heavy model runtime dependencies yet
- no external network dependency assumptions
- no hidden/private data coupling

See `docs/implementation_plan.md` for staged upgrades.
