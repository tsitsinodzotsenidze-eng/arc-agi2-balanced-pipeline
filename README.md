# ARC-AGI-2 Strong Balanced Competitive Pipeline

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
