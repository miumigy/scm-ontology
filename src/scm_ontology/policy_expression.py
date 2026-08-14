from dataclasses import dataclass
from typing import Any, Tuple


@dataclass(frozen=True)
class PolicyExpression:
    """Canonical structural expression for policy applicability or preference."""

    kind: str
    value: Any = None
    children: Tuple["PolicyExpression", ...] = ()

    @classmethod
    def atomic(cls, value: Any) -> "PolicyExpression":
        return cls(kind="atomic", value=value)

    @classmethod
    def all(cls, *children: "PolicyExpression") -> "PolicyExpression":
        return cls(kind="all", children=tuple(children))

    @classmethod
    def any(cls, *children: "PolicyExpression") -> "PolicyExpression":
        return cls(kind="any", children=tuple(children))

    @classmethod
    def not_(cls, child: "PolicyExpression") -> "PolicyExpression":
        return cls(kind="not", children=(child,))
