from __future__ import annotations

from typing import List, Sequence

from arc_agi2_pipeline.core.types import ArcTask, Candidate, PipelineContext


class SymbolicGenerator:
    """Rule-interface baseline with deterministic candidate IDs and provenance."""

    name = "symbolic_rules_v0"

    def generate(self, task: ArcTask, context: PipelineContext) -> Sequence[Candidate]:
        candidates: List[Candidate] = []
        if task.train:
            template = task.train[0].output
            for i, _test in enumerate(task.test_inputs):
                candidates.append(
                    Candidate(
                        candidate_id=f"{task.task_id}:t{i}:{self.name}:0",
                        task_id=task.task_id,
                        test_index=i,
                        grid=template,
                        generator_name=self.name,
                        provenance=("train_template",),
                        metadata={"run_id": context.run_id, "strategy": "first_train_output_template"},
                    )
                )
        return candidates
