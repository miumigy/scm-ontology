"""Canonical cardinality primitive for SCM relationships."""
from __future__ import annotations

from dataclasses import dataclass


class CardinalityError(ValueError):
    """Raised when a cardinality is invalid."""


@dataclass(frozen=True)
class Cardinality:
    """A minimum/maximum endpoint occurrence constraint."""

    minimum: int
    maximum: int | None = None

    def __post_init__(self) -> None:
        if self.minimum < 0:
            raise CardinalityError("minimum must be non-negative")
        if self.maximum is not None:
            if self.maximum < 0:
                raise CardinalityError("maximum must be non-negative")
            if self.maximum < self.minimum:
                raise CardinalityError("maximum must be greater than or equal to minimum")

    def allows(self, count: int) -> bool:
        if count < self.minimum:
            return False
        return self.maximum is None or count <= self.maximum

    def __str__(self) -> str:
        if self.maximum is None:
            return f"{self.minimum}..*"
        if self.minimum == self.maximum:
            return str(self.minimum)
        return f"{self.minimum}..{self.maximum}"


ONE = Cardinality(1, 1)
ZERO_OR_ONE = Cardinality(0, 1)
ZERO_OR_MANY = Cardinality(0, None)
ONE_OR_MANY = Cardinality(1, None)
