import pytest
from scm_ontology.semantic_surface_profile import SemanticSurfaceProfile
from scm_ontology.trace_bundle_profile import TraceBundleBoundaryError, enforce_trace_bundle_profile

PROFILE = SemanticSurfaceProfile("1.0.0", ("planning",), ("decision_trace", "execution_request"))

def test_trace_bundle_inside_profile_is_allowed():
    enforce_trace_bundle_profile(PROFILE, {"decision_trace": {}, "execution_request": {}})

def test_trace_bundle_outside_profile_is_rejected():
    with pytest.raises(TraceBundleBoundaryError):
        enforce_trace_bundle_profile(PROFILE, {"decision_trace": {}, "execution_event": {}})

def test_unknown_bundle_keys_do_not_bypass_known_semantic_boundary():
    enforce_trace_bundle_profile(PROFILE, {"custom_metadata": {}})
