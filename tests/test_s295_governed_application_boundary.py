from pathlib import Path

DOC = Path("docs/milestones/S295-governed-application-boundary.md")


def test_s295_requires_application_preconditions() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Resolution Record",
        "governing Decision",
        "target Canonical facts or graph scope",
        "evidence and provenance supporting the Decision",
        "authorization or policy context",
        "expected pre-application state",
        "idempotency key or equivalent replay identity",
    ):
        assert phrase in text


def test_s295_protects_explicit_canonical_application_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "A Resolution MUST NOT itself mutate Canonical facts",
        "Canonical mutation MUST occur only through an explicit governed Application step",
        "The Application scope MUST be explicit",
        "Application authorization MUST be attributable",
        "Reasoning and mapping MUST remain read-only until the Application boundary is crossed",
        "stale or conflicting state MUST cause rejection or a new governed Decision",
    ):
        assert phrase in text


def test_s295_requires_idempotent_replayable_and_auditable_execution() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Repeated submission of the same Application identity MUST NOT produce additional Canonical mutations",
        "Application execution MUST be replayable",
        "Replay MUST preserve the original Application history",
        "Partial execution MUST NOT be represented as successful completion",
        "Application history MUST be append-only",
        "Conflicts, unresolved identity, rejected Applications, and authorization failures MUST remain observable outcomes",
    ):
        assert phrase in text
