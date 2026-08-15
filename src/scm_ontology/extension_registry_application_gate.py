from __future__ import annotations

from dataclasses import dataclass

from .extension_registry_application import RegistryApplicationPlan


@dataclass(frozen=True)
class RegistryApplicationGate:
    plan: RegistryApplicationPlan
    validated: bool


def validate_registry_application_gate(
    plan: RegistryApplicationPlan,
) -> RegistryApplicationGate:
    """Mark a structurally valid plan as ready for a future governed apply step."""
    return RegistryApplicationGate(plan=plan, validated=True)
