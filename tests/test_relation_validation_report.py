from scm_ontology.relation_validation_batch import validate_relations
from scm_ontology.relation_validation_policy import ValidationDisposition
from scm_ontology.relation_validation_report import build_validation_report


def test_report_preserves_results_and_exposes_dispositions() -> None:
    results = validate_relations(
        (
            ("located_at", "PhysicalEntity", "Location"),
            ("located_at", "Order", "Location"),
            ("customer_specific_relation", "Order", "Location"),
        )
    )
    report = build_validation_report(results)
    assert report.results == results
    assert report.dispositions == (
        ValidationDisposition.ACCEPT,
        ValidationDisposition.REVIEW,
        ValidationDisposition.EXTENSION_CANDIDATE,
    )
