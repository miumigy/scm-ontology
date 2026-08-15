from pathlib import Path


DOC = Path("docs/architecture/v0.2-release-candidate.md")


def test_v02_rc_contains_frozen_stack() -> None:
    text = DOC.read_text(encoding="utf-8")
    for layer in (
        "Canonical Semantic Model",
        "Canonical Graph",
        "Query / Traversal",
        "Constraints",
        "Evidence / Provenance",
        "Reasoning Result",
        "Explanation / Confidence",
        "Reasoning Policy",
        "SCM Reasoning Patterns",
        "External Adapters",
    ):
        assert layer in text


def test_v02_rc_preserves_truth_and_read_only_boundaries() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Reasoning is read-only by default." in text
    assert "Inferred information is never promoted to canonical truth implicitly." in text
    assert "Evidence is provenance metadata, not ontology truth." in text
    assert "Confidence is derived metadata, not ontology truth." in text
