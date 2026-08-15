from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Mapping

from .assertion_model import CanonicalAssertionSet, EntityAssertion, RelationAssertion


class SerializationError(ValueError):
    """Raised when a canonical model cannot be serialized safely."""


def _context_dict(assertion: EntityAssertion | RelationAssertion) -> dict[str, Any]:
    context = assertion.context
    semantic = context.context
    return {
        "assertion_ref": context.relation_id,
        "semantic_context": asdict(semantic),
        "qualifiers": dict(context.qualifiers),
    }


def serialize_assertion_set(model: CanonicalAssertionSet) -> dict[str, Any]:
    """Serialize the canonical assertion model to a JSON-compatible mapping.

    This is deliberately a format-neutral mapping boundary: it does not choose
    JSON Schema, RDF, graph database properties, or storage-specific types.
    """
    if not isinstance(model, CanonicalAssertionSet):
        raise SerializationError("model must be a CanonicalAssertionSet")

    entity_assertions = []
    for assertion in model.entity_assertions:
        entity_assertions.append(
            {
                "assertion_ref": assertion.assertion_ref,
                "subject_ref": assertion.subject_ref,
                "attribute_ref": assertion.attribute_ref,
                "value": assertion.value,
                "context": _context_dict(assertion),
            }
        )

    relation_assertions = []
    for assertion in model.relation_assertions:
        relation = assertion.relation
        relation_assertions.append(
            {
                "assertion_ref": relation.relation_id,
                "subject_ref": relation.subject_id,
                "predicate_ref": relation.predicate_ref,
                "object_ref": relation.object_id,
                "qualifiers": dict(relation.qualifiers),
                "context": _context_dict(assertion),
            }
        )

    return {
        "entity_assertions": entity_assertions,
        "relation_assertions": relation_assertions,
        "metadata": dict(model.metadata),
    }


def is_json_compatible(value: Any) -> bool:
    """Return whether a value consists only of JSON-compatible primitives."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return True
    if isinstance(value, list):
        return all(is_json_compatible(item) for item in value)
    if isinstance(value, Mapping):
        return all(isinstance(k, str) and is_json_compatible(v) for k, v in value.items())
    return False
