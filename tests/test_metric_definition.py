import pytest

from scm_ontology.metric_definition import MetricDefinitionError, define_metric


def test_defines_metric_without_calculation_logic():
    metric = define_metric(
        "OTD",
        "KPI",
        "metric:on_time_delivery",
        "ratio",
        "higher_is_better",
    )
    assert metric.metric_id == "OTD"
    assert metric.metric_type == "KPI"
    assert metric.semantic_ref == "metric:on_time_delivery"
    assert metric.unit == "ratio"
    assert metric.direction == "higher_is_better"


def test_definition_is_deterministic():
    args = ("OTD", "KPI", "metric:on_time_delivery", "ratio", "higher_is_better")
    assert define_metric(*args) == define_metric(*args)


@pytest.mark.parametrize(
    "metric_id,metric_type,semantic_ref,unit,direction,message",
    [
        ("", "KPI", "metric:otd", "ratio", "higher_is_better", "metric_id"),
        ("OTD", "", "metric:otd", "ratio", "higher_is_better", "metric_type"),
        ("OTD", "KPI", "", "ratio", "higher_is_better", "semantic_ref"),
        ("OTD", "KPI", "metric:otd", "", "higher_is_better", "unit"),
        ("OTD", "KPI", "metric:otd", "ratio", "neutral", "direction"),
    ],
)
def test_metric_fields_are_validated(
    metric_id, metric_type, semantic_ref, unit, direction, message
):
    with pytest.raises(MetricDefinitionError, match=message):
        define_metric(metric_id, metric_type, semantic_ref, unit, direction)
