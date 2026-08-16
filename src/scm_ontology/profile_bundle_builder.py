"""Construct Trace Bundles within a negotiated semantic profile."""
from __future__ import annotations
from collections.abc import Mapping
from .profile_enforcement import enforce_semantic_elements
from .semantic_surface_profile import SemanticSurfaceProfile

class ProfileBundleConstructionError(ValueError):
    pass

def build_profile_bundle(profile: SemanticSurfaceProfile, elements: Mapping[str, object]) -> dict[str, object]:
    requested = frozenset(elements)
    try:
        enforce_semantic_elements(profile, requested)
    except ValueError as exc:
        raise ProfileBundleConstructionError(str(exc)) from exc
    return {key: elements[key] for key in profile.semantic_elements if key in elements}
