from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from .core_instance import CanonicalRelation
from .semantic_context import SemanticContext


@dataclass(frozen=True)
class AssertionContext:
    """Context attached to a canonical relation assertion.

    The relation remains the structural statement; this object carries the
    temporal, epistemic, provenance, and optional scenario context around it.
    """

    relation_id: str
    context: SemanticContext
    qualifiers: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.relation_id.strip():
            raise ValueError("relation_id is required")
        if self.context.assertion_ref != self.relation_id:
            raise ValueError("context assertion_ref must match relation_id")
        if not isinstance(self.qualifiers, Mapping):
            raise ValueError("qualifiers must be a mapping")


@dataclass(frozen=True)
class ContextualRelation:
    """A canonical relation paired with its semantic assertion context."""

    relation: CanonicalRelation
    assertion_context: AssertionContext

    def __post_init__(self) -> None:
        if self.relation.relation_id != self.assertion_context.relation_id:
            raise ValueError("relation and assertion context ids must match")
