from scm_ontology.canonical_relations import CANONICAL_RELATION_TYPES


def test_predicate_refs_are_unique() -> None:
    refs = [item.predicate_ref for item in CANONICAL_RELATION_TYPES]
    assert len(refs) == len(set(refs))


def test_inverse_refs_do_not_collide_with_predicate_refs_unless_declared_as_predicates() -> None:
    predicates = {item.predicate_ref for item in CANONICAL_RELATION_TYPES}
    inverses = {item.inverse_ref for item in CANONICAL_RELATION_TYPES if item.inverse_ref}
    assert all(ref in predicates or ref not in inverses for ref in inverses)
