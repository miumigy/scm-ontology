from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .assertion_context import AssertionContext


@dataclass(frozen=True)
class ValueAssertion:
    """A value attached to an entity attribute with explicit semantic context."""

    assertion_ref: str
    subject_ref: str
    attribute_ref: str
    value: Any
    context: AssertionContext

    def __post_init__(self) -> None:
        if not self.assertion_ref.strip() or not self.subject_ref.strip() or not self.attribute_ref.strip():
            raise ValueError("assertion_ref, subject_ref, and attribute_ref are required")
        if self.context.relation_id != self.assertion_ref:
            raise ValueError("context relation_id must match assertion_ref")
        if self.context.context.subject_ref != self.subject_ref:
            raise ValueError("context subject_ref must match value assertion subject_ref")
        if self.value is None:
            raise ValueError("null is represented by absence, not ValueAssertion")


@dataclass(frozen=True)
class ContextualValue:
    """Attribute value plus its assertion context, independent of storage."""

    assertion: ValueAssertion

    @property
    def epistemic_kind(self):
        return self.assertion.context.context.epistemic_kind

    @property
    def has_provenance(self) -> bool:
        return self.assertion.context.context.has_provenance
