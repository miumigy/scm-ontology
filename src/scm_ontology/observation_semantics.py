"""Semantic boundary between observations, states, and events."""
from __future__ import annotations

from enum import Enum


class ObservationSemanticBoundaryError(ValueError):
    """Raised when a semantic classification violates the canonical boundary."""


class SemanticKind(str, Enum):
    OBSERVATION = "observation"
    STATE = "state"
    EVENT = "event"


def validate_semantic_kind(kind: SemanticKind) -> SemanticKind:
    """Accept only explicit semantic kinds; no implicit inference is performed."""
    if not isinstance(kind, SemanticKind):
        raise ObservationSemanticBoundaryError("kind must be an explicit SemanticKind")
    return kind


def semantic_definition(kind: SemanticKind) -> str:
    """Return the canonical distinction for a semantic kind."""
    validate_semantic_kind(kind)
    return {
        SemanticKind.OBSERVATION: "a measured fact about an entity at an observation instant",
        SemanticKind.STATE: "a condition or configuration that holds for an entity over a period",
        SemanticKind.EVENT: "an occurrence that happens at or over a point or interval in time",
    }[kind]
