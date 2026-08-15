from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


class CoreInstanceError(ValueError):
    """Raised when a canonical instance violates core identity invariants."""


@dataclass(frozen=True)
class CanonicalEntity:
    """An instance of a canonical concept, identified independently of source data."""

    entity_id: str
    concept_ref: str
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.entity_id.strip():
            raise CoreInstanceError("entity_id must be non-empty")
        if not self.concept_ref.strip():
            raise CoreInstanceError("concept_ref must be non-empty")
        if not isinstance(self.attributes, Mapping):
            raise CoreInstanceError("attributes must be a mapping")


@dataclass(frozen=True)
class CanonicalRelation:
    """An assertion connecting two canonical entities by a canonical predicate."""

    relation_id: str
    subject_id: str
    predicate_ref: str
    object_id: str
    qualifiers: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.relation_id.strip():
            raise CoreInstanceError("relation_id must be non-empty")
        if not self.subject_id.strip() or not self.object_id.strip():
            raise CoreInstanceError("subject_id and object_id must be non-empty")
        if not self.predicate_ref.strip():
            raise CoreInstanceError("predicate_ref must be non-empty")
        if not isinstance(self.qualifiers, Mapping):
            raise CoreInstanceError("qualifiers must be a mapping")


@dataclass(frozen=True)
class CoreInstanceModel:
    """Minimal transport-neutral instance layer: entities and relations only."""

    entities: tuple[CanonicalEntity, ...] = ()
    relations: tuple[CanonicalRelation, ...] = ()

    def __post_init__(self) -> None:
        entity_ids = [entity.entity_id for entity in self.entities]
        relation_ids = [relation.relation_id for relation in self.relations]
        if len(entity_ids) != len(set(entity_ids)):
            raise CoreInstanceError("entity_id must be unique within a model")
        if len(relation_ids) != len(set(relation_ids)):
            raise CoreInstanceError("relation_id must be unique within a model")

        known_ids = set(entity_ids)
        for relation in self.relations:
            if relation.subject_id not in known_ids:
                raise CoreInstanceError("relation subject must resolve to an entity")
            if relation.object_id not in known_ids:
                raise CoreInstanceError("relation object must resolve to an entity")
