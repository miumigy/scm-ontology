"""Deterministic temporal reads over a CanonicalGraph."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .canonical_graph import CanonicalGraph, CanonicalRelationship


@dataclass(frozen=True)
class TemporalRelationshipMatch:
    relationship: CanonicalRelationship
    version_index: int
    valid_from: str
    valid_to: str | None
    qualifiers: dict[str, Any]


def _parse(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _contains(version: Any, at: datetime) -> bool:
    start = _parse(version.valid_from)
    end = _parse(version.valid_to) if version.valid_to else None
    return start <= at and (end is None or at < end)


def relationships_at(graph: CanonicalGraph, at: str, *, predicate: str | None = None, from_id: str | None = None, to_id: str | None = None) -> tuple[TemporalRelationshipMatch, ...]:
    """Return relationship versions valid at an instant without mutation."""
    instant = _parse(at)
    matches: list[TemporalRelationshipMatch] = []
    for relationship in graph.relationships:
        instance = relationship.instance
        if predicate is not None and instance.predicate != predicate:
            continue
        if from_id is not None and instance.from_id != from_id:
            continue
        if to_id is not None and instance.to_id != to_id:
            continue
        for index, version in enumerate(relationship.versions):
            if _contains(version, instant):
                matches.append(TemporalRelationshipMatch(relationship, index, version.valid_from, version.valid_to, dict(version.qualifiers or {})))
    return tuple(matches)
