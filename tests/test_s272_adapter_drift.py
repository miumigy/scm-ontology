from pathlib import Path


DOC = Path("docs/milestones/S272-m7-adapter-drift-contract.md")


def test_s272_defines_drift_dimensions() -> None:
    text = DOC.read_text(encoding="utf-8")
    for item in (
        "enterprise field structure or datatype",
        "source-system relation or identifier behavior",
        "adapter transformation behavior",
        "mapping-rule version",
        "mapping target",
        "mapping confidence",
        "provenance availability",
        "semantic-gap classification",
        "approved decision scope",
    ):
        assert item in text


def test_s272_defines_drift_classification() -> None:
    text = DOC.read_text(encoding="utf-8")
    for classification in (
        "representation_drift",
        "adapter_behavior_drift",
        "mapping_drift",
        "provenance_drift",
        "semantic_gap_drift",
        "scope_drift",
        "inconclusive_drift",
    ):
        assert f"`{classification}`" in text
    assert "not a Canonical Truth assertion" in text


def test_s272_preserves_history() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST preserve the versions being compared" in text
    assert "MUST NOT rewrite historical adapter decisions" in text
    assert "MUST NOT be treated as if it had always used the current mapping" in text


def test_s272_preserves_canonical_truth_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT create a new canonical entity, attribute, or predicate automatically" in text
    assert "MUST NOT mutate canonical facts" in text
    assert "MUST NOT infer a canonical fact from drift alone" in text
    assert "MUST NOT silently replace an approved mapping" in text
    assert "MUST NOT expand the Canonical Ontology merely because a representation changed" in text


def test_s272_requires_controlled_governance_handoff() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MAY produce a Governance Signal" in text
    assert "MUST follow the applicable controlled Governance Decision process" in text
    assert "MUST NOT itself authorize mapping replacement" in text


def test_s272_requires_explainability() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "compared versions" in text
    assert "affected scope" in text
    assert "changed dimensions" in text
    assert "evidence references" in text
    assert "classification rationale" in text
