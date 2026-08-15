import pytest

from scm_ontology.relation_constraints import (
    CANONICAL_RELATION_CONSTRAINTS,
    RelationConstraintError,
    relation_constraint,
)


def test_relation_constraints_are_unique() -> None:
    predicates = [item.predicate_ref for item in CANONICAL_RELATION_CONSTRAINTS]
    assert len(predicates) == len(set(predicates))


def test_located_at_has_location_range() -> None:
    constraint = relation_constraint("located_at")
    assert "Location" in constraint.range
    assert "PhysicalEntity" in constraint.domain


def test_unknown_relation_constraint_is_rejected() -> None:
    with pytest.raises(RelationConstraintError, match="no canonical domain/range constraint"):
        relation_constraint("customer_specific_relation")
