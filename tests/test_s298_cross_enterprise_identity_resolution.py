from pathlib import Path

DOC = Path("docs/history/phase8/S298-cross-enterprise-identity-resolution-contract.md")


def test_s298_preserves_enterprise_identity_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Enterprise identity scope MUST remain explicit",
        "An external identifier MUST retain its issuing enterprise and source context",
        "Cross-enterprise identity linkage MUST be attributable to an explicit governed decision",
        "A cross-enterprise match MUST NOT automatically create or mutate a Canonical Entity",
        "Identity similarity, shared identifiers, or reciprocal source agreement MUST NOT by themselves establish Canonical Identity",
        "A Canonical Identity MUST NOT be silently shared across enterprise boundaries",
        "Enterprise-specific semantics MUST NOT be promoted into Canonical semantics solely because two enterprises agree",
        "Cross-enterprise resolution MUST NOT be treated as an implicit Canonical mutation",
    ):
        assert phrase in text


def test_s298_preserves_authority_provenance_and_unresolved_outcomes() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "source identity, enterprise scope, provenance, evidence, and decision context",
        "The authority and scope under which the linkage was established MUST remain observable",
        "Evidence MUST remain distinguishable from the resulting identity decision",
        "Missing, conflicting, expired, or insufficient authority MUST produce an observable unresolved or rejected outcome",
        "ambiguous`, `unresolved`, `conflict`, and `rejected` MUST remain first-class outcomes",
    ):
        assert phrase in text


def test_s298_requires_append_only_replayable_decisions() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Cross-enterprise Identity Decisions MUST be append-only",
        "Historical cross-enterprise Identity Decisions MUST NOT be silently rewritten",
        "a new attributable decision linked to the prior decision",
        "Resolution MUST be replayable",
        "Identity resolution itself MUST NOT authorize Canonical mutation",
    ):
        assert phrase in text
