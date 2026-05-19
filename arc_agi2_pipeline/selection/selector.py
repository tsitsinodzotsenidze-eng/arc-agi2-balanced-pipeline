from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Sequence, Tuple

from arc_agi2_pipeline.core.types import ArcGrid, ArcTask, Candidate, PipelineContext, ScoredCandidate


def _grid_key(grid: ArcGrid) -> Tuple[Tuple[int, ...], ...]:
    """Return a hashable canonical key for exact grid equality checks."""
    return tuple(tuple(row) for row in grid)


class TopKSelector:
    """Select top-k candidates per test index with grid-level attempt diversity.

    Contract:
    - Candidates are ranked deterministically by score, then candidate_id.
    - attempt diversity is preferred at the grid level, not just candidate_id level.
    - If fewer than max_attempts grid-unique candidates exist, the selector falls
      back to additional candidate-id-unique entries in ranked order so downstream
      submission construction can still receive the required number of attempts.
    """

    name = "topk_selector_v1"

    def select(
        self,
        task: ArcTask,
        scored: Sequence[ScoredCandidate],
        max_attempts: int,
        context: PipelineContext,
    ) -> Sequence[Candidate]:
        del context
        by_test: Dict[int, List[ScoredCandidate]] = defaultdict(list)
        for item in scored:
            by_test[item.candidate.test_index].append(item)

        selected: List[Candidate] = []
        for test_index in range(len(task.test_inputs)):
            ranked = sorted(
                by_test.get(test_index, []),
                key=lambda x: (x.score, x.candidate.candidate_id),
                reverse=True,
            )

            chosen: List[Candidate] = []
            seen_ids = set()
            seen_grids = set()

            for entry in ranked:
                candidate = entry.candidate
                if candidate.candidate_id in seen_ids:
                    continue
                grid_key = _grid_key(candidate.grid)
                if grid_key in seen_grids:
                    continue
                chosen.append(candidate)
                seen_ids.add(candidate.candidate_id)
                seen_grids.add(grid_key)
                if len(chosen) >= max_attempts:
                    break

            if len(chosen) < max_attempts:
                for entry in ranked:
                    candidate = entry.candidate
                    if candidate.candidate_id in seen_ids:
                        continue
                    chosen.append(candidate)
                    seen_ids.add(candidate.candidate_id)
                    if len(chosen) >= max_attempts:
                        break

            selected.extend(chosen)
        return selected
