from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .canonical_model import get_concept, relationship_predicates
from .core_instance import CoreInstanceModel


@dataclass(frozen=True)
class InstanceIssue:
    code: str
    subject: str
    message: str


def validate_core_instances(
    model: CoreInstanceModel,
    *,
    concept_types: Mapping[str, str] | None = None,
) -> tuple[InstanceIssue, ...]:
    """Validate instance references against the canonical semantic registry.

    `concept_types` is an optional override for ingestion adapters. When absent,
    the entity's own canonical `concept_ref` is authoritative.
    """
    issues: list[InstanceIssue] = []
    concept_types = concept_types or {
        entity.entity_id: entity.concept_ref for entity in model.entities
    }

    for entity in model.entities:
        concept_ref = concept_types.get(entity.entity_id, "")
        if not concept_ref:
            issues.append(InstanceIssue("CON001", entity.entity_id, "canonical concept reference is required"))
            continue
        try:
            get_concept(concept_ref)
        except KeyError:
            issues.append(InstanceIssue("CON002", entity.entity_id, "unknown canonical concept"))

    predicates = relationship_predicates()
    for relation in model.relations:
        if relation.predicate_ref not in predicates:
            issues.append(InstanceIssue("REL001", relation.relation_id, "unknown canonical relationship predicate"))

    return tuple(issues)


def assert_core_instances_valid(
    model: CoreInstanceModel,
    *,
    concept_types: Mapping[str, str] | None = None,
) -> None:
    issues = validate_core_instances(model, concept_types=concept_types)
    if issues:
        details = "; ".join(f"{i.code}: {i.subject} — {i.message}" for i in issues)
        raise ValueError(f"invalid canonical instances: {details}")
