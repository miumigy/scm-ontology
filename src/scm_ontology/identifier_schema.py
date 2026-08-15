from __future__ import annotations

from dataclasses import dataclass

from .identity_reference import Identifier, ResolutionStatus


@dataclass(frozen=True)
class CanonicalIdentifierDefinition:
    """Schema-facing declaration of an identifier slot without making it identity."""

    ref: str
    namespace_ref: str
    value_type_ref: str
    role: str
    entity_type_ref: str | None = None

    def __post_init__(self) -> None:
        if not self.ref or not self.namespace_ref or not self.value_type_ref or not self.role:
            raise ValueError("ref, namespace_ref, value_type_ref, and role are required")


@dataclass(frozen=True)
class ReferenceResolution:
    """Explicit mapping assertion from a source identifier to a canonical reference."""

    ref: str
    source_identifier: Identifier
    target_entity_ref: str | None
    status: ResolutionStatus
    confidence: float | None = None
    provenance_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.ref:
            raise ValueError("ref is required")
        if self.status is ResolutionStatus.CONFIRMED and not self.target_entity_ref:
            raise ValueError("confirmed resolution requires target_entity_ref")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

    @property
    def is_canonical(self) -> bool:
        return self.status is ResolutionStatus.CONFIRMED and self.target_entity_ref is not None
