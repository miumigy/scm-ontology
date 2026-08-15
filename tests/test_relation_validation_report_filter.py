from scm_ontology.relation_validation_batch import validate_relations
from scm_ontology.relation_validation_policy import ValidationDisposition
from scm_ontology.relation_validation_report import build_validation_report


def test_report_filters_without_reordering_or_mutating_results() -> None:
    report = build_validation_report(
        validate_relations(
            (
                ("located_at", "PhysicalEntity", "Location"),
                ("located_at", "Order", "Location"),
                ("customer_specific_relation", "Order", "Location"),
            )
        )
    )
    assert len(report.by_disposition(ValidationDisposition.ACCEPT)) == 1
    assert len(report.by_disposition(ValidationDisposition.REVIEW)) == 1
    assert len(report.by_disposition(ValidationDisposition.EXTENSION_CANDIDATE)) == 1
    assert len(report.results) == 3
