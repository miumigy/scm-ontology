from scm_ontology.relation_validation_pipeline import validate_relation
from scm_ontology.relation_validation_result import ValidationStatus


def test_valid_relation_returns_pass() -> None:
    result = validate_relation("located_at", "PhysicalEntity", "Location")
    assert result.status is ValidationStatus.PASS
    assert result.domain_ok and result.range_ok


def test_type_mismatch_returns_review() -> None:
    result = validate_relation("located_at", "Order", "Location")
    assert result.status is ValidationStatus.REVIEW
    assert not result.valid


def test_unknown_predicate_returns_extension() -> None:
    result = validate_relation("customer_specific_relation", "Order", "Location")
    assert result.status is ValidationStatus.EXTENSION
    assert not result.valid
