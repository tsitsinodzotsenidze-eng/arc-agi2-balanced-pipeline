from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Sequence

from arc_agi2_pipeline.core.types import ArcTask, Candidate, PipelineContext, ScoredCandidate


class TopKSelector:
    """Select top-k unique candidates per test index by score."""

    name = "topk_selector_v0"

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
            seen_ids = set()
            for entry in ranked:
                cid = entry.candidate.candidate_id
                if cid in seen_ids:
                    continue
                selected.append(entry.candidate)
                seen_ids.add(cid)
                if len(seen_ids) >= max_attempts:
                    break
        return selected
