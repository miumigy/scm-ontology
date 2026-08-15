from pathlib import Path


DOC = Path("docs/milestones/S267-m7-governance-decision-contract.md")


def test_s267_defines_decision_identity() -> None:
    text = DOC.read_text(encoding="utf-8")
    for field in (
        "decision_id",
        "signal_id",
        "decision_state",
        "decision_reason",
        "decided_by",
        "decided_at",
        "mapping_rule_version",
        "adapter_version",
        "scope",
    ):
        assert f"`{field}`" in text


def test_s267_requires_explicit_decision_states() -> None:
    text = DOC.read_text(encoding="utf-8")
    for state in ("approved", "rejected", "deferred", "needs_more_evidence"):
        assert f"`{state}`" in text
    assert "Absence of a decision MUST NOT be interpreted as approval" in text


def test_s267_limits_approval_scope() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT silently authorize unrelated ontology expansion" in text
    assert "A proposal for a new canonical concept remains a proposal" in text


def test_s267_preserves_canonical_truth_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT create a new canonical entity, attribute, or predicate automatically" in text
    assert "MUST NOT mutate canonical facts as a side effect of review" in text
    assert "MUST NOT infer a canonical fact from approval alone" in text
    assert "MUST NOT rewrite historical audit records" in text
    assert "approved mapping" in text
    assert "asserted business fact" in text


def test_s267_preserves_evidence_and_provenance() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT erase ambiguity, provenance, semantic gaps, or contradictory evidence" in text
    assert "evidence references SHOULD remain attached" in text


def test_s267_requires_versioned_explainability() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "mapping-rule and adapter versions" in text
    assert "what was decided, why it was decided, by whom, when, and within what scope" in text
