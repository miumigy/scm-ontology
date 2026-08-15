import pytest

from scm_ontology.relation_instance_validation import (
    RelationInstanceValidationError,
    validate_relation_instance,
)


def test_valid_relation_instance() -> None:
    validate_relation_instance("located_at", "PhysicalEntity", "Location")


def test_invalid_domain_is_rejected() -> None:
    with pytest.raises(RelationInstanceValidationError, match="invalid domain"):
        validate_relation_instance("located_at", "Order", "Location")


def test_invalid_range_is_rejected() -> None:
    with pytest.raises(RelationInstanceValidationError, match="invalid range"):
        validate_relation_instance("located_at", "PhysicalEntity", "Order")
