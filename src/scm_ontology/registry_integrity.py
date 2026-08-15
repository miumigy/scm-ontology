from __future__ import annotations

from collections.abc import Iterable

from .canonical_relations import CanonicalRelationType


class RegistryIntegrityError(ValueError):
    pass


def validate_relation_registry(
    relations: Iterable[CanonicalRelationType],
) -> None:
    """Validate predicate uniqueness and reciprocal integrity for registered inverses."""
    items = tuple(relations)
    by_predicate = {item.predicate_ref: item for item in items}
    if len(by_predicate) != len(items):
        raise RegistryIntegrityError("predicate refs must be unique")

    for item in items:
        if item.inverse_ref in by_predicate:
            inverse = by_predicate[item.inverse_ref]
            if inverse.inverse_ref != item.predicate_ref:
                raise RegistryIntegrityError(
                    f"inverse relation must be reciprocal: {item.predicate_ref} ↔ {item.inverse_ref}"
                )
