from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .core_instance import CanonicalRelation


@dataclass(frozen=True)
class RelationGraphEdge:
    relation_id: str
    subject_id: str
    predicate_ref: str
    object_id: str
    qualifiers: Mapping[str, Any]


def project_relation_instance_to_graph(relation: CanonicalRelation) -> RelationGraphEdge:
    """Project one canonical relation instance into an immutable graph-edge descriptor."""
    return RelationGraphEdge(
        relation_id=relation.relation_id,
        subject_id=relation.subject_id,
        predicate_ref=relation.predicate_ref,
        object_id=relation.object_id,
        qualifiers=dict(relation.qualifiers),
    )
