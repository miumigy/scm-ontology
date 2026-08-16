"""Profile-aware reference Trace Bundle factory.

The factory is intentionally small: it centralizes construction so callers cannot
accidentally bypass the negotiated semantic-surface boundary.
"""
from __future__ import annotations
from collections.abc import Mapping
from .profile_bundle_builder import build_profile_bundle
from .semantic_surface_profile import SemanticSurfaceProfile

class TraceBundleFactory:
    def __init__(self, profile: SemanticSurfaceProfile) -> None:
        self._profile = profile

    @property
    def profile(self) -> SemanticSurfaceProfile:
        return self._profile

    def build(self, elements: Mapping[str, object]) -> dict[str, object]:
        return build_profile_bundle(self._profile, elements)


def create_trace_bundle_factory(profile: SemanticSurfaceProfile) -> TraceBundleFactory:
    return TraceBundleFactory(profile)
