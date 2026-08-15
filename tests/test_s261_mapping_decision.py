from pathlib import Path


DOC = Path("docs/milestones/S261-m7-mapping-decision-contract.md")


def test_s261_defines_explicit_decision_states() -> None:
    text = DOC.read_text(encoding="utf-8")
    for state in (
        "mapped",
        "ambiguous",
        "unmappable",
        "unsupported",
        "vendor_specific",
        "insufficient_evidence",
        "conflicting_semantics",
        "rejected",
    ):
        assert f"`{state}`" in text


def test_s261_separates_mapping_confidence_from_fact_truth() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT be interpreted as" in text
    assert "permission to create a Canonical Fact" in text


def test_s261_mapped_does_not_mean_true() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT be treated as a Canonical Fact merely because its state is `mapped`" in text
    assert "MUST NOT treat `mapped` as equivalent to `true`" in text


def test_s261_preserves_provenance_and_semantic_gap() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "provenance" in text
    assert "semantic_gap" in text
    assert "rather than replacing them with a single confidence value" in text


def test_s261_forbids_canonical_mutation() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT create a new canonical entity, attribute, or predicate automatically" in text
    assert "MUST NOT mutate canonical facts" in text
    assert "MUST NOT infer a canonical fact from a mapping decision alone" in text


def test_s261_requires_explainable_decisions() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST have an explainable `reason`" in text
    assert "MUST NOT be hidden behind a null result" in text
