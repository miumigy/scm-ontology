"""Canonical identifier and reference semantics for S115.

Identifiers are contextual reference tokens, not identities. The model keeps
namespace, issuer, validity, resolution status, and epistemic/provenance hooks
explicit while remaining independent of storage and matching algorithms.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ResolutionStatus(StrEnum):
    CONFIRMED = "confirmed"
    PROBABLE = "probable"
    POSSIBLE = "possible"
    UNRESOLVED = "unresolved"
    CONTRADICTED = "contradicted"


@dataclass(frozen=True)
class IdentifierNamespace:
    name: str
    issuer: str | None = None
    description: str = ""


@dataclass(frozen=True)
class Identifier:
    value: str
    namespace: IdentifierNamespace
    issuer: str | None = None

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("identifier value must not be empty")


@dataclass(frozen=True)
class IdentifierAssignment:
    identifier: Identifier
    entity_ref: str
    valid_from: str | None = None
    valid_to: str | None = None
    source_ref: str | None = None

    def __post_init__(self) -> None:
        if not self.entity_ref:
            raise ValueError("identifier assignment requires an entity reference")
        if self.valid_from and self.valid_to and self.valid_from > self.valid_to:
            raise ValueError("identifier validity interval is reversed")


@dataclass(frozen=True)
class Alias:
    value: str
    entity_ref: str
    namespace: IdentifierNamespace | None = None
    valid_from: str | None = None
    valid_to: str | None = None


@dataclass(frozen=True)
class CanonicalReference:
    target_ref: str
    source_identifier: Identifier | None = None
    resolution_status: ResolutionStatus = ResolutionStatus.CONFIRMED
    confidence: float | None = None
    provenance_ref: str | None = None

    def __post_init__(self) -> None:
        if not self.target_ref:
            raise ValueError("reference requires a target reference")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if self.resolution_status == ResolutionStatus.UNRESOLVED and self.target_ref:
            # An unresolved reference may point to a candidate target, but the
            # target must never be interpreted as confirmed identity.
            return


@dataclass(frozen=True)
class IdentityResolutionAssertion:
    left_ref: Identifier
    right_ref: Identifier | str
    status: ResolutionStatus
    method: str | None = None
    confidence: float | None = None
    valid_from: str | None = None
    valid_to: str | None = None
    provenance_ref: str | None = None

    def __post_init__(self) -> None:
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if self.valid_from and self.valid_to and self.valid_from > self.valid_to:
            raise ValueError("resolution validity interval is reversed")


def identifier_key(identifier: Identifier) -> tuple[str, str, str | None]:
    """Return the contextual key used to interpret an identifier."""
    return (identifier.namespace.name, identifier.value, identifier.issuer)
