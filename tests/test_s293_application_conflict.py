from pathlib import Path

DOC = Path("docs/milestones/S293-application-conflict-contract.md")


def test_s293_requires_observable_conflict_context() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Every material Application conflict MUST remain observable and attributable",
        "affected source identities",
        "relevant Decision and Application Identity",
        "conflicting evidence and provenance",
        "competing proposed values or identities",
        "conflict status",
        "governing context used for resolution",
    ):
        assert phrase in text


def test_s293_forbids_silent_canonical_resolution() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "MUST NOT create a new canonical entity, attribute, or predicate automatically as a conflict response",
        "MUST NOT mutate canonical facts implicitly",
        "MUST NOT silently choose one conflicting source as Canonical Truth",
        "MUST NOT silently discard conflicting evidence or provenance",
        "Conflicts MUST remain observable",
        "Ambiguous and unresolved identity MUST remain first-class outcomes",
        "Reasoning MUST remain read-only",
        "MUST NOT expand the original Application scope implicitly",
    ):
        assert phrase in text


def test_s293_preserves_conflict_history() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Conflict Records MUST be append-only",
        "MUST NOT silently rewrite the historical conflict or decision",
        "Replay MUST preserve the original conflict context",
        "MUST produce an observable result",
    ):
        assert phrase in text
