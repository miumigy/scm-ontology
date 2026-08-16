from pathlib import Path

DOC = Path("docs/milestones/S297-multisource-identity-resolution-contract.md")


def test_s297_preserves_identity_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Source Identity and Canonical Identity MUST remain distinct concepts",
        "A Canonical Identity MUST NOT be created automatically from a successful match",
        "ambiguous`, `unresolved`, or `conflict",
        "Identity similarity, deterministic key equality, or mapping success MUST NOT by itself establish Canonical Identity",
        "Conflicting identifiers or evidence MUST remain observable",
        "Provenance MUST remain attached to the identity decision",
        "MUST NOT create a new canonical entity, attribute, or predicate automatically",
        "MUST NOT mutate Canonical facts implicitly",
        "Identity resolution MUST NOT be treated as an implicit Canonical mutation",
        "Semantic Gap and unresolved identity MUST remain observable outcomes",
    ):
        assert phrase in text


def test_s297_preserves_history_and_replay() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Identity Decisions MUST be append-only",
        "Historical Identity Decisions MUST NOT be silently rewritten",
        "a new attributable decision linked to the prior decision",
        "Identity resolution MUST be replayable",
    ):
        assert phrase in text


def test_s297_rejects_implicit_cross_source_canonicalization() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Source-specific semantics MUST NOT be promoted into Canonical semantics solely because multiple sources agree" in text
