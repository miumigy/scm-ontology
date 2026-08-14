from dataclasses import dataclass
from typing import Any, Tuple


@dataclass(frozen=True)
class ConstraintExpression:
    """Canonical structural expression for a constraint.

    The expression is intentionally not executable. Evaluation semantics belong
    to a validation or policy runtime outside the canonical model.
    """

    kind: str
    value: Any = None
    children: Tuple["ConstraintExpression", ...] = ()

    @classmethod
    def atomic(cls, value: Any) -> "ConstraintExpression":
        return cls(kind="atomic", value=value)

    @classmethod
    def all(cls, *children: "ConstraintExpression") -> "ConstraintExpression":
        return cls(kind="all", children=tuple(children))

    @classmethod
    def any(cls, *children: "ConstraintExpression") -> "ConstraintExpression":
        return cls(kind="any", children=tuple(children))

    @classmethod
    def not_(cls, child: "ConstraintExpression") -> "ConstraintExpression":
        return cls(kind="not", children=(child,))
