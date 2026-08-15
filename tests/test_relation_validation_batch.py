from scm_ontology.relation_validation_batch import validate_relations
from scm_ontology.relation_validation_result import ValidationStatus


def test_validate_relations_preserves_order_and_status() -> None:
    results = validate_relations(
        (
            ("located_at", "PhysicalEntity", "Location"),
            ("located_at", "Order", "Location"),
            ("customer_specific_relation", "Order", "Location"),
        )
    )
    assert [result.status for result in results] == [
        ValidationStatus.PASS,
        ValidationStatus.REVIEW,
        ValidationStatus.EXTENSION,
    ]
