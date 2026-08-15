from scm_ontology.canonical_relations import CANONICAL_RELATION_TYPES


def test_inverse_references_are_unique() -> None:
    inverses = [item.inverse_ref for item in CANONICAL_RELATION_TYPES if item.inverse_ref]
    assert len(inverses) == len(set(inverses))


def test_no_relation_points_to_itself() -> None:
    for item in CANONICAL_RELATION_TYPES:
        assert item.inverse_ref != item.predicate_ref
