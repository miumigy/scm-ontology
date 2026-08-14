"""S57 canonical temporal semantics.

This module distinguishes temporal *roles* from temporal representations.
It intentionally does not parse timestamps or implement interval arithmetic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

TemporalKind = Literal["point", "interval"]
TemporalRole = Literal["occurrence", "validity"]


class TemporalSemanticError(ValueError):
    """Raised when a canonical temporal contract is violated."""


@dataclass(frozen=True)
class TemporalReference:
    """A minimal temporal point or interval.

    Values are opaque temporal literals. Their concrete syntax and timezone
    policy are intentionally outside this contract.
    """

    kind: TemporalKind
    start: str
    end: str | None = None

    def __post_init__(self) -> None:
        if not self.start.strip():
            raise TemporalSemanticError("temporal start must be non-empty")
        if self.kind == "point" and self.end is not None:
            raise TemporalSemanticError("point references cannot have an end")
        if self.kind == "interval" and self.end == "":
            raise TemporalSemanticError("interval end must be non-empty when provided")


@dataclass(frozen=True)
class TemporalAssertion:
    """Associates a temporal reference with a semantic role."""

    role: TemporalRole
    reference: TemporalReference

    def __post_init__(self) -> None:
        expected = "point" if self.role == "occurrence" else "interval"
        if self.reference.kind != expected:
            raise TemporalSemanticError(
                f"{self.role} requires a {expected} temporal reference"
            )

    @classmethod
    def occurrence(cls, reference: TemporalReference) -> "TemporalAssertion":
        return cls(role="occurrence", reference=reference)

    @classmethod
    def validity(cls, reference: TemporalReference) -> "TemporalAssertion":
        return cls(role="validity", reference=reference)
