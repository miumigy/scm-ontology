"""Constraint-aware reasoning over semantic supply-chain paths.

Constraints are evaluated against explicit relationship qualifiers only. No
missing value is inferred, and a failed constraint never mutates the graph.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .semantic_query import SemanticSupplyChainPath


@dataclass(frozen=True)
class PathConstraint:
    """Optional upper bounds for a supply-chain path."""

    max_total_lead_time_days: float | None = None
    min_total_capacity: float | None = None


@dataclass(frozen=True)
class ConstraintCheck:
    name: str
    passed: bool
    actual: float | None
    expected: float | None
    reason: str


@dataclass(frozen=True)
class ConstrainedPathResult:
    path: SemanticSupplyChainPath
    feasible: bool
    checks: tuple[ConstraintCheck, ...]


def _number(value: Any, key: str) -> float | None:
    value = value.get(key) if isinstance(value, dict) else None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def evaluate_path(path: SemanticSupplyChainPath, constraints: PathConstraint) -> ConstrainedPathResult:
    checks: list[ConstraintCheck] = []
    if constraints.max_total_lead_time_days is not None:
        values = [_number(step.qualifiers, "lead_time_days") for step in path.steps]
        if any(value is None for value in values):
            checks.append(ConstraintCheck("max_total_lead_time_days", False, None, constraints.max_total_lead_time_days, "missing lead_time_days"))
        else:
            total = sum(value for value in values if value is not None)
            checks.append(ConstraintCheck("max_total_lead_time_days", total <= constraints.max_total_lead_time_days, total, constraints.max_total_lead_time_days, "total lead time"))

    if constraints.min_total_capacity is not None:
        values = [_number(step.qualifiers, "capacity") for step in path.steps]
        if any(value is None for value in values):
            checks.append(ConstraintCheck("min_total_capacity", False, None, constraints.min_total_capacity, "missing capacity"))
        else:
            bottleneck = min(values)
            checks.append(ConstraintCheck("min_total_capacity", bottleneck >= constraints.min_total_capacity, bottleneck, constraints.min_total_capacity, "path bottleneck capacity"))

    return ConstrainedPathResult(path, all(check.passed for check in checks), tuple(checks))


def filter_feasible_paths(paths: tuple[SemanticSupplyChainPath, ...], constraints: PathConstraint) -> tuple[ConstrainedPathResult, ...]:
    """Evaluate all paths and return only feasible ones, preserving deterministic order."""
    return tuple(result for result in (evaluate_path(path, constraints) for path in paths) if result.feasible)
