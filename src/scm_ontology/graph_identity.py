from __future__ import annotations

from dataclasses import dataclass

from .core_instance import CanonicalEntity


class GraphIdentityError(ValueError):
    pass


@dataclass(frozen=True)
class GraphNodeIdentity:
    node_id: str
    node_type: str


def graph_node_identity(entity: CanonicalEntity) -> GraphNodeIdentity:
    """Derive deterministic graph identity from canonical entity identity."""
    if not entity.entity_id.strip() or not entity.concept_ref.strip():
        raise GraphIdentityError("canonical entity identity must be non-empty")
    return GraphNodeIdentity(node_id=entity.entity_id, node_type=entity.concept_ref)
