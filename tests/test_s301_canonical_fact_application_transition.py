from pathlib import Path

DOC = Path("docs/milestones/S301-canonical-fact-application-transition-contract.md")


def test_s301_requires_governed_application_preconditions() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "A Fact Application MUST reference an explicit governed Write Intent",
        "The Write Intent MUST identify the target Canonical Fact",
        "governing decision, authorization, provenance, evidence, and idempotency context",
        "Application MUST validate the expected current version/state",
        "A stale, conflicting, unauthorized, or incomplete Write Intent MUST NOT produce a Canonical Fact mutation",
    ):
        assert phrase in text


def test_s301_preserves_version_lineage_and_lifecycle() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "A successful application MUST create a new attributable Fact Version",
        "The new Fact Version MUST preserve lineage to the prior version",
        "The prior version MUST remain historically retrievable",
        "A version transition MUST NOT overwrite the prior version's historical content",
        "The resulting lifecycle state MUST be explicit and valid under S300",
        "Supersession MUST explicitly reference the version it supersedes",
        "Invalidation, retirement, dispute, and deferral MUST remain distinguishable from successful activation",
    ):
        assert phrase in text


def test_s301_requires_observable_outcomes_and_idempotency() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "`applied`, `rejected`, `deferred`, `conflict`, `stale`, or `failed`",
        "An `applied` outcome MUST reference the resulting Fact Version",
        "A `rejected`, `deferred`, `conflict`, `stale`, or `failed` outcome MUST NOT be represented as an applied Canonical mutation",
        "Partial execution MUST remain observable",
        "Repeated application of the same accepted Write Intent MUST resolve to the same governed application outcome",
        "MUST NOT create unintended duplicate Fact Versions",
        "A replay against a changed current version MUST re-evaluate preconditions",
    ):
        assert phrase in text


def test_s301_preserves_audit_and_blocks_implicit_application() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Application History MUST be append-only",
        "Historical application outcomes and Fact Versions MUST NOT be silently rewritten",
        "Current Canonical Truth MUST remain reconstructable",
        "Identity Resolution, Conflict Resolution, Mapping, Reasoning, semantic similarity, evidence evaluation, or replay MUST NOT directly perform Fact Application",
        "Only the explicit governed application step MAY create a new Canonical Fact Version or lifecycle transition",
    ):
        assert phrase in text
