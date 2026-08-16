import pytest
from scm_ontology.semantic_surface_profile import SemanticSurfaceProfile
from scm_ontology.trace_bundle_factory import TraceBundleFactory, create_trace_bundle_factory
from scm_ontology.profile_bundle_builder import ProfileBundleConstructionError

PROFILE = SemanticSurfaceProfile("1.0.0", ("planning",), ("decision_trace", "execution_request"))

def test_factory_requires_and_retains_a_semantic_profile():
    factory = create_trace_bundle_factory(PROFILE)
    assert isinstance(factory, TraceBundleFactory)
    assert factory.profile == PROFILE

def test_factory_delegates_construction_through_profile_boundary():
    factory = TraceBundleFactory(PROFILE)
    assert factory.build({"decision_trace": {"id": "d1"}}) == {"decision_trace": {"id": "d1"}}

def test_factory_cannot_construct_outside_negotiated_surface():
    factory = TraceBundleFactory(PROFILE)
    with pytest.raises(ProfileBundleConstructionError):
        factory.build({"execution_event": {"id": "e1"}})
