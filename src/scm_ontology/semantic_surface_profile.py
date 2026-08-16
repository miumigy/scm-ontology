"""Reusable profile of the semantic surface negotiated between two systems."""
from __future__ import annotations
from dataclasses import dataclass
from .capability_aware_negotiation import SemanticNegotiation

@dataclass(frozen=True)
class SemanticSurfaceProfile:
    schema_version: str
    shared_capabilities: tuple[str, ...]
    semantic_elements: tuple[str, ...]

    @property
    def usable(self) -> bool:
        return bool(self.shared_capabilities and self.semantic_elements)


def profile_from_negotiation(result: SemanticNegotiation, *, preferred_schema_version: str | None = None) -> SemanticSurfaceProfile:
    if not result.compatible_versions:
        raise ValueError("cannot create semantic surface profile without a compatible schema version")
    version = preferred_schema_version or result.compatible_versions[-1]
    if version not in result.compatible_versions:
        raise ValueError(f"preferred schema version is not negotiated: {version}")
    return SemanticSurfaceProfile(version, result.shared_capabilities, result.shared_semantic_elements)
