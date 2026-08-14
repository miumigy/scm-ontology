import pytest

from scm_ontology.party_transaction import (
    CANONICAL_PARTY_TRANSACTION_RELATIONSHIPS,
    PartyTransactionRelationship,
    PartyTransactionRelationshipError,
    is_party_transaction_relationship,
)


def test_canonical_party_transaction_relationships_are_explicit():
    relationships = {
        (r.party_role, r.predicate, r.transaction_type)
        for r in CANONICAL_PARTY_TRANSACTION_RELATIONSHIPS
    }
    assert relationships == {
        ("customer", "places", "CustomerOrder"),
        ("supplier", "receives", "PurchaseOrder"),
        ("manufacturer", "creates", "ProductionOrder"),
        ("carrier", "executes", "Shipment"),
    }
    assert all(is_party_transaction_relationship(r) for r in CANONICAL_PARTY_TRANSACTION_RELATIONSHIPS)


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"party_role": "", "predicate": "places", "transaction_type": "CustomerOrder"}, "party_role"),
        ({"party_role": "customer", "predicate": "", "transaction_type": "CustomerOrder"}, "predicate"),
        ({"party_role": "customer", "predicate": "places", "transaction_type": ""}, "transaction_type"),
    ],
)
def test_rejects_invalid_relationship(kwargs, message):
    with pytest.raises(PartyTransactionRelationshipError, match=message):
        PartyTransactionRelationship(**kwargs)
