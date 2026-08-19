from pathlib import Path


DOC = Path("docs/history/phase7/M7-acceptance-report.md")


def test_m7_acceptance_report_declares_completion() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "**M7 COMPLETE**" in text
    assert "S275" in text
    assert "S276" in text
    assert "S277" in text


def test_m7_acceptance_report_preserves_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Enterprise Representation → Canonical Semantics" in text
    assert "Adapter is therefore a semantic boundary" in text
    assert "Reasoning remains read-only" in text
    assert "Graph mutation remains an explicit governed application stage" in text


def test_m7_acceptance_report_preserves_safety_invariants() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "automatic Canonical entity, attribute, or predicate creation",
        "implicit Canonical Fact mutation",
        "silent ambiguity resolution",
        "silent provenance loss",
        "Semantic Gap into an ontology extension",
        "automatic promotion of Planning / Derived Artifacts",
        "historical audit rewriting",
        "vendor-specific semantics crossing the Adapter Boundary",
    ):
        assert phrase in text


def test_m7_acceptance_report_defines_next_phase_without_weakening_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "multi-source canonical graph integration" in text
    assert "cross-enterprise identity resolution" in text
    assert "canonical fact lifecycle and versioning" in text
    assert "enterprise-scale" in text
    assert "not reasons to weaken the M7 boundary" in text
