"""Canonical temporal semantics for metric observations."""
from __future__ import annotations

from datetime import datetime

from .simulation import SimulationError


class ObservationTemporalContractError(SimulationError):
    """Raised when observation temporal semantics are invalid."""


def validate_observed_at(observed_at: datetime) -> datetime:
    """Validate an observation timestamp as a timezone-aware instant."""
    if not isinstance(observed_at, datetime):
        raise ObservationTemporalContractError("observed_at must be a datetime")
    if observed_at.tzinfo is None or observed_at.utcoffset() is None:
        raise ObservationTemporalContractError("observed_at must be timezone-aware")
    return observed_at
