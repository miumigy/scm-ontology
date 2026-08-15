from __future__ import annotations

from dataclasses import dataclass

from .extension_proposal import ExtensionProposal


class InvalidRegistryApplicationPlan(ValueError):
    pass


@dataclass(frozen=True)
class RegistryApplicationPlan:
    proposal: ExtensionProposal


def plan_registry_application(proposal: ExtensionProposal) -> RegistryApplicationPlan:
    """Create an explicit validated plan; do not mutate the canonical registry."""
    if not proposal.candidate_ref or not proposal.predicate_ref:
        raise InvalidRegistryApplicationPlan("proposal must identify candidate and predicate")
    if not proposal.subject_type or not proposal.object_type:
        raise InvalidRegistryApplicationPlan("proposal must identify endpoint types")
    return RegistryApplicationPlan(proposal)
