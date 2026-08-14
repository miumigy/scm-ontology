import pytest

from scm_ontology.relationship_constraints import (
    CANONICAL_RELATIONSHIP_CONSTRAINTS,
    RelationshipConstraint,
    RelationshipConstraintError,
    get_relationship_constraint,
    validate_relationship,
)


def test_known_relationships_have_explicit_endpoint_constraints():
    assert get_relationship_constraint("places").allows("Party", "CustomerOrder")
    assert get_relationship_constraint("establishes").allows("Event", "State")
    assert len(CANONICAL_RELATIONSHIP_CONSTRAINTS) == 9


def test_unknown_predicate_is_not_rejected_by_s42():
    validate_relationship("domain_specific_predicate", "CustomEntity", "CustomEntity")


def test_rejects_invalid_endpoints():
    with pytest.raises(RelationshipConstraintError, match="invalid endpoints for places"):
        validate_relationship("places", "Shipment", "Party")


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"predicate": "", "allowed_from": ("Party",), "allowed_to": ("Order",)}, "predicate"),
        ({"predicate": "places", "allowed_from": (), "allowed_to": ("Order",)}, "allowed_from"),
        ({"predicate": "places", "allowed_from": ("Party",), "allowed_to": ()}, "allowed_to"),
    ],
)
def test_rejects_invalid_constraint(kwargs, message):
    with pytest.raises(RelationshipConstraintError, match=message):
        RelationshipConstraint(**kwargs)
