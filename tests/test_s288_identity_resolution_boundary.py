from pathlib import Path

DOC = Path("docs/milestones/S288-m8-identity-resolution-boundary-contract.md")


def test_s288_protects_canonical_identity() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Identity similarity MUST NOT by itself establish Canonical Identity",
        "MUST NOT create a new canonical entity, attribute, or predicate automatically",
        "MUST NOT mutate canonical facts implicitly",
        "MUST NOT infer Canonical Truth from identity similarity or matching success alone",
    ):
        assert phrase in text


def test_s288_preserves_evidence_and_unresolved_outcomes() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "source identity, matching evidence, provenance, and confidence",
        "Ambiguous, conflicting, and unresolved matches MUST remain first-class outcomes",
        "Conflicts MUST remain observable",
        "Semantic Gap and unresolved identity MUST remain first-class outcomes",
        "Reasoning MUST remain read-only",
    ):
        assert phrase in text


def test_s288_requires_governed_application_and_history() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "explicit governed Decision and Application step",
        "Historical identity-resolution decisions MUST remain append-only",
        "silently rewriting history",
    ):
        assert phrase in text
