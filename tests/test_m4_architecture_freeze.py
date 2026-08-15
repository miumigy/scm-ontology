from pathlib import Path


DOC = Path("docs/architecture/M4-architecture-freeze.md")


def test_m4_architecture_freeze_contains_truth_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Canonical truth is distinct from derived and inferred information." in text
    assert "Reasoning is read-only by default." in text
    assert "Inferred information cannot become canonical truth implicitly." in text


def test_m4_architecture_freeze_contains_layer_boundaries() -> None:
    text = DOC.read_text(encoding="utf-8")
    for layer in (
        "Canonical Semantic Model",
        "Canonical Graph",
        "Query / Traversal",
        "Constraint Evaluation",
        "Evidence / Provenance",
        "Reasoning Result",
        "Explanation / Confidence",
        "Reasoning Policy",
        "External Adapters",
    ):
        assert layer in text
