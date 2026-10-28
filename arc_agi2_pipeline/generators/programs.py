"""Bounded train-consistent symbolic programs; no test targets enter this API."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import product
from typing import Any

from arc_agi2_pipeline.core.types import ArcGrid, ArcTask

SOLVER_VERSION = "symbolic-programs-v1"
OPS = tuple(sorted(
    ["rot90", "rot180", "rot270", "flip_h", "flip_v", "transpose", "anti_transpose"]
    + [f"crop_{c}" for c in range(10)] + ["crop_dominant"]
    + ["scale_2", "scale_3"]
    + [f"tile_{r}_{c}" for r in (2, 3) for c in (2, 3)]
))


def grid_key(grid: ArcGrid) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(row) for row in grid)


def apply_op(grid: ArcGrid, op: str) -> ArcGrid | None:
    h, w = len(grid), len(grid[0])
    if op == "rot90":
        out = [list(row) for row in zip(*grid[::-1])]
    elif op == "rot180":
        out = [row[::-1] for row in grid[::-1]]
    elif op == "rot270":
        out = [list(row) for row in zip(*grid)][::-1]
    elif op == "flip_h":
        out = [row[::-1] for row in grid]
    elif op == "flip_v":
        out = [row[:] for row in grid[::-1]]
    elif op == "transpose":
        out = [list(row) for row in zip(*grid)]
    elif op == "anti_transpose":
        out = [list(row)[::-1] for row in zip(*grid)][::-1]
    elif op.startswith("crop_"):
        if op == "crop_dominant":
            counts = Counter(v for row in grid for v in row)
            background = min(counts, key=lambda v: (-counts[v], v))
        else:
            background = int(op.split("_")[1])
        cells = [(r, c) for r, row in enumerate(grid) for c, v in enumerate(row) if v != background]
        if not cells:
            return None
        r0, r1 = min(r for r, _ in cells), max(r for r, _ in cells)
        c0, c1 = min(c for _, c in cells), max(c for _, c in cells)
        out = [row[c0:c1 + 1] for row in grid[r0:r1 + 1]]
    elif op.startswith("scale_"):
        n = int(op.split("_")[1])
        if h * n > 30 or w * n > 30:
            return None
        out = [[v for v in row for _ in range(n)] for row in grid for _ in range(n)]
    elif op.startswith("tile_"):
        _, rs, cs = op.split("_")
        r, c = int(rs), int(cs)
        if h * r > 30 or w * c > 30:
            return None
        out = [row * c for _ in range(r) for row in grid]
    else:
        raise ValueError(f"Unknown operator: {op}")
    return out


def transform(grid: ArcGrid, program: tuple[str, ...]) -> ArcGrid | None:
    out = [row[:] for row in grid]
    for op in program:
        out = apply_op(out, op)
        if out is None:
            return None
    return out


@dataclass(frozen=True)
class FittedProgram:
    ops: tuple[str, ...]
    color_map: tuple[tuple[int, int], ...]

    @property
    def rank(self) -> tuple:
        return (len(self.ops), sum(a != b for a, b in self.color_map), self.ops, self.color_map)

    def predict(self, grid: ArcGrid) -> ArcGrid | None:
        out = transform(grid, self.ops)
        if out is None:
            return None
        mapping = dict(self.color_map)
        return [[mapping.get(v, v) for v in row] for row in out]

    def describe(self) -> dict[str, Any]:
        return {"ops": list(self.ops), "color_map": [list(x) for x in self.color_map]}


def fit_program(task: ArcTask, program: tuple[str, ...]) -> FittedProgram | None:
    if not task.train:
        return None
    mapping: dict[int, int] = {}
    for pair in task.train:
        out = transform(pair.input, program)
        if out is None or len(out) != len(pair.output) or len(out[0]) != len(pair.output[0]):
            return None
        for row, target_row in zip(out, pair.output):
            for v, target in zip(row, target_row):
                if v in mapping and mapping[v] != target:
                    return None
                mapping[v] = target
    fitted = FittedProgram(program, tuple(sorted(mapping.items())))
    if not all(fitted.predict(pair.input) == pair.output for pair in task.train):
        raise AssertionError("Internal train-consistency failure")
    return fitted


def solve_task(task: ArcTask, max_depth: int = 2) -> tuple[list[list[ArcGrid]], dict[str, Any]]:
    if max_depth not in (1, 2):
        raise ValueError("max_depth must be 1 or 2")
    if not task.test_inputs:
        raise ValueError("task must contain test inputs")
    programs = [()]
    for depth in range(1, max_depth + 1):
        programs.extend(product(OPS, repeat=depth))
    fitted = [p for ops in programs if (p := fit_program(task, ops)) is not None]
    fitted.sort(key=lambda p: p.rank)
    predictions: list[list[ArcGrid]] = []
    selections = []
    for test_grid in task.test_inputs:
        choices: list[ArcGrid] = []
        evidence = []
        seen = set()
        for p in fitted:
            out = p.predict(test_grid)
            if out is None or grid_key(out) in seen:
                continue
            seen.add(grid_key(out))
            choices.append(out)
            evidence.append({"source": "train_consistent_program", **p.describe()})
            if len(choices) == 2:
                break
        if len(choices) == 1:
            choices.append([row[:] for row in choices[0]])
            evidence.append({**evidence[0], "source": "duplicate_verified"})
        elif not choices:
            template = task.train[0].output if task.train else test_grid
            choices = [[row[:] for row in test_grid], [row[:] for row in template]]
            evidence = [{"source": "fallback_identity"}, {"source": "fallback_first_train_output"}]
        predictions.append(choices)
        selections.append(evidence)
    return predictions, {
        "solver_version": SOLVER_VERSION, "max_depth": max_depth,
        "programs_enumerated": len(programs), "train_consistent_programs": len(fitted),
        "selected": selections,
    }
