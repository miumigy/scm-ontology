import pytest

from scm_ontology.relationship_vocabulary import (
    CANONICAL_PREDICATES,
    CanonicalPredicate,
    RelationshipVocabularyError,
    is_canonical_predicate,
)


def test_canonical_predicate_categories_are_explicit():
    predicates = {(p.name, p.category) for p in CANONICAL_PREDICATES}
    assert predicates == {
        ("contains", "structural"),
        ("located_at", "structural"),
        ("part_of", "structural"),
        ("plays_role", "participation"),
        ("places", "participation"),
        ("receives", "participation"),
        ("executes", "participation"),
        ("establishes", "lifecycle"),
        ("changes", "lifecycle"),
        ("moves_to", "flow"),
        ("supplies", "flow"),
        ("consumes", "flow"),
    }
    assert all(is_canonical_predicate(p) for p in CANONICAL_PREDICATES)


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"name": "", "category": "structural"}, "name"),
        ({"name": "contains", "category": ""}, "category"),
    ],
)
def test_rejects_invalid_predicate(kwargs, message):
    with pytest.raises(RelationshipVocabularyError, match=message):
        CanonicalPredicate(**kwargs)
