from pathlib import Path


def test_s247_reports_all_m5_use_cases() -> None:
    text = Path("docs/history/phase5/M5-validation-report.md").read_text(encoding="utf-8")
    for use_case in (
        "UC-01 Supply Dependency",
        "UC-02 Site Dependency",
        "UC-03 Material Flow",
        "UC-04 Inventory Dependency",
        "UC-05 Capacity Dependency",
        "UC-06 Lead-Time Dependency",
        "UC-07 Supply Risk",
        "UC-08 Demand / Supply Alignment",
        "UC-09 Enterprise Mapping",
    ):
        assert use_case in text


def test_s247_marks_m5_complete_and_points_to_m6() -> None:
    text = Path("docs/history/phase5/M5-validation-report.md").read_text(encoding="utf-8")
    assert "M5 is functionally complete" in text
    assert "M6 — SCM Graph Integration" in text
    assert "Enterprise Data" in text
    assert "Canonical SCM Graph" in text
