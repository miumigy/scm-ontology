import pytest

from scm_ontology.temporal import (
    CanonicalDuration,
    CanonicalTimeInterval,
    TemporalConceptError,
    is_duration,
    is_time_interval,
)


def test_creates_duration():
    duration = CanonicalDuration(value=27.5, unit="minutes")
    assert duration.value == 27.5
    assert is_duration(duration)


def test_creates_time_interval():
    interval = CanonicalTimeInterval(
        start="2026-09-01T09:00:00+09:00",
        end="2026-09-01T09:27:30+09:00",
    )
    assert interval.start < interval.end
    assert is_time_interval(interval)


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"value": -1, "unit": "minutes"}, "non-negative"),
        ({"value": 1, "unit": ""}, "unit"),
    ],
)
def test_rejects_invalid_duration(kwargs, message):
    with pytest.raises(TemporalConceptError, match=message):
        CanonicalDuration(**kwargs)


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"start": "", "end": "2026-09-01"}, "start"),
        ({"start": "2026-09-01", "end": ""}, "end"),
    ],
)
def test_rejects_invalid_interval(kwargs, message):
    with pytest.raises(TemporalConceptError, match=message):
        CanonicalTimeInterval(**kwargs)
