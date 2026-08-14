from datetime import datetime, timezone

import pytest

from scm_ontology.canonical_event import CanonicalEvent, CanonicalEventError, is_event


def test_creates_canonical_event():
    event = CanonicalEvent(
        event_type="shipment_dispatched",
        occurred_at=datetime(2026, 8, 14, 10, 0, tzinfo=timezone.utc),
        entity_id="SHIPMENT-1",
        attributes={"mode": "road"},
    )
    assert event.event_type == "shipment_dispatched"
    assert event.entity_id == "SHIPMENT-1"
    assert is_event(event)


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"event_type": "", "occurred_at": datetime(2026, 8, 14, tzinfo=timezone.utc), "entity_id": "X", "attributes": {}}, "event_type"),
        ({"event_type": "dispatch", "occurred_at": datetime(2026, 8, 14), "entity_id": "X", "attributes": {}}, "timezone-aware"),
        ({"event_type": "dispatch", "occurred_at": datetime(2026, 8, 14, tzinfo=timezone.utc), "entity_id": "", "attributes": {}}, "entity_id"),
        ({"event_type": "dispatch", "occurred_at": datetime(2026, 8, 14, tzinfo=timezone.utc), "entity_id": "X", "attributes": None}, "attributes"),
    ],
)
def test_event_contract_is_validated(kwargs, message):
    with pytest.raises(CanonicalEventError, match=message):
        CanonicalEvent(**kwargs)
