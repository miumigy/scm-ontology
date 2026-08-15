from scm_ontology.relation_validation_batch import validate_relations
from scm_ontology.relation_validation_extension import extension_candidate_queue


def test_extension_candidate_queue_preserves_only_candidates() -> None:
    results = validate_relations(
        (
            ("located_at", "PhysicalEntity", "Location"),
            ("located_at", "Order", "Location"),
            ("customer_specific_relation", "Order", "Location"),
        )
    )
    queued = extension_candidate_queue(results)
    assert len(queued) == 1
    assert queued[0] is results[2]
