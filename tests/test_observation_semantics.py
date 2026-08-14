from scm_ontology.observation_semantics import (
    ObservationSemanticBoundaryError,
    SemanticKind,
    semantic_definition,
    validate_semantic_kind,
)


def test_requires_explicit_semantic_kind():
    assert validate_semantic_kind(SemanticKind.OBSERVATION) is SemanticKind.OBSERVATION


def test_distinguishes_observation_state_and_event():
    assert "measured fact" in semantic_definition(SemanticKind.OBSERVATION)
    assert "condition" in semantic_definition(SemanticKind.STATE)
    assert "occurrence" in semantic_definition(SemanticKind.EVENT)


def test_rejects_implicit_string_classification():
    try:
        validate_semantic_kind("state")
    except ObservationSemanticBoundaryError as exc:
        assert "explicit SemanticKind" in str(exc)
    else:
        raise AssertionError("string classification must not be accepted")
