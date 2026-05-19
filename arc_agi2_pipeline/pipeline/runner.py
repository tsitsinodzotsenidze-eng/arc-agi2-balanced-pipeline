from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from arc_agi2_pipeline.adaptation import PerPuzzleAdapter
from arc_agi2_pipeline.augmentation import AugmentationPipeline
from arc_agi2_pipeline.core.types import Candidate, PipelineContext
from arc_agi2_pipeline.data import load_tasks_from_dir
from arc_agi2_pipeline.generators import ModelBasedGenerator, SymbolicGenerator
from arc_agi2_pipeline.search import BeamSearchExpander
from arc_agi2_pipeline.selection import TopKSelector
from arc_agi2_pipeline.submission import (
    build_submission_payload,
    validate_submission_against_tasks,
    write_submission,
)
from arc_agi2_pipeline.verification import BasicVerifier


def run(
    tasks_dir: Path, output_path: Path, max_attempts: int = 2, seed: int = 0
) -> None:
    # ARC-AGI-2 submissions require both attempt_1 and attempt_2, so keep at least two attempts.
    if max_attempts < 2:
        raise ValueError(
            "ARC-AGI-2 submissions require both attempt_1 and attempt_2; max_attempts must be at least 2."
        )

    tasks = load_tasks_from_dir(tasks_dir)
    context = PipelineContext(run_id=f"run:{tasks_dir}:{seed}", random_seed=seed)

    augment = AugmentationPipeline()
    adapt = PerPuzzleAdapter()
    generators = [ModelBasedGenerator(), SymbolicGenerator()]
    search = BeamSearchExpander()
    verifier = BasicVerifier()
    selector = TopKSelector()

    final_candidates: List[Candidate] = []

    for task in tasks:
        task_aug = augment.apply(task)
        task_adapted = adapt.adapt(task_aug)

        seed_candidates: List[Candidate] = []
        for gen in generators:
            seed_candidates.extend(gen.generate(task_adapted, context))

        expanded = search.expand(seed_candidates)
        scored = verifier.score(task_adapted, expanded, context)
        selected = selector.select(
            task_adapted, scored, max_attempts=max_attempts, context=context
        )
        final_candidates.extend(selected)

    payload = build_submission_payload(final_candidates)
    validate_submission_against_tasks(tasks, payload)
    write_submission(payload, output_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run ARC-AGI-2 pipeline scaffold.")
    parser.add_argument("--tasks-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-attempts", type=int, default=2)
    parser.add_argument("--seed", type=int, default=0)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args.tasks_dir, args.output, max_attempts=args.max_attempts, seed=args.seed)
