from __future__ import annotations

from dataclasses import dataclass


class ExtensionAlreadyApplied(ValueError):
    pass


@dataclass(frozen=True)
class ExtensionApplicationKey:
    proposal_ref: str
    target_registry_version: str


def ensure_not_already_applied(
    key: ExtensionApplicationKey,
    applied_keys: frozenset[ExtensionApplicationKey],
) -> bool:
    """Return True when the application is new; reject duplicate application."""
    if key in applied_keys:
        raise ExtensionAlreadyApplied(
            f"extension application already exists: {key.proposal_ref}"
        )
    return True
