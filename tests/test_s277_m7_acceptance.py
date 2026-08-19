from pathlib import Path


DOC = Path("docs/history/phase7/S277-m7-acceptance.md")


def test_s277_acceptance_chain_is_complete() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Enterprise Representation",
        "Adapter Conformance",
        "Approved Mapping",
        "Canonicalization Result",
        "Provenance / Audit",
        "Governed Graph Application",
        "Canonical SCM Graph",
    ):
        assert phrase in text


def test_s277_requires_core_m7_properties() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "enterprise representations remain outside Canonical Semantics",
        "entity, attribute, and predicate mappings are explicit and versioned",
        "provenance and mapping confidence survive Canonicalization",
        "ambiguity and Semantic Gap remain observable",
        "negative contamination cases remain non-success outcomes",
        "Canonicalization Result is distinct from authorization",
        "applied graph changes are traceable",
        "replay does not rewrite historical execution records",
        "Reasoning remains read-only",
        "vendor-specific semantics do not cross the Adapter Boundary",
    ):
        assert phrase in text


def test_s277_defines_acceptance_failure_conditions() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "automatic Canonical concept creation",
        "implicit Canonical Fact mutation",
        "silent ambiguity resolution",
        "provenance loss",
        "silent Semantic Gap suppression",
        "Planning / Derived Artifact promotion",
        "historical audit rewriting",
        "vendor semantics entering Canonical Semantics",
    ):
        assert phrase in text


def test_s277_completion_requires_regression_and_boundary_evidence() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "full regression suite passes" in text
    assert "Enterprise Representation → Canonical Semantics boundary remains explicit" in text
    assert "auditable" in text
    assert "reversible by replay" in text
    assert "protected against Canonical contamination" in text
