from pathlib import Path


def test_uc07_is_multi_hop_and_evidence_bound() -> None:
    text = Path("docs/use-cases/UC-07-supply-risk.md").read_text(encoding="utf-8")
    assert "multi-hop" in text
    assert "Evidence" in text
    assert "explicit risk fact" in text


def test_uc07_rejects_implicit_risk_promotion() -> None:
    text = Path("docs/use-cases/UC-07-supply-risk.md").read_text(encoding="utf-8")
    assert "must not be promoted to canonical truth" in text
    assert "without silently creating risk facts" in text
