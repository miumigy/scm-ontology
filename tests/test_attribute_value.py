import pytest

from scm_ontology.attribute_value import (
    AttributeDefinition,
    CanonicalValue,
    ValueKind,
    ValueStatus,
    make_attribute_value,
)


def test_quantity_requires_unit() -> None:
    with pytest.raises(ValueError, match="unit_ref"):
        CanonicalValue(kind=ValueKind.QUANTITY, value=10)


def test_reference_requires_type() -> None:
    with pytest.raises(ValueError, match="type_ref"):
        CanonicalValue(kind=ValueKind.REFERENCE, value="material:1")


def test_unknown_is_not_zero() -> None:
    value = CanonicalValue(kind=ValueKind.NUMBER, value=None, status=ValueStatus.UNKNOWN)
    assert value.value is None
    assert value.is_actual_observation is False


def test_attribute_value_requires_matching_kind() -> None:
    attribute = AttributeDefinition(
        name="quantity",
        value_kind=ValueKind.QUANTITY,
        description="Canonical quantity",
        unit_ref="unit:kg",
    )
    value = CanonicalValue(kind=ValueKind.QUANTITY, value=10, unit_ref="unit:kg")
    result = make_attribute_value("inventory:1", attribute, value)
    assert result.subject_ref == "inventory:1"


def test_attribute_value_rejects_wrong_unit() -> None:
    attribute = AttributeDefinition(
        name="quantity",
        value_kind=ValueKind.QUANTITY,
        description="Canonical quantity",
        unit_ref="unit:kg",
    )
    value = CanonicalValue(kind=ValueKind.QUANTITY, value=10, unit_ref="unit:piece")
    with pytest.raises(ValueError, match="unit"):
        make_attribute_value("inventory:1", attribute, value)


def test_inferred_value_is_not_actual() -> None:
    value = CanonicalValue(
        kind=ValueKind.NUMBER,
        value=42,
        status=ValueStatus.INFERRED,
    )
    assert value.is_inference is True
    assert value.is_actual_observation is False
