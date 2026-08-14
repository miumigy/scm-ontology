import pytest

from scm_ontology.relationship_contract import RelationshipContract
from scm_ontology.relationship_qualifiers import (
    CANONICAL_RELATIONSHIP_QUALIFIERS,
    RelationshipQualifier,
    RelationshipQualifierError,
    is_relationship_qualifier,
)


def test_canonical_qualifiers_are_typed():
    qualifiers = {item.name: item.value_type for item in CANONICAL_RELATIONSHIP_QUALIFIERS}
    assert qualifiers == {
        "valid_from": "time_reference",
        "valid_to": "time_reference",
        "sequence": "integer",
        "priority": "integer",
        "allocation_ratio": "decimal",
    }
    assert all(is_relationship_qualifier(item) for item in CANONICAL_RELATIONSHIP_QUALIFIERS)


def test_relationship_contract_can_attach_qualifiers():
    contract = RelationshipContract(
        predicate="supplies",
        qualifiers=(CANONICAL_RELATIONSHIP_QUALIFIERS[0], CANONICAL_RELATIONSHIP_QUALIFIERS[3]),
    )
    assert contract.has_qualifier("valid_from")
    assert contract.has_qualifier("priority")
    assert not contract.has_qualifier("sequence")


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"name": "", "value_type": "integer"}, "name"),
        ({"name": "priority", "value_type": ""}, "value_type"),
    ],
)
def test_rejects_invalid_qualifier(kwargs, message):
    with pytest.raises(RelationshipQualifierError, match=message):
        RelationshipQualifier(**kwargs)
