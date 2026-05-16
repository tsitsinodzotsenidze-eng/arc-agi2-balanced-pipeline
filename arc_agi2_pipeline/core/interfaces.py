from __future__ import annotations

from typing import Protocol, Sequence

from .types import ArcTask, Candidate, PipelineContext, ScoredCandidate


class CandidateGenerator(Protocol):
    name: str

    def generate(self, task: ArcTask, context: PipelineContext) -> Sequence[Candidate]:
        ...


class CandidateVerifier(Protocol):
    name: str

    def score(
        self,
        task: ArcTask,
        candidates: Sequence[Candidate],
        context: PipelineContext,
    ) -> Sequence[ScoredCandidate]:
        ...


class CandidateSelector(Protocol):
    name: str

    def select(
        self,
        task: ArcTask,
        scored: Sequence[ScoredCandidate],
        max_attempts: int,
        context: PipelineContext,
    ) -> Sequence[Candidate]:
        ...
