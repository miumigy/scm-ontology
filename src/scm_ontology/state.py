"""Canonical state concept for the SCM domain layer."""
from __future__ import annotations

from dataclasses import dataclass


class StateConceptError(ValueError):
    """Raised when a canonical state is invalid."""


@dataclass(frozen=True)
class CanonicalState:
    """The effective state of a subject at a defined point in time."""

    state_type: str
    subject_id: str
    effective_at: str

    def __post_init__(self) -> None:
        if not self.state_type.strip():
            raise StateConceptError("state_type must be non-empty")
        if not self.subject_id.strip():
            raise StateConceptError("subject_id must be non-empty")
        if not self.effective_at.strip():
            raise StateConceptError("effective_at must be non-empty")


def is_state(value: object) -> bool:
    return isinstance(value, CanonicalState)
