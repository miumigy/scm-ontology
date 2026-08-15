from pathlib import Path


DOC = Path("docs/milestones/S273-m7-adapter-conformance-contract.md")


def test_s273_requires_core_invariants() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "preserve Enterprise-to-Canonical directionality",
        "identify the source representation and adapter version",
        "preserve provenance for mapped outputs",
        "expose mapping confidence where applicable",
        "represent ambiguous mappings explicitly",
        "represent unmappable data explicitly",
        "preserve Semantic Gap classification",
        "preserve the scope of an approved Governance Decision",
        "remain traceable to the Mapping Configuration used for execution",
    ):
        assert phrase in text


def test_s273_forbids_canonical_contamination() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "MUST NOT create a new canonical entity, attribute, or predicate automatically",
        "MUST NOT mutate canonical facts",
        "MUST NOT infer Canonical Truth solely from source labels, vendor codes, mapping success, or adapter behavior",
        "MUST NOT silently discard provenance",
        "MUST NOT silently resolve ambiguity",
        "MUST NOT silently convert unmappable data into a new Canonical concept",
        "MUST NOT rewrite historical canonicalization results",
        "MUST NOT treat vendor-specific semantics as Canonical Semantics without an explicit approved mapping",
    ):
        assert phrase in text


def test_s273_defines_explicit_results() -> None:
    text = DOC.read_text(encoding="utf-8")
    for result in ("`conformant`", "`non_conformant`", "`inconclusive`"):
        assert result in text
    assert "`inconclusive` MUST NOT be interpreted as `conformant`" in text


def test_s273_requires_failure_and_regression_controls() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT be presented as eligible for unrestricted Canonicalization" in text
    assert "SHOULD be repeatable against a fixed Adapter Fixture" in text
    assert "MUST be re-evaluated when a change can affect its Canonicalization behavior" in text


def test_s273_separates_conformance_from_governance() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Conformance is a technical contract check" in text
    assert "It is not a Governance Decision" in text
    assert "MUST proceed through the applicable Governance process" in text
