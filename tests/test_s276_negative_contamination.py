from pathlib import Path


DOC = Path("docs/milestones/S276-m7-negative-contamination-tests.md")


def test_s276_requires_negative_cases() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "enterprise classification with no approved Canonical mapping",
        "ambiguous enterprise label",
        "provenance is missing or invalid",
        "predicate mapping is not approved",
        "create a new Canonical concept from an unmappable source value",
        "planning or derived artifact into a Canonical Fact",
        "vendor-specific semantic that has no approved Canonical mapping",
    ):
        assert phrase in text


def test_s276_forbids_canonical_contamination() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "MUST NOT create a new canonical entity, attribute, or predicate automatically",
        "MUST NOT mutate canonical facts as a side effect of mapping failure or ambiguity",
        "MUST NOT infer Canonical Truth from source labels, vendor codes, or mapping success alone",
        "MUST NOT silently resolve ambiguity",
        "MUST NOT silently discard provenance",
        "MUST NOT convert a Semantic Gap into a new Canonical concept",
        "MUST NOT promote Planning / Derived Artifacts into Canonical Facts automatically",
    ):
        assert phrase in text


def test_s276_requires_observable_non_success() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST produce an observable non-success outcome" in text
    assert "explicit Semantic Gap classification" in text
    assert "explicit governance-required outcome" in text
    assert "MUST NOT be represented as successful Canonicalization" in text


def test_s276_negative_cases_are_regression_controls() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST remain part of the regression suite" in text
    assert "MUST fail CI" in text
