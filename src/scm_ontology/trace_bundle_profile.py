"""Profile-aware Trace Bundle boundary checks."""
from __future__ import annotations
from collections.abc import Mapping
from .profile_enforcement import enforce_semantic_elements
from .semantic_surface_profile import SemanticSurfaceProfile

class TraceBundleBoundaryError(ValueError):
    pass

_ELEMENT_KEYS = frozenset({"decision_trace", "execution_request", "execution_event", "reasoning_provenance", "validation"})

def enforce_trace_bundle_profile(profile: SemanticSurfaceProfile, bundle: Mapping[str, object]) -> None:
    requested = frozenset(key for key in _ELEMENT_KEYS if key in bundle)
    try:
        enforce_semantic_elements(profile, requested)
    except ValueError as exc:
        raise TraceBundleBoundaryError(str(exc)) from exc
