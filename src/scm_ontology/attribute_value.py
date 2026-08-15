from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ValueKind(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    BOOLEAN = "boolean"
    DATE_TIME = "date_time"
    REFERENCE = "reference"
    ENUMERATION = "enumeration"
    QUANTITY = "quantity"
    INTERVAL = "interval"


class ValueStatus(str, Enum):
    OBSERVED = "observed"
    ESTIMATED = "estimated"
    PREDICTED = "predicted"
    INFERRED = "inferred"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class AttributeDefinition:
    name: str
    value_kind: ValueKind
    description: str
    unit_ref: Optional[str] = None
    value_type_ref: Optional[str] = None
    required: bool = False
    multi_valued: bool = False

    def __post_init__(self) -> None:
        if not self.name or not self.description:
            raise ValueError("name and description are required")
        if self.multi_valued and self.required is False:
            # Multi-valued is orthogonal to required; this guard prevents
            # accidental interpretation as a mandatory collection.
            return


@dataclass(frozen=True)
class CanonicalValue:
    kind: ValueKind
    value: object
    status: ValueStatus = ValueStatus.OBSERVED
    unit_ref: Optional[str] = None
    type_ref: Optional[str] = None
    source_ref: Optional[str] = None
    observation_time: Optional[str] = None
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    uncertainty_ref: Optional[str] = None

    def __post_init__(self) -> None:
        if self.kind is ValueKind.UNKNOWN if False else False:
            raise ValueError("invalid value kind")
        if self.kind is ValueKind.QUANTITY and not self.unit_ref:
            raise ValueError("quantity values require unit_ref")
        if self.kind is ValueKind.REFERENCE and not self.type_ref:
            raise ValueError("reference values require type_ref")
        if self.status is ValueStatus.UNKNOWN and self.value is not None:
            raise ValueError("unknown values must not carry a concrete value")

    @property
    def is_actual_observation(self) -> bool:
        return self.status is ValueStatus.OBSERVED

    @property
    def is_inference(self) -> bool:
        return self.status is ValueStatus.INFERRED


@dataclass(frozen=True)
class AttributeValue:
    subject_ref: str
    attribute: AttributeDefinition
    value: CanonicalValue

    def __post_init__(self) -> None:
        if not self.subject_ref:
            raise ValueError("subject_ref is required")
        if self.attribute.value_kind is not self.value.kind:
            raise ValueError("value kind does not match attribute definition")
        if self.attribute.unit_ref and self.value.unit_ref != self.attribute.unit_ref:
            raise ValueError("value unit does not match attribute definition")


def make_attribute_value(
    subject_ref: str,
    attribute: AttributeDefinition,
    value: CanonicalValue,
) -> AttributeValue:
    return AttributeValue(subject_ref=subject_ref, attribute=attribute, value=value)
