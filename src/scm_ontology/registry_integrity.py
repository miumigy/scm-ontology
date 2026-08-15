from __future__ import annotations

from collections.abc import Iterable

from .canonical_relations import CanonicalRelationType


class RegistryIntegrityError(ValueError):
    pass


def validate_relation_registry(
    relations: Iterable[CanonicalRelationType],
) -> None:
    """Validate predicate uniqueness and complete inverse namespace coverage."""
    items = tuple(relations)
    predicates = {item.predicate_ref for item in items}
    if len(predicates) != len(items):
        raise RegistryIntegrityError("predicate refs must be unique")

    inverse_refs = {item.inverse_ref for item in items if item.inverse_ref}
    undeclared = inverse_refs - predicates
    if undeclared:
        raise RegistryIntegrityError(
            "inverse refs must be declared predicate refs: "
            + ", ".join(sorted(undeclared))
        )
