from pathlib import Path


DOC = Path("docs/milestones/S269-m7-application-effectiveness-contract.md")


def test_s269_defines_assessment_identity() -> None:
    text = DOC.read_text(encoding="utf-8")
    for field in (
        "assessment_id",
        "decision_id",
        "effective configuration version",
        "observed execution references",
        "assessment scope",
        "assessment criteria",
        "assessment result",
        "assessed_at",
    ):
        assert field in text
    assert "MUST remain traceable" in text


def test_s269_defines_bounded_outcomes() -> None:
    text = DOC.read_text(encoding="utf-8")
    for outcome in (
        "effective",
        "partially_effective",
        "ineffective",
        "inconclusive",
        "not_evaluable",
    ):
        assert f"`{outcome}`" in text
    assert "MUST NOT be generalized to unrelated enterprise representations" in text


def test_s269_separates_observation_from_canonical_truth() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Observed mapping outcomes are evidence about adapter behavior" in text
    assert "MUST NOT automatically become Canonical Facts" in text


def test_s269_preserves_canonical_truth_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT create a new canonical entity, attribute, or predicate automatically" in text
    assert "MUST NOT mutate canonical facts" in text
    assert "MUST NOT infer a canonical fact from effectiveness alone" in text
    assert "MUST NOT rewrite historical audit records" in text
    assert "MUST NOT silently alter the approved Governance Decision" in text


def test_s269_requires_controlled_change() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST proceed through a new controlled Governance Decision" in text
    assert "original decision and its application history remain intact" in text


def test_s269_requires_explainability() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "observed executions" in text
    assert "relevant versions" in text
    assert "evidence supporting its outcome" in text
    assert "`inconclusive` and `not_evaluable`" in text
