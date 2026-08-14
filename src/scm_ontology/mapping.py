from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class MappingStatus(str, Enum):
    PROPOSED = "proposed"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    DEPRECATED = "deprecated"
    REJECTED = "rejected"


class TransformationKind(str, Enum):
    RENAME = "rename"
    TYPE_CONVERSION = "type_conversion"
    UNIT_CONVERSION = "unit_conversion"
    CODE_TRANSLATION = "code_translation"
    NORMALIZATION = "normalization"
    COMPOSITION = "composition"
    DECOMPOSITION = "decomposition"
    AGGREGATION = "aggregation"
    DERIVATION = "derivation"
    IDENTITY_RESOLUTION = "identity_resolution"


@dataclass(frozen=True)
class SourceField:
    system: str
    concept: str
    field: str
    namespace: Optional[str] = None


@dataclass(frozen=True)
class CanonicalTarget:
    concept: str
    attribute: Optional[str] = None


@dataclass(frozen=True)
class Transformation:
    kind: TransformationKind
    expression: Optional[str] = None


@dataclass(frozen=True)
class SemanticMapping:
    source: SourceField
    target: CanonicalTarget
    transformations: tuple[Transformation, ...] = field(default_factory=tuple)
    status: MappingStatus = MappingStatus.PROPOSED
    confidence: Optional[float] = None
    provenance_ref: Optional[str] = None
    identity_resolution_ref: Optional[str] = None
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None

    def __post_init__(self) -> None:
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if not self.source.system or not self.source.concept or not self.source.field:
            raise ValueError("source system, concept, and field are required")
        if not self.target.concept:
            raise ValueError("target concept is required")

    @property
    def is_approved(self) -> bool:
        return self.status is MappingStatus.APPROVED
