from scm_ontology.extension_candidate_report import build_extension_candidate_report
from scm_ontology.relation_validation_batch import validate_relations


def test_extension_candidate_report_is_immutable_and_ordered() -> None:
    results = validate_relations(
        (
            ("located_at", "PhysicalEntity", "Location"),
            ("customer_specific_relation", "Order", "Location"),
        )
    )
    report = build_extension_candidate_report(results)
    assert report.candidates == (results[1],)
