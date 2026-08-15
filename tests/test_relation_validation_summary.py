from scm_ontology.relation_validation_batch import validate_relations
from scm_ontology.relation_validation_summary import summarize_validation


def test_summarize_validation_counts_statuses() -> None:
    results = validate_relations(
        (
            ("located_at", "PhysicalEntity", "Location"),
            ("located_at", "Order", "Location"),
            ("customer_specific_relation", "Order", "Location"),
        )
    )
    assert summarize_validation(results) == {
        "pass": 1,
        "review": 1,
        "extension": 1,
    }
