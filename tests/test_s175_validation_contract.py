from scm_ontology.relation_validation_pipeline import validate_relation
from scm_ontology.relation_validation_result import ValidationStatus


def test_pass_for_matching_direct_types() -> None:
    result = validate_relation("located_at", "PhysicalEntity", "Location")
    assert result.status is ValidationStatus.PASS
    assert result.valid


def test_review_for_canonical_predicate_type_mismatch() -> None:
    result = validate_relation("located_at", "Order", "Location")
    assert result.status is ValidationStatus.REVIEW
    assert not result.valid


def test_extension_for_unknown_predicate() -> None:
    result = validate_relation("customer_specific_relation", "Order", "Location")
    assert result.status is ValidationStatus.EXTENSION
    assert not result.valid
