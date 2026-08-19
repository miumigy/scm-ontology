from pathlib import Path

DOC = Path("docs/history/phase8/S309-operational-readiness-contract.md")


def test_s309_requires_traceability_and_explicit_outcomes() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Every governed operation MUST expose enough metadata",
        "Operational records MUST remain linked to the historical records they describe",
        "Operations MUST expose explicit outcomes",
        "Unknown, partial, failed, conflicted, stale, or unsupported outcomes MUST NOT be represented as successful",
    ):
        assert phrase in text


def test_s309_requires_idempotency_replay_and_audit() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Governed application operations MUST define an idempotency identity",
        "MUST NOT create unintended duplicate Fact Versions or materializations",
        "Replay MUST use retained historical inputs",
        "Changed preconditions MUST cause explicit re-evaluation",
        "Audit records MUST be append-only for governed decisions",
    ):
        assert phrase in text


def test_s309_protects_failure_recovery_and_scope() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Failures MUST remain observable",
        "Recovery MUST be an explicit governed operation",
        "Retries MUST NOT silently broaden scope",
        "Partial execution MUST identify completed and incomplete portions",
        "Every operation that can mutate Canonical Truth MUST pass through an explicit governed application boundary",
        "No operational mechanism may infer authorization or scope from mapping similarity",
    ):
        assert phrase in text


def test_s309_defines_m8_readiness_gate() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "traceable execution identity and provenance",
        "idempotent application behavior",
        "replayable historical execution",
        "preserved Fact Version and projection lineage",
        "explicit scope and authorization boundaries",
        "preservation of the Canonical mutation boundary",
        "conformance with the preceding M8 contracts",
    ):
        assert phrase in text
