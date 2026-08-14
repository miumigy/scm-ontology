import pytest

from scm_ontology.s141_measure import (
    MeasurementRecord,
    MeasurementStatus,
    PerformanceAssessment,
    record_measurement,
)


def test_measurement_preserves_observation_context() -> None:
    measurement = record_measurement(
        ref="measurement:service-level:1",
        subject_ref="kpi:service-level",
        value=0.94,
        unit_ref="unit:ratio",
        observation_time="2026-08-15T10:00:00Z",
        transaction_time="2026-08-15T10:01:00Z",
        method_ref="method:order-fill",
        source_ref="wms:1",
        uncertainty_ref="uncertainty:1",
    )
    assert measurement.value == 0.94
    assert measurement.is_actual is True
    assert measurement.is_metric is False


def test_measurement_is_not_performance_assessment() -> None:
    measurement = MeasurementRecord(
        ref="measurement:1",
        subject_ref="inventory:1",
        value=100,
    )
    assert measurement.is_performance_assessment is False


def test_missing_measurement_is_not_zero() -> None:
    measurement = record_measurement(
        ref="measurement:missing",
        subject_ref="inventory:1",
        value=None,
        status=MeasurementStatus.MISSING,
    )
    assert measurement.value is None


def test_stale_measurement_cannot_be_presented_as_current_value() -> None:
    with pytest.raises(ValueError):
        record_measurement(
            ref="measurement:stale",
            subject_ref="inventory:1",
            value=10,
            status=MeasurementStatus.STALE,
        )


def test_restatement_preserves_lineage() -> None:
    measurement = record_measurement(
        ref="measurement:v2",
        subject_ref="metric:cost",
        value=105,
        status=MeasurementStatus.RESTATED,
        predecessor_ref="measurement:v1",
    )
    assert measurement.predecessor_ref == "measurement:v1"


def test_performance_assessment_requires_metric_values() -> None:
    assessment = PerformanceAssessment(
        ref="assessment:1",
        subject_ref="kpi:1",
        metric_value_refs=("metric-value:1",),
        comparison_basis_refs=("target:1",),
    )
    assert assessment.is_decision is False
