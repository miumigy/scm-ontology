from datetime import datetime, timezone

import pytest

from scm_ontology.observation import Observation


def test_observation_keeps_observation_time_separate_from_claim_validity():
    observed_at = datetime(2026, 8, 2, 10, 30, tzinfo=timezone.utc)
    observation = Observation("O1", observed_at, "Shipment-001")
    assert observation.observed_at == observed_at
    assert observation.subject_id == "Shipment-001"


def test_observation_requires_identity():
    with pytest.raises(ValueError):
        Observation("", datetime(2026, 8, 2, tzinfo=timezone.utc), "Shipment-001")


def test_observation_requires_subject_reference():
    with pytest.raises(ValueError):
        Observation("O1", datetime(2026, 8, 2, tzinfo=timezone.utc), "")
