from scm_ontology.temporal_semantics import (
    TemporalAssertion,
    TemporalReference,
    TemporalSemanticError,
)


def test_event_occurrence_is_a_point():
    reference = TemporalReference(kind="point", start="2026-08-14T09:00:00")
    assertion = TemporalAssertion.occurrence(reference)

    assert assertion.role == "occurrence"
    assert assertion.reference == reference


def test_relationship_or_state_validity_is_an_interval():
    reference = TemporalReference(
        kind="interval",
        start="2026-07-01",
        end="2026-12-31",
    )
    assertion = TemporalAssertion.validity(reference)

    assert assertion.role == "validity"
    assert assertion.reference == reference


def test_open_ended_validity_is_supported():
    reference = TemporalReference(kind="interval", start="2026-07-01")

    assert TemporalAssertion.validity(reference).reference.end is None


def test_occurrence_cannot_use_an_interval():
    reference = TemporalReference(
        kind="interval",
        start="2026-07-01",
        end="2026-12-31",
    )

    try:
        TemporalAssertion.occurrence(reference)
    except TemporalSemanticError:
        pass
    else:
        raise AssertionError("occurrence must require a point reference")


def test_point_cannot_have_end():
    try:
        TemporalReference(
            kind="point",
            start="2026-08-14T09:00:00",
            end="2026-08-14T10:00:00",
        )
    except TemporalSemanticError:
        pass
    else:
        raise AssertionError("point references cannot contain an end")


def test_temporal_literal_is_opaque():
    reference = TemporalReference(kind="point", start="business_day_42")

    assert reference.start == "business_day_42"
