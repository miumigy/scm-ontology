import pytest

from scm_ontology.claim_object import ClaimObject


def test_claim_object_can_reference_a_canonical_or_external_entity():
    obj = ClaimObject.reference_object("SUP-001")
    assert obj.kind == "reference"
    assert obj.reference == "SUP-001"
    assert obj.value is None


def test_claim_object_can_hold_a_literal_value():
    obj = ClaimObject.value_object("delivered")
    assert obj.kind == "value"
    assert obj.value == "delivered"
    assert obj.reference is None


def test_claim_object_allows_numeric_literal_values():
    obj = ClaimObject.value_object(100)
    assert obj.value == 100


def test_claim_object_rejects_ambiguous_reference_and_value():
    with pytest.raises(ValueError, match="value must be None"):
        ClaimObject(kind="reference", reference="SUP-001", value="Supplier")


def test_claim_object_rejects_empty_reference():
    with pytest.raises(ValueError, match="reference must not be empty"):
        ClaimObject.reference_object("")


def test_claim_object_rejects_invalid_kind():
    with pytest.raises(ValueError, match="kind"):
        ClaimObject(kind="unknown")
