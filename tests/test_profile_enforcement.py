import pytest
from scm_ontology.profile_enforcement import SemanticBoundaryError, enforce_capabilities, enforce_semantic_elements
from scm_ontology.semantic_surface_profile import SemanticSurfaceProfile
PROFILE = SemanticSurfaceProfile("1.0.0", ("planning",), ("decision_trace", "execution_request"))
def test_allowed_semantic_surface_passes():
    enforce_semantic_elements(PROFILE, {"decision_trace"})
def test_denied_semantic_element_is_rejected():
    with pytest.raises(SemanticBoundaryError):
        enforce_semantic_elements(PROFILE, {"execution_event"})
def test_allowed_capability_passes():
    enforce_capabilities(PROFILE, {"planning"})
def test_denied_capability_is_rejected():
    with pytest.raises(SemanticBoundaryError):
        enforce_capabilities(PROFILE, {"execution"})
