from __future__ import annotations

from dataclasses import dataclass

from .extension_registry_application_preflight import RegistryApplicationPreflight


class RegistryMutationGuardError(ValueError):
    pass


@dataclass(frozen=True)
class RegistryMutationGuard:
    preflight: RegistryApplicationPreflight
    predicate_refs: frozenset[str]
    inverse_refs: frozenset[str]


def build_registry_mutation_guard(
    preflight: RegistryApplicationPreflight,
    *,
    predicate_refs: frozenset[str],
    inverse_refs: frozenset[str],
) -> RegistryMutationGuard:
    if not preflight.ready:
        raise RegistryMutationGuardError("registry application preflight is not ready")
    if not predicate_refs:
        raise RegistryMutationGuardError("predicate_refs must not be empty")
    undeclared_inverse_refs = inverse_refs - predicate_refs
    if undeclared_inverse_refs:
        raise RegistryMutationGuardError(
            "inverse refs must be declared predicate refs: "
            + ", ".join(sorted(undeclared_inverse_refs))
        )
    return RegistryMutationGuard(
        preflight=preflight,
        predicate_refs=predicate_refs,
        inverse_refs=inverse_refs,
    )
