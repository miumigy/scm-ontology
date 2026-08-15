from scm_ontology.relation_validation_batch import validate_relations
from scm_ontology.relation_validation_report import build_validation_report


def test_report_exposes_deterministic_disposition_counts() -> None:
    results = validate_relations(
        (
            ("located_at", "PhysicalEntity", "Location"),
            ("located_at", "Order", "Location"),
            ("customer_specific_relation", "Order", "Location"),
        )
    )
    report = build_validation_report(results)
    assert report.disposition_counts == {
        "accept": 1,
        "review": 1,
        "extension_candidate": 1,
    }
