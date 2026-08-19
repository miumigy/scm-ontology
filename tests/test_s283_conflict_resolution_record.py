from pathlib import Path


DOC = Path("docs/history/phase8/S283-m8-conflict-resolution-record.md")


def test_s283_defines_governed_decision_record() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Conflict Set",
        "Decision Proposal",
        "Governed Review",
        "Decision Record",
        "Explicit Application (if approved)",
    ):
        assert phrase in text


def test_s283_preserves_decision_history() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Decision history MUST be append-only",
        "Historical decisions MUST NOT be silently rewritten",
        "Rejected, superseded, and proposed decisions MUST remain observable",
        "Evidence and provenance MUST remain attached to the decision",
    ):
        assert phrase in text


def test_s283_separates_governance_from_canonical_mutation() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Approved decision MUST NOT mutate canonical facts by itself",
        "application MUST be an explicit governed step",
        "A decision MUST NOT infer Canonical Truth from provenance alone",
        "Reasoning MUST remain read-only",
    ):
        assert phrase in text


def test_s283_is_auditable_and_not_canonical_truth() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Decision rationale MUST be auditable and replayable" in text
    assert "It is not a Canonical Fact" in text
    assert "Vendor-specific governance rules MUST remain outside the Canonical Ontology" in text
