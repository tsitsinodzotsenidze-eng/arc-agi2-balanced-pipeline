from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

ArcGrid = List[List[int]]


@dataclass(frozen=True)
class ArcPair:
    input: ArcGrid
    output: ArcGrid


@dataclass(frozen=True)
class ArcTask:
    task_id: str
    train: Sequence[ArcPair]
    test_inputs: Sequence[ArcGrid]
    source_path: Optional[str] = None


@dataclass(frozen=True)
class PipelineContext:
    run_id: str
    random_seed: int = 0
    tags: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    task_id: str
    test_index: int
    grid: ArcGrid
    generator_name: str
    provenance: Tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ScoredCandidate:
    candidate: Candidate
    score: float
    passed: bool
    reasons: Tuple[str, ...] = ()
    metrics: Mapping[str, float] = field(default_factory=dict)
