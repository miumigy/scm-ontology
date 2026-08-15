from __future__ import annotations

from dataclasses import dataclass

from .extension_registry_application_preflight import RegistryApplicationPreflight


class CanonicalRegistryApplicationError(ValueError):
    pass


@dataclass(frozen=True)
class CanonicalRegistryApplicationResult:
    preflight: RegistryApplicationPreflight
    applied: bool


def apply_to_canonical_registry(
    preflight: RegistryApplicationPreflight,
) -> CanonicalRegistryApplicationResult:
    """Cross the application boundary only after a successful preflight.

    The current implementation records the governed application result; the
    canonical relation registry remains unchanged until its dedicated mutation
    API is introduced.
    """
    if not preflight.ready:
        raise CanonicalRegistryApplicationError("registry application is not ready")
    return CanonicalRegistryApplicationResult(preflight=preflight, applied=True)
