import pytest

from scm_ontology.type_semantics import (
    AttributeDefinition,
    AttributeRole,
    Cardinality,
    ScalarType,
    ValueKind,
    ValueType,
    VALUE_TYPES,
    get_value_type,
)


def test_scalar_types_require_scalar_datatype():
    assert get_value_type("Decimal").scalar == ScalarType.DECIMAL
    with pytest.raises(ValueError):
        ValueType("Broken", ValueKind.SCALAR)


def test_quantity_requires_unit_semantics():
    assert get_value_type("Quantity").unit_required is True
    with pytest.raises(ValueError):
        ValueType("Broken", ValueKind.QUANTITY)


def test_reference_requires_target():
    reference = get_value_type("Reference")
    assert reference.reference_target == "Entity"
    with pytest.raises(ValueError):
        ValueType("Broken", ValueKind.REFERENCE)


def test_non_scalar_cannot_carry_scalar_datatype():
    with pytest.raises(ValueError):
        ValueType("Broken", ValueKind.CODE, scalar=ScalarType.STRING)


def test_attribute_is_typed_and_role_qualified():
    attribute = AttributeDefinition(
        name="quantity",
        owner="Inventory",
        value_type=get_value_type("Quantity"),
        role=AttributeRole.MEASURE,
        cardinality=Cardinality.ONE,
    )
    assert attribute.owner == "Inventory"
    assert attribute.value_type.kind == ValueKind.QUANTITY
    assert attribute.role == AttributeRole.MEASURE


def test_canonical_value_type_names_are_unique():
    names = [value_type.name for value_type in VALUE_TYPES]
    assert len(names) == len(set(names))
