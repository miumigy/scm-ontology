from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable, Mapping


@dataclass(frozen=True)
class CanonicalEntityGraphNode:
    entity_type_ref: str
    identity_ref: str
    properties: tuple[tuple[str, object], ...] = ()


def project_canonical_entities(
    entities: Iterable[Mapping[str, object]],
) -> tuple[CanonicalEntityGraphNode, ...]:
    """Project canonical entity records into immutable graph-node descriptors."""
    return tuple(
        CanonicalEntityGraphNode(
            entity_type_ref=str(entity["type"]),
            identity_ref=str(entity["id"]),
            properties=tuple(
                sorted(
                    (str(key), value)
                    for key, value in (entity.get("properties", {}) or {}).items()
                    if key != "id"
                )
            ),
        )
        for entity in entities
    )
