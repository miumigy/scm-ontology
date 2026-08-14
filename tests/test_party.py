import pytest

from scm_ontology.party import CanonicalParty, PartyConceptError, is_party


def test_creates_canonical_party():
    party = CanonicalParty(party_id="PARTY-001", name="Example Supplier", party_type="supplier")
    assert party.name == "Example Supplier"
    assert is_party(party)


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"party_id": "", "name": "Example"}, "party_id"),
        ({"party_id": "P", "name": ""}, "name"),
        ({"party_id": "P", "name": "Example", "party_type": ""}, "party_type"),
    ],
)
def test_rejects_invalid_party(kwargs, message):
    with pytest.raises(PartyConceptError, match=message):
        CanonicalParty(**kwargs)
