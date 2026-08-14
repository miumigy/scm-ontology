import pytest

from scm_ontology.s45_relationship_identity import RelationshipIdentityError, RelationshipInstance


def test_relationship_has_stable_identity_and_endpoints():
    relationship = RelationshipInstance("R1", "order-1", "supplied_by", "supplier-a")
    assert relationship.identity == "R1"
    assert relationship.endpoints() == ("order-1", "supplier-a")


@pytest.mark.parametrize("field", ["relationship_id", "from_id", "predicate", "to_id"])
def test_rejects_empty_identity_fields(field):
    values = dict(relationship_id="R1", from_id="order-1", predicate="supplied_by", to_id="supplier-a")
    values[field] = ""
    with pytest.raises(RelationshipIdentityError, match=field):
        RelationshipInstance(**values)
