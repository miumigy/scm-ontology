from scm_ontology.relation_validation_batch import validate_relations
from scm_ontology.relation_validation_review import review_queue


def test_review_queue_preserves_only_review_results() -> None:
    results = validate_relations(
        (
            ("located_at", "PhysicalEntity", "Location"),
            ("located_at", "Order", "Location"),
            ("customer_specific_relation", "Order", "Location"),
        )
    )
    queued = review_queue(results)
    assert len(queued) == 1
    assert queued[0] is results[1]
