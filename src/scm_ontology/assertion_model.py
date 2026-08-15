from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .assertion_context import AssertionContext
from .core_instance import CanonicalRelation


class AssertionModelError(ValueError):
    """Raised when a canonical assertion violates core invariants."""


@dataclass(frozen=True)
class EntityAssertion:
    """A contextual assertion about an entity attribute."""

    assertion_ref: str
    subject_ref: str
    attribute_ref: str
    value: Any
    context: AssertionContext

    def __post_init__(self) -> None:
        if not self.assertion_ref.strip() or not self.subject_ref.strip() or not self.attribute_ref.strip():
            raise AssertionModelError("assertion_ref, subject_ref, and attribute_ref are required")
        if self.context.relation_id != self.assertion_ref:
            raise AssertionModelError("context assertion ref must match assertion_ref")
        if self.context.context.subject_ref != self.subject_ref:
            raise AssertionModelError("context subject ref must match subject_ref")
        if self.value is None:
            raise AssertionModelError("null is not a canonical assertion value")


@dataclass(frozen=True)
class RelationAssertion:
    """A contextual assertion about a canonical relation."""

    relation: CanonicalRelation
    context: AssertionContext

    def __post_init__(self) -> None:
        if self.relation.relation_id != self.context.relation_id:
            raise AssertionModelError("context assertion ref must match relation_id")


@dataclass(frozen=True)
class CanonicalAssertionSet:
    """Transport-neutral collection of entity-value and relation assertions."""

    entity_assertions: tuple[EntityAssertion, ...] = ()
    relation_assertions: tuple[RelationAssertion, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        assertion_ids = [a.assertion_ref for a in self.entity_assertions]
        assertion_ids.extend(a.context.relation_id for a in self.relation_assertions)
        if len(assertion_ids) != len(set(assertion_ids)):
            raise AssertionModelError("assertion references must be unique within a set")
        if not isinstance(self.metadata, Mapping):
            raise AssertionModelError("metadata must be a mapping")
