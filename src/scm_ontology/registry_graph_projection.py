from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable

from .canonical_relations import CanonicalRelationType


@dataclass(frozen=True)
class RegistryGraphEdge:
    predicate_ref: str
    subject_type_ref: str
    object_type_ref: str


def project_relation_registry_to_graph(
    relations: Iterable[CanonicalRelationType],
) -> tuple[RegistryGraphEdge, ...]:
    """Project relation declarations into immutable graph-edge descriptors."""
    return tuple(
        RegistryGraphEdge(
            predicate_ref=item.predicate_ref,
            subject_type_ref=item.subject_type_ref,
            object_type_ref=item.object_type_ref,
        )
        for item in relations
    )
