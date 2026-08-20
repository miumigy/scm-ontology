from pathlib import Path


DOC = Path("docs/history/legacy/m6-e2e-business-questions.md")


def test_m6_e2e_contract_covers_graph_to_answer() -> None:
    text = DOC.read_text(encoding="utf-8")
    for value in ("Canonical Query", "Graph Path Resolution", "Evidence / Provenance", "Explanation", "Confidence", "Business Answer"):
        assert value in text


def test_m6_e2e_contract_has_four_representative_questions() -> None:
    text = DOC.read_text(encoding="utf-8")
    for value in ("Q-001", "Q-003", "Q-004", "Q-005"):
        assert value in text


def test_m6_e2e_preserves_read_only_and_no_inference_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "no graph mutation" in text
    assert "no implicit canonical-fact creation" in text
    assert "explicit `no_match`" in text
