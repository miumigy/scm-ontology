from __future__ import annotations

from dataclasses import dataclass

from .extension_registry_application_gate import RegistryApplicationGate


@dataclass(frozen=True)
class RegistryApplicationPreflight:
    gate: RegistryApplicationGate
    ready: bool


def run_registry_application_preflight(
    gate: RegistryApplicationGate,
) -> RegistryApplicationPreflight:
    """Confirm readiness without applying the proposal to the registry."""
    return RegistryApplicationPreflight(gate=gate, ready=gate.validated)
