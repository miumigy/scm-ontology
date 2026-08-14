import pytest

from scm_ontology.metric_impact_link import MetricImpactLinkError, link_metric_impact


def test_links_impact_to_metric():
    link = link_metric_impact("impact-1", "OTD")

    assert link.impact_id == "impact-1"
    assert link.metric_id == "OTD"
    assert link.relationship == "impacts"


def test_link_is_deterministic():
    args = ("impact-1", "OTD", "impacts")
    assert link_metric_impact(*args) == link_metric_impact(*args)


@pytest.mark.parametrize(
    "impact_id,metric_id,relationship,message",
    [
        ("", "OTD", "impacts", "impact_id"),
        ("impact-1", "", "impacts", "metric_id"),
        ("impact-1", "OTD", "measures", "relationship must be impacts"),
    ],
)
def test_link_fields_are_validated(
    impact_id, metric_id, relationship, message
):
    with pytest.raises(MetricImpactLinkError, match=message):
        link_metric_impact(impact_id, metric_id, relationship)
