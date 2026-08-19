from pathlib import Path

DOC = Path("docs/history/phase8/S299-canonical-graph-write-governance-contract.md")


def test_s299_requires_explicit_write_intent_and_authorization() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Every Canonical Graph write MUST be represented by an explicit Write Intent",
        "governing Decision / Resolution reference",
        "authorization and scope",
        "provenance and evidence references",
        "idempotency key",
        "A Graph Write MUST require an explicit governed authorization",
        "Identity Resolution, Conflict Resolution, Mapping, Reasoning, or Provenance processing MUST NOT itself authorize a Graph Write",
        "A Write MUST be rejected when its authorization, scope, decision reference, or required evidence is missing or invalid",
    ):
        assert phrase in text


def test_s299_protects_canonical_state_and_preconditions() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "A Write MUST validate its expected current version/state before mutation",
        "A stale Write Intent MUST NOT overwrite a newer Canonical state",
        "Concurrent or conflicting state MUST remain observable",
        "Preconditions MUST be evaluated before Canonical mutation",
        "Canonical Graph mutation MUST occur only through an explicit governed application step",
        "No upstream mapping, identity match, resolution result, or reasoning output MAY implicitly mutate the Canonical Graph",
        "A Graph Write MUST NOT create a new canonical entity, attribute, or predicate unless that creation is explicitly authorized",
    ):
        assert phrase in text


def test_s299_requires_audit_idempotency_and_replay() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Before-state and intended after-state MUST be recorded",
        "Write History MUST be append-only",
        "Historical Write Records MUST NOT be silently rewritten",
        "Rejected, deferred, and failed Writes MUST remain observable and attributable",
        "Every Write MUST be idempotent under its declared idempotency key",
        "Replaying the same accepted Write Intent MUST NOT produce an unintended additional mutation",
        "Application MUST be replayable",
    ):
        assert phrase in text


def test_s299_preserves_partial_failure_and_lineage() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Partial execution MUST NOT be silently reported as successful completion",
        "Compensation or recovery MUST be an explicit governed operation",
        "MUST preserve the original Write History",
        "current Canonical state MUST remain distinguishable from historical Write Records and Fact Versions",
        "MUST NOT erase the lineage that preceded it",
    ):
        assert phrase in text
