from scm_ontology.canonical_relations import CANONICAL_RELATION_TYPES, RelationKind


def test_canonical_relation_predicates_are_unique() -> None:
    predicates = [item.predicate_ref for item in CANONICAL_RELATION_TYPES]
    assert len(predicates) == len(set(predicates))


def test_canonical_relation_inverses_are_distinct() -> None:
    for relation in CANONICAL_RELATION_TYPES:
        assert relation.inverse_ref != relation.predicate_ref


def test_relation_taxonomy_covers_expected_semantic_layers() -> None:
    kinds = {item.kind for item in CANONICAL_RELATION_TYPES}
    assert {RelationKind.PHYSICAL, RelationKind.INFORMATIONAL, RelationKind.TEMPORAL,
            RelationKind.CAUSAL, RelationKind.OPERATIONAL, RelationKind.GOVERNANCE} <= kinds
