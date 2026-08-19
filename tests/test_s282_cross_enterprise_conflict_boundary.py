from pathlib import Path


DOC = Path("docs/history/phase8/S282-m8-cross-enterprise-conflict-boundary.md")


def test_s282_defines_conflict_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Conflict Set",
        "Governed Resolution Decision",
        "Canonical application (if approved)",
        "conflicting enterprise representations",
    ):
        assert phrase in text


def test_s282_preserves_conflicting_evidence() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "all materially conflicting source assertions",
        "source identity and provenance",
        "evidence references",
        "Conflicts MUST remain observable",
        "Conflicting source assertions MUST NOT be silently discarded",
        "Unresolved conflicts MUST remain first-class outcomes",
    ):
        assert phrase in text


def test_s282_forbids_implicit_resolution_and_mutation() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "MUST NOT silently select a winning source",
        "MUST NOT create a new canonical entity, attribute, or predicate automatically",
        "MUST NOT mutate canonical facts without an explicit governed application step",
        "Reasoning MUST remain read-only",
    ):
        assert phrase in text


def test_s282_is_auditable_and_replayable() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "auditable and replayable" in text
    assert "Vendor-specific conflict rules MUST remain outside the Canonical Ontology" in text
