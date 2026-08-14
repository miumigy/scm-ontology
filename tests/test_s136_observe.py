import pytest

from scm_ontology.s136_observe import (
    Observation,
    ObservationEpistemicStatus,
    record_observation,
)


def test_observation_preserves_source_and_time() -> None:
    observation = record_observation(
        ref="observation:stock:1",
        subject_ref="inventory:sku-1:warehouse-a",
        observed_at="2026-08-15T10:00:00Z",
        value=120,
        source_ref="wms:stock",
        unit_ref="unit:each",
        provenance_refs=("source:wms",),
    )
    assert observation.source_ref == "wms:stock"
    assert observation.observed_at != "2026-08-15T09:00:00Z"
    assert observation.is_event is False
    assert observation.is_state is False


def test_prediction_is_not_observed_fact() -> None:
    observation = record_observation(
        ref="observation:forecast:1",
        subject_ref="demand:sku-1",
        observed_at="2026-08-15T10:00:00Z",
        value=200,
        epistemic_status=ObservationEpistemicStatus.PREDICTED,
    )
    assert observation.epistemic_status is ObservationEpistemicStatus.PREDICTED
    assert observation.is_inference is False


def test_inference_is_explicit() -> None:
    observation = Observation(
        ref="observation:inferred:1",
        subject_ref="inventory:sku-1",
        observed_at="2026-08-15T10:00:00Z",
        value=100,
        epistemic_status=ObservationEpistemicStatus.INFERRED,
    )
    assert observation.is_inference is True


def test_unknown_value_is_not_zero() -> None:
    observation = record_observation(
        ref="observation:missing:1",
        subject_ref="inventory:sku-2",
        observed_at="2026-08-15T10:00:00Z",
        value=None,
        epistemic_status=ObservationEpistemicStatus.UNKNOWN,
    )
    assert observation.value is None
    assert observation.epistemic_status is ObservationEpistemicStatus.UNKNOWN


def test_observation_requires_subject_and_time() -> None:
    with pytest.raises(ValueError):
        Observation(ref="observation:bad", subject_ref="", observed_at="", value=1)
