from __future__ import annotations

from typing import Sequence

from arc_agi2_pipeline.core.types import ArcTask, Candidate, PipelineContext


class ModelBasedGenerator:
    """Interface-complete generator hook for future model-backed synthesis."""

    name = "model_interface"

    def generate(self, task: ArcTask, context: PipelineContext) -> Sequence[Candidate]:
        return []
