import pytest

from scm_ontology.relationships import (
    CORE_SCM_RELATIONSHIPS,
    CanonicalRelationship,
    RelationshipContractError,
    is_relationship,
)


def test_core_relationships_are_explicit():
    relations = {(r.source_type, r.predicate, r.target_type) for r in CORE_SCM_RELATIONSHIPS}
    assert relations == {
        ("Inventory", "for_item", "Item"),
        ("Inventory", "held_at", "Location"),
        ("Demand", "for_item", "Item"),
    }
    assert all(is_relationship(r) for r in CORE_SCM_RELATIONSHIPS)


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"source_type": "", "predicate": "for_item", "target_type": "Item"}, "source_type"),
        ({"source_type": "Inventory", "predicate": "", "target_type": "Item"}, "predicate"),
        ({"source_type": "Inventory", "predicate": "for_item", "target_type": ""}, "target_type"),
    ],
)
def test_rejects_invalid_relationship(kwargs, message):
    with pytest.raises(RelationshipContractError, match=message):
        CanonicalRelationship(**kwargs)
