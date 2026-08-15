from __future__ import annotations

from dataclasses import dataclass

from .extension_proposal import ExtensionProposal


@dataclass(frozen=True)
class RegistryApplicationPlan:
    proposal: ExtensionProposal


def plan_registry_application(proposal: ExtensionProposal) -> RegistryApplicationPlan:
    """Create an explicit plan; do not mutate the canonical registry."""
    return RegistryApplicationPlan(proposal)
