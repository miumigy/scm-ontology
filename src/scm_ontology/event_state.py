"""Canonical Event and State semantic primitives."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CanonicalEvent:
    """An occurrence in the SCM domain.

    ``event_id`` identifies this occurrence; ``event_type`` identifies its
    semantic kind. Timing, causality, and persistence policies are modeled by
    separate contracts rather than embedded here.
    """

    event_id: str
    event_type: str


@dataclass(frozen=True)
class CanonicalState:
    """A condition or configuration that holds for a canonical subject."""

    state_id: str
    state_type: str
    subject_id: str
