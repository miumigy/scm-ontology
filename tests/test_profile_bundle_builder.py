import pytest
from scm_ontology.profile_bundle_builder import ProfileBundleConstructionError, build_profile_bundle
from scm_ontology.semantic_surface_profile import SemanticSurfaceProfile

PROFILE = SemanticSurfaceProfile("1.0.0", ("planning",), ("decision_trace", "execution_request"))

def test_builder_constructs_only_profile_allowed_elements():
    bundle = build_profile_bundle(PROFILE, {"decision_trace": {"id": "d1"}, "execution_request": {"id": "r1"}})
    assert bundle == {"decision_trace": {"id": "d1"}, "execution_request": {"id": "r1"}}

def test_builder_rejects_element_outside_profile():
    with pytest.raises(ProfileBundleConstructionError):
        build_profile_bundle(PROFILE, {"execution_event": {"id": "e1"}})

def test_builder_does_not_invent_missing_elements():
    bundle = build_profile_bundle(PROFILE, {"decision_trace": {"id": "d1"}})
    assert bundle == {"decision_trace": {"id": "d1"}}
