from pathlib import Path

DOC = Path("docs/history/phase8/S291-identity-resolution-application-contract.md")


def test_s291_requires_governed_application_inputs() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "identity-resolution Decision",
        "evidence and provenance",
        "source identities in scope",
        "governing policy or authorization context",
        "intended Canonical Identity change",
    ):
        assert phrase in text


def test_s291_protects_canonical_semantics() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "MUST NOT create a new canonical entity, attribute, or predicate automatically outside the governed Application",
        "MUST NOT mutate canonical facts implicitly",
        "MUST NOT infer Canonical Truth from application success alone",
        "Conflicts MUST remain observable",
        "Source identity and provenance MUST remain attached",
        "Semantic Gap and unresolved identity MUST remain first-class outcomes",
        "Reasoning MUST remain read-only",
    ):
        assert phrase in text


def test_s291_preserves_application_history_and_replay() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Application Records MUST be append-only",
        "MUST NOT silently rewrite the historical application decision",
        "Application execution MUST be replayable",
        "Replay MUST produce a distinct result",
    ):
        assert phrase in text
