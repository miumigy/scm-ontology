from pathlib import Path

DOC = Path("docs/history/phase8/S289-identity-resolution-evidence-contract.md")


def test_s289_requires_identity_evidence_context() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "source identity and source system",
        "evidence references",
        "matching rationale or signal description",
        "confidence or uncertainty representation",
        "provenance",
        "resolution status",
    ):
        assert phrase in text


def test_s289_prevents_evidence_from_becoming_canonical_truth() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Evidence MUST NOT by itself establish Canonical Identity",
        "MUST NOT create a new canonical entity, attribute, or predicate automatically",
        "MUST NOT mutate canonical facts implicitly",
        "MUST NOT infer Canonical Truth from confidence alone",
        "Conflicts MUST remain observable",
        "Ambiguous and unresolved identity MUST remain first-class outcomes",
    ):
        assert phrase in text


def test_s289_preserves_evidence_history() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "New or changed evidence MUST produce an observable evidence revision",
        "Historical identity-resolution evidence MUST remain append-only",
        "MUST NOT erase the provenance or decision context of the earlier record",
        "explicit governed Decision and Application step",
    ):
        assert phrase in text
