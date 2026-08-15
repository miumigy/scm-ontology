from __future__ import annotations

from .canonical_relations import CANONICAL_RELATION_TYPES, RelationKind


_RELATIONS_BY_PREDICATE = {item.predicate_ref: item for item in CANONICAL_RELATION_TYPES}


def relation_kind(predicate_ref: str) -> RelationKind:
    """Return the canonical semantic class of a registered predicate."""
    try:
        return _RELATIONS_BY_PREDICATE[predicate_ref].kind
    except KeyError as exc:
        raise ValueError(f"unknown canonical predicate: {predicate_ref}") from exc


def is_causal_relation(predicate_ref: str) -> bool:
    return relation_kind(predicate_ref) is RelationKind.CAUSAL


def is_operational_relation(predicate_ref: str) -> bool:
    return relation_kind(predicate_ref) is RelationKind.OPERATIONAL
