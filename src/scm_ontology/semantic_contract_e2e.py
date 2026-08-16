"""End-to-end semantic contract enforcement for Trace Bundle construction."""
from __future__ import annotations
from collections.abc import Mapping
from dataclasses import dataclass
from .capability_aware_negotiation import negotiate_semantic_surface
from .capability_negotiation import CapabilitySet
from .profile_bundle_builder import build_profile_bundle
from .semantic_surface_profile import SemanticSurfaceProfile, profile_from_negotiation

@dataclass(frozen=True)
class SemanticContractSession:
    profile: SemanticSurfaceProfile

    @classmethod
    def negotiate(cls, producer: CapabilitySet, consumer: CapabilitySet) -> "SemanticContractSession":
        result = negotiate_semantic_surface(producer, consumer)
        return cls(profile_from_negotiation(result))

    def build_bundle(self, elements: Mapping[str, object]) -> dict[str, object]:
        return build_profile_bundle(self.profile, elements)
