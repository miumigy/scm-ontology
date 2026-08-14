import pytest

from scm_ontology.party_role import (
    CANONICAL_PARTY_ROLES,
    CanonicalPartyRole,
    PartyRoleContractError,
    is_party_role,
)


def test_creates_canonical_party_role():
    role = CanonicalPartyRole(
        party_id="PARTY-001",
        role="supplier",
        context="supply_chain",
    )
    assert role.role == "supplier"
    assert is_party_role(role)


def test_canonical_roles_are_scoped_vocabulary():
    assert CANONICAL_PARTY_ROLES == (
        "supplier",
        "customer",
        "manufacturer",
        "carrier",
        "logistics_provider",
    )


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"party_id": "", "role": "supplier"}, "party_id"),
        ({"party_id": "P", "role": ""}, "role"),
        ({"party_id": "P", "role": "supplier", "context": ""}, "context"),
    ],
)
def test_rejects_invalid_party_role(kwargs, message):
    with pytest.raises(PartyRoleContractError, match=message):
        CanonicalPartyRole(**kwargs)
