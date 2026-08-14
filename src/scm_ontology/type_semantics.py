"""Canonical type, attribute, and value semantics for S114.

S114 defines the semantic contract for describing what kind of value a
canonical concept carries. It intentionally does not prescribe a storage or
serialization format; later schema work will do that.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ValueKind(StrEnum):
    SCALAR = "scalar"
    QUANTITY = "quantity"
    CODE = "code"
    REFERENCE = "reference"
    ENUMERATION = "enumeration"
    INTERVAL = "interval"
    RANGE = "range"
    COLLECTION = "collection"
    STRUCTURED = "structured"


class ScalarType(StrEnum):
    STRING = "string"
    BOOLEAN = "boolean"
    INTEGER = "integer"
    DECIMAL = "decimal"
    DATE = "date"
    DATETIME = "datetime"
    DURATION = "duration"


class AttributeRole(StrEnum):
    IDENTITY = "identity"
    DESCRIPTIVE = "descriptive"
    QUALIFIER = "qualifier"
    MEASURE = "measure"
    TEMPORAL = "temporal"
    EPISTEMIC = "epistemic"
    PROVENANCE = "provenance"
    DERIVATION = "derivation"
    GOVERNANCE = "governance"
    REFERENCE = "reference"


class Cardinality(StrEnum):
    ONE = "1"
    ZERO_OR_ONE = "0..1"
    ZERO_OR_MANY = "0..*"
    ONE_OR_MANY = "1..*"


@dataclass(frozen=True)
class ValueType:
    name: str
    kind: ValueKind
    scalar: ScalarType | None = None
    reference_target: str | None = None
    unit_required: bool = False

    def __post_init__(self) -> None:
        if self.kind == ValueKind.SCALAR and self.scalar is None:
            raise ValueError("scalar values require scalar type")
        if self.kind == ValueKind.QUANTITY and not self.unit_required:
            raise ValueError("quantity values require unit semantics")
        if self.kind == ValueKind.REFERENCE and not self.reference_target:
            raise ValueError("reference values require a target concept")
        if self.kind != ValueKind.SCALAR and self.scalar is not None:
            raise ValueError("scalar type is only valid for scalar values")


@dataclass(frozen=True)
class AttributeDefinition:
    name: str
    owner: str
    value_type: ValueType
    role: AttributeRole
    cardinality: Cardinality = Cardinality.ZERO_OR_ONE
    description: str = ""


VALUE_TYPES: tuple[ValueType, ...] = (
    ValueType("String", ValueKind.SCALAR, scalar=ScalarType.STRING),
    ValueType("Boolean", ValueKind.SCALAR, scalar=ScalarType.BOOLEAN),
    ValueType("Integer", ValueKind.SCALAR, scalar=ScalarType.INTEGER),
    ValueType("Decimal", ValueKind.SCALAR, scalar=ScalarType.DECIMAL),
    ValueType("Date", ValueKind.SCALAR, scalar=ScalarType.DATE),
    ValueType("DateTime", ValueKind.SCALAR, scalar=ScalarType.DATETIME),
    ValueType("Duration", ValueKind.SCALAR, scalar=ScalarType.DURATION),
    ValueType("Quantity", ValueKind.QUANTITY, unit_required=True),
    ValueType("Code", ValueKind.CODE),
    ValueType("Reference", ValueKind.REFERENCE, reference_target="Entity"),
    ValueType("Enumeration", ValueKind.ENUMERATION),
    ValueType("Interval", ValueKind.INTERVAL),
    ValueType("Range", ValueKind.RANGE),
    ValueType("Collection", ValueKind.COLLECTION),
    ValueType("Structured", ValueKind.STRUCTURED),
)


def value_type_names() -> frozenset[str]:
    return frozenset(value_type.name for value_type in VALUE_TYPES)


def get_value_type(name: str) -> ValueType:
    for value_type in VALUE_TYPES:
        if value_type.name == name:
            return value_type
    raise KeyError(f"unknown canonical value type: {name}")
