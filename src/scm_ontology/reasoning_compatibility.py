from __future__ import annotations

from collections.abc import Iterable

from .canonical_relations import CanonicalRelationType


class ReasoningCompatibilityError(ValueError):
    pass


def validate_reasoning_compatibility(
    relations: Iterable[CanonicalRelationType],
) -> None:
    """Validate that projected relation semantics are sufficient for reasoning use."""
    items = tuple(relations)
    predicate_refs = {item.predicate_ref for item in items}
    if len(predicate_refs) != len(items):
        raise ReasoningCompatibilityError("predicate refs must be unique")

    for item in items:
        if item.inverse_ref is None:
            continue
        inverse = next(
            (candidate for candidate in items if candidate.predicate_ref == item.inverse_ref),
            None,
        )
        if inverse is not None and inverse.inverse_ref != item.predicate_ref:
            raise ReasoningCompatibilityError(
                f"non-reciprocal inverse is not reasoning-compatible: {item.predicate_ref}"
            )
