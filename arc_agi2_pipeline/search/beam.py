from __future__ import annotations

from typing import Sequence

from arc_agi2_pipeline.core.types import Candidate


class BeamSearchExpander:
    """Placeholder for candidate-space expansion and pruning."""

    def expand(self, seed_candidates: Sequence[Candidate]) -> Sequence[Candidate]:
        return seed_candidates
