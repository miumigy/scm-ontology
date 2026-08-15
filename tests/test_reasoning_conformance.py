from scm_ontology.path_reasoning_result import PathReasoningResult
from scm_ontology.reasoning_conformance import validate_reasoning_result_conformance
from scm_ontology.reasoning_policy import ReasoningPolicy


def test_reasoning_result_is_canonical_safe() -> None:
    report = validate_reasoning_result_conformance(PathReasoningResult("result:1", "matched"), ReasoningPolicy())
    assert report.canonical_safe is True
    assert report.read_only is False


def test_conformance_preserves_result_identity() -> None:
    result = PathReasoningResult("result:2", "no_match")
    report = validate_reasoning_result_conformance(result, ReasoningPolicy())
    assert report.result_ref == result.result_ref
