from scm_ontology.relation_validation_pipeline import validate_relation
from scm_ontology.relation_validation_policy import ValidationDisposition, disposition_for


def test_pass_maps_to_accept() -> None:
    result = validate_relation("located_at", "PhysicalEntity", "Location")
    assert disposition_for(result) is ValidationDisposition.ACCEPT


def test_review_maps_to_review() -> None:
    result = validate_relation("located_at", "Order", "Location")
    assert disposition_for(result) is ValidationDisposition.REVIEW


def test_extension_maps_to_extension_candidate() -> None:
    result = validate_relation("customer_specific_relation", "Order", "Location")
    assert disposition_for(result) is ValidationDisposition.EXTENSION_CANDIDATE
