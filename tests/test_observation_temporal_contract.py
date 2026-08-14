from datetime import datetime, timezone

import pytest

from scm_ontology.observation_temporal_contract import (
    ObservationTemporalContractError,
    validate_observed_at,
)


def test_accepts_timezone_aware_instant():
    observed_at = datetime(2026, 8, 14, 10, 0, tzinfo=timezone.utc)
    assert validate_observed_at(observed_at) == observed_at


def test_rejects_naive_datetime():
    with pytest.raises(ObservationTemporalContractError, match="timezone-aware"):
        validate_observed_at(datetime(2026, 8, 14, 10, 0))


def test_rejects_non_datetime():
    with pytest.raises(ObservationTemporalContractError, match="must be a datetime"):
        validate_observed_at("2026-08-14T10:00:00+00:00")
