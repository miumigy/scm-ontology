from datetime import datetime, timezone

import pytest

from scm_ontology.metric_observation import MetricObservationError, observe_metric


def test_observes_metric_without_changing_metric_definition():
    observed_at = datetime(2026, 8, 14, 9, 0, tzinfo=timezone.utc)
    observation = observe_metric("OTD", 0.96, observed_at, "SITE-A", "wms:shipment:123")

    assert observation.metric_id == "OTD"
    assert observation.value == 0.96
    assert observation.observed_at == observed_at
    assert observation.entity_id == "SITE-A"
    assert observation.source_ref == "wms:shipment:123"


def test_observation_is_deterministic():
    observed_at = datetime(2026, 8, 14, 9, 0, tzinfo=timezone.utc)
    args = ("OTD", 0.96, observed_at, "SITE-A", "wms:shipment:123")
    assert observe_metric(*args) == observe_metric(*args)


@pytest.mark.parametrize(
    "metric_id,value,observed_at,entity_id,source_ref,message",
    [
        ("", 0.96, datetime(2026, 8, 14, 9, 0, tzinfo=timezone.utc), "SITE-A", "src:1", "metric_id"),
        ("OTD", 0.96, datetime(2026, 8, 14, 9, 0), "SITE-A", "src:1", "timezone-aware"),
        ("OTD", 0.96, datetime(2026, 8, 14, 9, 0, tzinfo=timezone.utc), "", "src:1", "entity_id"),
        ("OTD", 0.96, datetime(2026, 8, 14, 9, 0, tzinfo=timezone.utc), "SITE-A", "", "source_ref"),
    ],
)
def test_observation_fields_are_validated(
    metric_id, value, observed_at, entity_id, source_ref, message
):
    with pytest.raises(MetricObservationError, match=message):
        observe_metric(metric_id, value, observed_at, entity_id, source_ref)
