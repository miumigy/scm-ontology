from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from .canonical_relations import CanonicalRelationType, RelationKind


@dataclass(frozen=True)
class RegistryGraphEdge:
    predicate_ref: str
    kind: RelationKind
    inverse_ref: str | None


def project_relation_registry_to_graph(
    relations: Iterable[CanonicalRelationType],
) -> tuple[RegistryGraphEdge, ...]:
    """Project declared relation semantics into immutable graph-edge descriptors."""
    return tuple(
        RegistryGraphEdge(
            predicate_ref=item.predicate_ref,
            kind=item.kind,
            inverse_ref=item.inverse_ref,
        )
        for item in relations
    )
