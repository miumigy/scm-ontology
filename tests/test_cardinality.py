import pytest

from scm_ontology.cardinality import (
    ONE,
    ONE_OR_MANY,
    ZERO_OR_MANY,
    ZERO_OR_ONE,
    Cardinality,
    CardinalityError,
)
from scm_ontology.relationship_cardinality import (
    CANONICAL_RELATIONSHIP_CARDINALITIES,
    get_relationship_cardinality,
)


def test_standard_cardinalities():
    assert str(ONE) == "1"
    assert str(ZERO_OR_ONE) == "0..1"
    assert str(ZERO_OR_MANY) == "0..*"
    assert str(ONE_OR_MANY) == "1..*"


def test_cardinality_allows_expected_counts():
    assert ONE.allows(1)
    assert not ONE.allows(0)
    assert not ONE.allows(2)
    assert ZERO_OR_ONE.allows(0)
    assert ZERO_OR_ONE.allows(1)
    assert not ZERO_OR_ONE.allows(2)
    assert ZERO_OR_MANY.allows(100)


def test_selected_relationship_cardinalities_are_explicit():
    places = get_relationship_cardinality("places")
    assert places is not None
    assert str(places.from_cardinality) == "0..*"
    assert str(places.to_cardinality) == "1"
    assert len(CANONICAL_RELATIONSHIP_CARDINALITIES) == 7


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"minimum": -1, "maximum": None}, "minimum"),
        ({"minimum": 2, "maximum": 1}, "maximum"),
    ],
)
def test_rejects_invalid_cardinality(kwargs, message):
    with pytest.raises(CardinalityError, match=message):
        Cardinality(**kwargs)
