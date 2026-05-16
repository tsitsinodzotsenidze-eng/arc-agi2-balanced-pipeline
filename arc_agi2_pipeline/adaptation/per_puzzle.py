from __future__ import annotations

from arc_agi2_pipeline.core.types import ArcTask


class PerPuzzleAdapter:
    """Placeholder for per-task prompt/program/hyperparameter adaptation."""

    def adapt(self, task: ArcTask) -> ArcTask:
        return task
