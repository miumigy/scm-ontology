"""Composable semantic contract for canonical relationships."""
from __future__ import annotations

from dataclasses import dataclass

from .relationship_qualifiers import RelationshipQualifier


@dataclass(frozen=True)
class RelationshipContract:
    """Predicate plus optional qualifiers; endpoints remain separate constraints."""

    predicate: str
    qualifiers: tuple[RelationshipQualifier, ...] = ()

    def has_qualifier(self, name: str) -> bool:
        return any(item.name == name for item in self.qualifiers)
