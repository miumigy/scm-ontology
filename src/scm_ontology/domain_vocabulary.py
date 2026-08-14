"""Contract for controlled SCM domain vocabulary extensions."""
from __future__ import annotations

from dataclasses import dataclass


class DomainVocabularyError(ValueError):
    """Raised when a domain vocabulary entry violates its contract."""


@dataclass(frozen=True)
class DomainVocabularyEntry:
    """A canonical SCM term with explicit semantic boundaries."""

    name: str
    definition: str
    core_primitive: str
    synonyms: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise DomainVocabularyError("name must be non-empty")
        if not self.definition.strip():
            raise DomainVocabularyError("definition must be non-empty")
        if not self.core_primitive.strip():
            raise DomainVocabularyError("core_primitive must be non-empty")
        if any(not synonym.strip() for synonym in self.synonyms):
            raise DomainVocabularyError("synonyms must be non-empty strings")


def is_domain_vocabulary_entry(value: object) -> bool:
    return isinstance(value, DomainVocabularyEntry)
