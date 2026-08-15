from __future__ import annotations

from dataclasses import dataclass

from .canonical_relations import CanonicalRelationType, RelationKind
from .extension_proposal import ExtensionProposal
from .registry_mutation_guard import RegistryMutationGuard


class CanonicalRegistryMutationError(ValueError):
    pass


@dataclass(frozen=True)
class CanonicalRegistryMutationResult:
    registry: tuple[CanonicalRelationType, ...]
    applied_predicate_ref: str


def apply_canonical_registry_mutation(
    guard: RegistryMutationGuard,
    registry: tuple[CanonicalRelationType, ...],
    *,
    kind: RelationKind,
    inverse_ref: str | None = None,
) -> CanonicalRegistryMutationResult:
    """Functionally apply an accepted proposal to a canonical relation snapshot."""
    proposal: ExtensionProposal = guard.preflight.gate.plan.proposal
    existing_predicates = {item.predicate_ref for item in registry}
    existing_inverses = {item.inverse_ref for item in registry if item.inverse_ref}

    if proposal.predicate_ref in existing_predicates or proposal.predicate_ref in existing_inverses:
        raise CanonicalRegistryMutationError(
            f"predicate ref already exists in canonical registry: {proposal.predicate_ref}"
        )
    if inverse_ref == proposal.predicate_ref:
        raise CanonicalRegistryMutationError("a relation cannot be its own inverse")
    if inverse_ref and (inverse_ref in existing_predicates or inverse_ref in existing_inverses):
        raise CanonicalRegistryMutationError(
            f"inverse ref already exists in canonical registry: {inverse_ref}"
        )

    relation = CanonicalRelationType(
        predicate_ref=proposal.predicate_ref,
        kind=kind,
        inverse_ref=inverse_ref,
    )
    return CanonicalRegistryMutationResult(
        registry=registry + (relation,),
        applied_predicate_ref=relation.predicate_ref,
    )
