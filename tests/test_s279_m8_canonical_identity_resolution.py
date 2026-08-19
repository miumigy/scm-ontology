from pathlib import Path


DOC = Path("docs/history/phase8/S279-m8-canonical-identity-resolution.md")


def test_s279_defines_identity_states() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Source Identity",
        "Candidate Identity Match",
        "Governed Canonical Identity",
        "MUST NOT be treated as a Governed Canonical Identity",
    ):
        assert phrase in text


def test_s279_protects_canonical_semantics() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Identity similarity MUST NOT by itself establish Canonical Identity",
        "MUST NOT create a new canonical entity, attribute, or predicate automatically",
        "MUST NOT mutate canonical facts implicitly",
        "Reasoning MUST remain read-only",
        "MUST NOT be silently resolved",
        "MUST NOT be silently discarded",
    ):
        assert phrase in text


def test_s279_preserves_evidence_confidence_and_replayability() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "preserve the evidence and rationale" in text
    assert "Confidence is metadata about a resolution decision, not Canonical Truth." in text
    assert "MUST be replayable" in text
    assert "MUST remain auditable" in text


def test_s279_keeps_unresolved_identity_and_semantic_gap_first_class() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Unresolved identity MUST remain a first-class outcome." in text
    assert "insufficient evidence" in text
    assert "MUST NOT expand the Canonical Ontology" in text
