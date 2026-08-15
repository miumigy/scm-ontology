from scm_ontology.canonical_relations import CANONICAL_RELATION_TYPES


def test_predicate_refs_are_unique() -> None:
    refs = [item.predicate_ref for item in CANONICAL_RELATION_TYPES]
    assert len(refs) == len(set(refs))


def test_registered_inverse_refs_are_reciprocal() -> None:
    by_predicate = {item.predicate_ref: item for item in CANONICAL_RELATION_TYPES}
    for item in CANONICAL_RELATION_TYPES:
        if item.inverse_ref in by_predicate:
            assert by_predicate[item.inverse_ref].inverse_ref == item.predicate_ref
