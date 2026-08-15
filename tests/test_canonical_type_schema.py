import pytest

from scm_ontology.canonical_type_schema import (
    CanonicalAttributeDefinition,
    CanonicalTypeDefinition,
    Nullability,
)
from scm_ontology.type_semantics import Cardinality, ValueKind


def test_quantity_type_requires_unit() -> None:
    with pytest.raises(ValueError, match="unit_ref"):
        CanonicalTypeDefinition("type:q", "Quantity", ValueKind.QUANTITY)


def test_reference_type_requires_target() -> None:
    with pytest.raises(ValueError, match="reference_target"):
        CanonicalTypeDefinition("type:r", "Reference", ValueKind.REFERENCE)


def test_attribute_requires_owner_and_type() -> None:
    with pytest.raises(ValueError, match="required"):
        CanonicalAttributeDefinition("a:1", "", "status", "type:code")


def test_mandatory_attribute_cannot_be_nullable() -> None:
    with pytest.raises(ValueError, match="nullable"):
        CanonicalAttributeDefinition(
            "a:1", "Shipment", "status", "type:code",
            cardinality=Cardinality.ONE,
            nullability=Nullability.NULLABLE,
        )


def test_optional_attribute_can_be_non_null_when_present() -> None:
    attribute = CanonicalAttributeDefinition(
        "a:1", "Shipment", "status", "type:code",
        cardinality=Cardinality.ZERO_OR_ONE,
        nullability=Nullability.NON_NULL,
    )
    assert attribute.type_ref == "type:code"
