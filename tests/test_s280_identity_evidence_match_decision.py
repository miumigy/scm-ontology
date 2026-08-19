from pathlib import Path


DOC = Path("docs/history/phase8/S280-m8-identity-evidence-match-decision.md")


def test_s280_defines_identity_decision_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Identity Evidence",
        "Candidate Identity Match",
        "Match Decision",
        "Governed Canonical Identity",
    ):
        assert phrase in text


def test_s280_preserves_evidence_and_governance() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Identity evidence MUST remain distinguishable from Canonical Truth",
        "Evidence MUST NOT be promoted to Canonical Identity automatically",
        "A confidence score MUST NOT by itself establish Canonical Identity",
        "Ambiguous or insufficient evidence MUST remain an explicit unresolved outcome",
        "Conflicting evidence MUST remain observable",
        "Provenance MUST remain attached",
        "auditable and replayable",
    ):
        assert phrase in text


def test_s280_forbids_implicit_canonical_mutation() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Reasoning MUST remain read-only" in text
    assert "MUST NOT create a new canonical entity, attribute, or predicate automatically" in text
    assert "MUST NOT mutate canonical facts without an explicit governed application step" in text


def test_s280_defines_non_goals() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "does not implement probabilistic entity-resolution algorithms" in text
    assert "autonomous graph mutation" in text
