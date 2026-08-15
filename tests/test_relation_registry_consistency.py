from scm_ontology.canonical_relations import CANONICAL_RELATION_TYPES
from scm_ontology.relation_constraints import CANONICAL_RELATION_CONSTRAINTS


def test_relation_constraint_predicates_are_registered() -> None:
    registered = {item.predicate_ref for item in CANONICAL_RELATION_TYPES}
    constrained = {item.predicate_ref for item in CANONICAL_RELATION_CONSTRAINTS}
    assert constrained <= registered


def test_inverse_references_are_not_accidentally_registered_as_required_constraints() -> None:
    registered = {item.predicate_ref for item in CANONICAL_RELATION_TYPES}
    inverses = {item.inverse_ref for item in CANONICAL_RELATION_TYPES if item.inverse_ref}
    assert inverses - registered
