from __future__ import annotations

from dataclasses import dataclass

from .extension_proposal import ExtensionProposal
from .extension_registry_application_preflight import RegistryApplicationPreflight


class InvalidRegistryApplicationPlan(ValueError):
    pass


class RegistryApplicationNotReady(ValueError):
    pass


@dataclass(frozen=True)
class RegistryApplicationPlan:
    proposal: ExtensionProposal


@dataclass(frozen=True)
class RegistryApplicationIntent:
    preflight: RegistryApplicationPreflight


def plan_registry_application(proposal: ExtensionProposal) -> RegistryApplicationPlan:
    """Create an explicit validated plan; do not mutate the canonical registry."""
    if not proposal.candidate_ref or not proposal.predicate_ref:
        raise InvalidRegistryApplicationPlan("proposal must identify candidate and predicate")
    if not proposal.subject_type or not proposal.object_type:
        raise InvalidRegistryApplicationPlan("proposal must identify endpoint types")
    return RegistryApplicationPlan(proposal)


def apply_registry_application(
    preflight: RegistryApplicationPreflight,
) -> RegistryApplicationIntent:
    """Create an immutable application intent; canonical mutation is a later step."""
    if not preflight.ready:
        raise RegistryApplicationNotReady("registry application preflight is not ready")
    return RegistryApplicationIntent(preflight=preflight)
