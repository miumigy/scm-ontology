"""Enforce negotiated SCM semantic-surface boundaries."""
from __future__ import annotations
from .semantic_surface_profile import SemanticSurfaceProfile

class SemanticBoundaryError(ValueError):
    pass

def enforce_semantic_elements(profile: SemanticSurfaceProfile, requested_elements: set[str] | frozenset[str]) -> None:
    requested = frozenset(requested_elements)
    if not requested <= frozenset(profile.semantic_elements):
        denied = sorted(requested - frozenset(profile.semantic_elements))
        raise SemanticBoundaryError(f"semantic elements outside negotiated surface: {', '.join(denied)}")

def enforce_capabilities(profile: SemanticSurfaceProfile, requested_capabilities: set[str] | frozenset[str]) -> None:
    requested = frozenset(requested_capabilities)
    if not requested <= frozenset(profile.shared_capabilities):
        denied = sorted(requested - frozenset(profile.shared_capabilities))
        raise SemanticBoundaryError(f"capabilities outside negotiated surface: {', '.join(denied)}")
