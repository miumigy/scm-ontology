from pathlib import Path

DOC = Path("docs/milestones/S292-identity-application-idempotency-contract.md")


def test_s292_defines_stable_application_identity() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "stable Application Identity",
        "governing Decision",
        "application scope",
        "target Canonical Identity",
        "intended change",
    ):
        assert phrase in text


def test_s292_protects_canonical_safety_on_retry() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "MUST NOT create a new canonical entity, attribute, or predicate automatically outside the governed Application",
        "MUST NOT mutate canonical facts implicitly",
        "MUST NOT treat retry success as evidence of new Canonical Truth",
        "Conflicts MUST remain observable",
        "Source identity and provenance MUST remain attached",
        "Semantic Gap and unresolved identity MUST remain first-class outcomes",
        "Reasoning MUST remain read-only",
        "MUST NOT silently expand the original Application scope",
    ):
        assert phrase in text


def test_s292_preserves_history_and_surfaces_drift() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "A retry MUST NOT silently execute a different Canonical change",
        "Replay MUST produce a distinct observable execution result",
        "MUST expose the drift rather than silently treating the execution as identical",
        "Application Records MUST be append-only",
        "MUST NOT be implemented by silently rewriting, deleting, or collapsing historical Application Records",
        "new governed Application Identity",
    ):
        assert phrase in text
