from pathlib import Path


def test_s237_catalog_contains_stable_use_case_ids() -> None:
    text = Path("docs/use-cases/M5-use-case-catalog.md").read_text(encoding="utf-8")
    for use_case_id in ("UC-01", "UC-02", "UC-03", "UC-04", "UC-05", "UC-06", "UC-07", "UC-08", "UC-09"):
        assert use_case_id in text


def test_s237_catalog_contains_m5_validation_fields() -> None:
    text = Path("docs/use-cases/M5-use-case-catalog.md").read_text(encoding="utf-8")
    for field in (
        "business question",
        "canonical concepts",
        "canonical predicates",
        "path query",
        "explicit constraints",
        "expected result",
        "evidence requirements",
        "explanation requirements",
        "confidence factors",
        "semantic-gap classification",
    ):
        assert field in text
