import pytest

from scm_ontology.event import CanonicalEvent, EventConceptError, is_event


def test_creates_canonical_event():
    event = CanonicalEvent(
        event_id="EVT-001",
        event_type="shipment_departed",
        occurred_at="2026-09-01T09:30:00+09:00",
        subject_id="SHP-001",
    )
    assert event.event_type == "shipment_departed"
    assert is_event(event)


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"event_id": "", "event_type": "shipment_departed", "occurred_at": "2026-09-01", "subject_id": "S"}, "event_id"),
        ({"event_id": "E", "event_type": "", "occurred_at": "2026-09-01", "subject_id": "S"}, "event_type"),
        ({"event_id": "E", "event_type": "shipment_departed", "occurred_at": "", "subject_id": "S"}, "occurred_at"),
        ({"event_id": "E", "event_type": "shipment_departed", "occurred_at": "2026-09-01", "subject_id": ""}, "subject_id"),
    ],
)
def test_rejects_invalid_event(kwargs, message):
    with pytest.raises(EventConceptError, match=message):
        CanonicalEvent(**kwargs)
