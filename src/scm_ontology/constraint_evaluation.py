from dataclasses import dataclass
from enum import Enum
from typing import Any


class ConstraintResult(str, Enum):
    SATISFIED = "satisfied"
    VIOLATED = "violated"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class EvaluationContext:
    """Canonical context supplied to an external constraint evaluator."""

    facts: Any


@dataclass(frozen=True)
class ConstraintEvaluation:
    """Canonical result of evaluating a constraint expression."""

    result: ConstraintResult
    reason: str | None = None
