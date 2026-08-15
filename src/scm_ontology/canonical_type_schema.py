from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Optional

from .type_semantics import AttributeDefinition, Cardinality, ValueKind


class Nullability(StrEnum):
    NON_NULL = "non_null"
    NULLABLE = "nullable"


@dataclass(frozen=True)
class CanonicalTypeDefinition:
    ref: str
    name: str
    value_kind: ValueKind
    scalar_type: Optional[str] = None
    unit_ref: Optional[str] = None
    reference_target: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.ref or not self.name:
            raise ValueError("ref and name are required")
        if self.value_kind is ValueKind.QUANTITY and not self.unit_ref:
            raise ValueError("quantity types require unit_ref")
        if self.value_kind is ValueKind.REFERENCE and not self.reference_target:
            raise ValueError("reference types require reference_target")
        if self.value_kind is not ValueKind.QUANTITY and self.unit_ref:
            raise ValueError("unit_ref is only valid for quantity types")


@dataclass(frozen=True)
class CanonicalAttributeDefinition:
    ref: str
    owner_ref: str
    name: str
    type_ref: str
    cardinality: Cardinality = Cardinality.ZERO_OR_ONE
    nullability: Nullability = Nullability.NON_NULL

    def __post_init__(self) -> None:
        if not all((self.ref, self.owner_ref, self.name, self.type_ref)):
            raise ValueError("ref, owner_ref, name, and type_ref are required")
        if self.cardinality is Cardinality.ONE and self.nullability is Nullability.NULLABLE:
            raise ValueError("mandatory cardinality cannot be nullable")


def attribute_definition_to_contract(attribute: AttributeDefinition) -> CanonicalAttributeDefinition:
    """Lift the S114 semantic contract into the canonical schema layer."""
    return CanonicalAttributeDefinition(
        ref=f"attribute:{attribute.owner}:{attribute.name}",
        owner_ref=attribute.owner,
        name=attribute.name,
        type_ref=f"type:{attribute.value_type.name}",
        cardinality=attribute.cardinality,
    )
