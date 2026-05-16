from __future__ import annotations

from typing import List, Sequence

from arc_agi2_pipeline.core.types import ArcTask, Candidate, PipelineContext, ScoredCandidate


class BasicVerifier:
    """Deterministic structural verifier scaffold with extensible metrics."""

    name = "structural_verifier_v0"

    def score(
        self,
        task: ArcTask,
        candidates: Sequence[Candidate],
        context: PipelineContext,
    ) -> Sequence[ScoredCandidate]:
        scored: List[ScoredCandidate] = []
        for c in candidates:
            valid_shape = len(c.grid) > 0 and all(len(row) == len(c.grid[0]) for row in c.grid)
            score = 0.5 if valid_shape else 0.0
            scored.append(
                ScoredCandidate(
                    candidate=c,
                    score=score,
                    passed=valid_shape,
                    reasons=("rectangular_grid",) if valid_shape else ("non_rectangular_grid",),
                    metrics={"shape_valid": 1.0 if valid_shape else 0.0, "seed": float(context.random_seed)},
                )
            )
        return scored
