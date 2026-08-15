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
class RegistryApplicationResult:
    preflight: RegistryApplicationPreflight
    applied: bool


def plan_registry_application(proposal: ExtensionProposal) -> RegistryApplicationPlan:
    """Create an explicit validated plan; do not mutate the canonical registry."""
    if not proposal.candidate_ref or not proposal.predicate_ref:
        raise InvalidRegistryApplicationPlan("proposal must identify candidate and predicate")
    if not proposal.subject_type or not proposal.object_type:
        raise InvalidRegistryApplicationPlan("proposal must identify endpoint types")
    return RegistryApplicationPlan(proposal)


def apply_registry_application(
    preflight: RegistryApplicationPreflight,
) -> RegistryApplicationResult:
    """Record application intent without mutating the canonical registry yet."""
    if not preflight.ready:
        raise RegistryApplicationNotReady("registry application preflight is not ready")
    return RegistryApplicationResult(preflight=preflight, applied=True)
