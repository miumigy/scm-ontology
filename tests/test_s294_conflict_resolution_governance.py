from pathlib import Path

DOC = Path("docs/milestones/S294-conflict-resolution-governance-contract.md")


def test_s294_requires_resolution_governance_context() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "immutable Conflict Record",
        "governing Decision",
        "evidence and provenance considered",
        "affected source identities",
        "intended resolution outcome",
        "authorization or policy context",
    ):
        assert phrase in text


def test_s294_protects_canonical_truth() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "MUST NOT create a new canonical entity, attribute, or predicate automatically as a conflict-resolution side effect",
        "MUST NOT mutate canonical facts implicitly",
        "MUST NOT silently select a conflicting value as Canonical Truth",
        "MUST NOT silently discard unresolved evidence, provenance, or competing interpretations",
        "Conflicts MUST remain observable after resolution",
        "Unresolved identity MUST remain a valid outcome",
        "Reasoning MUST remain read-only until explicit governed Application",
        "MUST NOT expand the scope of the original Application implicitly",
    ):
        assert phrase in text


def test_s294_preserves_resolution_history_and_replay() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "accepted, rejected, unresolved, superseded, or deferred",
        "MUST NOT be treated as an implicit Canonical mutation",
        "MUST expose that drift",
        "Conflict Records and Resolution Records MUST be append-only",
        "MUST NOT silently rewrite historical conflict or resolution decisions",
        "Resolution execution MUST be replayable",
        "MUST preserve historical records",
    ):
        assert phrase in text
