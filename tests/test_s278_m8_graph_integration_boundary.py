from pathlib import Path


DOC = Path("docs/milestones/S278-m8-graph-integration-boundary.md")


def test_s278_requires_m7_input_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Only Canonicalization Results that satisfy the M7 contract may enter this stage." in text
    assert "MUST consume explicit Canonicalization Results, not raw enterprise records" in text


def test_s278_protects_canonical_semantics() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "MUST NOT create a new canonical entity, attribute, or predicate automatically",
        "MUST NOT mutate canonical facts implicitly",
        "Source identity and provenance MUST remain attached",
        "conflicts MUST remain observable",
        "Identity similarity MUST NOT by itself establish Canonical Identity",
        "MUST be replayable",
        "Reasoning MUST remain read-only",
        "Semantic Gap and unresolved identity MUST remain first-class outcomes",
    ):
        assert phrase in text


def test_s278_separates_identity_match_from_governed_identity() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Source Identity" in text
    assert "Candidate Identity Match" in text
    assert "Governed Canonical Identity" in text
    assert "MUST NOT be treated as a Governed Canonical Identity" in text


def test_s278_preserves_conflicts_and_defines_non_goals() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST preserve the conflict and its provenance" in text
    assert "MUST NOT silently select a winner" in text
    assert "does not implement probabilistic entity resolution" in text
    assert "autonomous graph mutation" in text
