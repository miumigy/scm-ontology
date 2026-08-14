"""Contract for extending SCM Ontology Core with domain semantics."""
from __future__ import annotations

from dataclasses import dataclass


class DomainExtensionError(ValueError):
    """Raised when a domain extension violates the canonical boundary."""


@dataclass(frozen=True)
class DomainExtension:
    """A domain concept explicitly mapped to a Core semantic primitive."""

    name: str
    core_primitive: str
    definition: str

    def __post_init__(self) -> None:
        if not self.name:
            raise DomainExtensionError("name must be non-empty")
        if not self.core_primitive:
            raise DomainExtensionError("core_primitive must be non-empty")
        if not self.definition:
            raise DomainExtensionError("definition must be non-empty")


def validate_domain_extension(extension: DomainExtension) -> DomainExtension:
    """Validate that a domain extension is explicit and self-contained."""
    if not isinstance(extension, DomainExtension):
        raise DomainExtensionError("extension must be a DomainExtension")
    return extension
