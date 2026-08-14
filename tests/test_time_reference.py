import pytest

from scm_ontology.time_reference import (
    CANONICAL_TIME_TYPES,
    CanonicalTimeReference,
    TimeReferenceError,
    is_time_reference,
)


def test_creates_canonical_time_reference():
    reference = CanonicalTimeReference(
        value="2026-09-01T09:30:00+09:00",
        time_type="occurred_at",
    )
    assert reference.time_type == "occurred_at"
    assert is_time_reference(reference)


def test_time_types_are_explicit():
    assert CANONICAL_TIME_TYPES == (
        "occurred_at",
        "effective_at",
        "planned_at",
        "requested_at",
        "confirmed_at",
    )


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"value": "", "time_type": "occurred_at"}, "value"),
        ({"value": "2026-09-01", "time_type": ""}, "time_type"),
    ],
)
def test_rejects_invalid_time_reference(kwargs, message):
    with pytest.raises(TimeReferenceError, match=message):
        CanonicalTimeReference(**kwargs)
