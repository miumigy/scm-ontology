"""Canonical provenance semantics for metric observations."""
from __future__ import annotations

from .simulation import SimulationError


class ObservationProvenanceContractError(SimulationError):
    """Raised when observation provenance semantics are invalid."""


def validate_source_ref(source_ref: str) -> str:
    """Validate the existing observation source reference as provenance."""
    if not isinstance(source_ref, str):
        raise ObservationProvenanceContractError("source_ref must be a string")
    if not source_ref.strip():
        raise ObservationProvenanceContractError("source_ref is required")
    return source_ref
