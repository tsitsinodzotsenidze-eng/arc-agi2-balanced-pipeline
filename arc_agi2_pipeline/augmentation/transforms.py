from __future__ import annotations

from arc_agi2_pipeline.core.types import ArcTask


class AugmentationPipeline:
    """Placeholder for forward/inverse transforms and test-time augmentation."""

    def apply(self, task: ArcTask) -> ArcTask:
        return task
