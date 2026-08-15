import pytest

from scm_ontology.epistemic_provenance import (
    EpistemicAssertion,
    EpistemicStatus,
    Evidence,
    EvidenceAssessment,
    EvidenceRole,
    ProvenanceAssertion,
)


def test_fact_and_inference_are_distinct() -> None:
    fact = EpistemicAssertion("a:1", "inventory:1", EpistemicStatus.FACT)
    inference = EpistemicAssertion("a:2", "inventory:1", EpistemicStatus.INFERENCE, confidence=0.8)
    assert fact.is_fact
    assert not fact.is_inference
    assert inference.is_inference


def test_unknown_cannot_claim_confidence() -> None:
    with pytest.raises(ValueError, match="confidence"):
        EpistemicAssertion("a:1", "x:1", EpistemicStatus.UNKNOWN, confidence=0.2)


def test_confidence_is_bounded() -> None:
    with pytest.raises(ValueError, match="between 0 and 1"):
        EpistemicAssertion("a:1", "x:1", EpistemicStatus.INFERENCE, confidence=1.2)


def test_evidence_keeps_source_and_role() -> None:
    evidence = Evidence("e:1", "source:erp", EvidenceRole.SUPPORTING)
    assert evidence.source_ref == "source:erp"
    assert evidence.role is EvidenceRole.SUPPORTING


def test_provenance_requires_source_lineage() -> None:
    with pytest.raises(ValueError, match="source_refs"):
        ProvenanceAssertion("p:1", "metric:1", ())


def test_evidence_assessment_is_bounded() -> None:
    with pytest.raises(ValueError, match="between 0 and 1"):
        EvidenceAssessment("e:1", "a:1", -0.1)
