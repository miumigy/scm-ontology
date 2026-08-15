import pytest

from scm_ontology.evidence_provenance import EvidenceRef, EvidenceSet
from scm_ontology.reasoning_result import ReasoningResult, ReasoningResultError


def test_reasoning_result_preserves_matches_and_evidence() -> None:
    evidence = EvidenceSet(refs=(EvidenceRef("erp:order:123"),))
    result = ReasoningResult(
        result_ref="reasoning:1",
        status="supported",
        matches=("product:1",),
        evidence=evidence,
        explanation="explicit property match",
    )
    assert result.matches == ("product:1",)
    assert result.evidence == evidence
    assert result.metadata == {}


def test_reasoning_result_requires_identity_and_status() -> None:
    with pytest.raises(ReasoningResultError):
        ReasoningResult("", "supported")
    with pytest.raises(ReasoningResultError):
        ReasoningResult("reasoning:1", "")
