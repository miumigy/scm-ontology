from pathlib import Path

DOC = Path("docs/history/phase8/S290-identity-resolution-decision-contract.md")


def test_s290_requires_governed_decision_context() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "identity-resolution proposal",
        "evidence context",
        "source identity, provenance, evidence references, uncertainty",
        "governing policy or rule set",
    ):
        assert phrase in text


def test_s290_preserves_unresolved_and_conflicting_outcomes() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Unresolved and conflicting outcomes MUST remain first-class",
        "MUST NOT be coerced into acceptance",
        "MUST NOT silently resolve ambiguous mappings or identities",
        "Conflicts MUST remain observable",
    ):
        assert phrase in text


def test_s290_separates_decision_from_canonical_mutation() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Identity similarity MUST NOT by itself establish Canonical Identity",
        "Confidence MUST NOT by itself authorize Canonical Identity mutation",
        "MUST NOT create a new canonical entity, attribute, or predicate automatically",
        "MUST NOT mutate canonical facts implicitly",
        "separately governed Application step",
        "auditable application record",
    ):
        assert phrase in text


def test_s290_preserves_history_and_replayability() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Identity-resolution decisions MUST be append-only and replayable",
        "A replay MUST NOT rewrite the historical decision",
        "Differences caused by changed evidence, mappings, semantics, or governance MUST remain observable as replay drift",
    ):
        assert phrase in text
