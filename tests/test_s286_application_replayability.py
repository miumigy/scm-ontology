from pathlib import Path

DOC = Path("docs/history/phase8/S286-m8-application-replayability-contract.md")


def test_s286_defines_replay_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "original Application Record",
        "governing Decision Record",
        "recorded application scope",
        "Replay MUST NOT silently broaden application scope",
    ):
        assert phrase in text


def test_s286_protects_canonical_semantics() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Replay MUST NOT create a new canonical entity, attribute, or predicate implicitly",
        "Replay MUST NOT mutate canonical facts without an explicit governed application step",
        "Replay MUST NOT infer Canonical Truth from replay success alone",
        "Conflicts MUST remain observable",
        "Semantic Gap and unresolved identity MUST remain first-class outcomes",
    ):
        assert phrase in text


def test_s286_preserves_history_and_surfaces_drift() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Changes in source data, mapping definitions, Canonical semantics, Decision status, or governance policy MUST be surfaced as replay differences",
        "Historical Application Records MUST remain append-only",
        "A replay result MUST be recorded separately from the historical Application Record",
    ):
        assert phrase in text
