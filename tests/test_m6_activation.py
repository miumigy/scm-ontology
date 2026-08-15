from pathlib import Path


def test_m6_is_active_in_milestone_roadmap() -> None:
    text = Path("docs/milestones/README.md").read_text(encoding="utf-8")
    assert "M6" in text
    assert "SCM Graph Integration" in text
    assert "Active" in text


def test_m6_fixture_families_are_defined() -> None:
    text = Path("docs/graph-fixtures/README.md").read_text(encoding="utf-8")
    for family in ("supply dependency chain", "inventory/capacity chain", "multi-hop supply-risk chain"):
        assert family in text
