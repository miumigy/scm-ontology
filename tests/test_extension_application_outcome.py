from scm_ontology.extension_application_outcome import (
    ExtensionApplicationOutcomeKind,
    rejected_application,
    rolled_back_application,
)


def test_rejection_is_explicit_and_reasoned() -> None:
    outcome = rejected_application("reason:integrity")
    assert outcome.kind is ExtensionApplicationOutcomeKind.REJECTED
    assert outcome.reason_ref == "reason:integrity"
    assert outcome.transaction_ref is None


def test_rollback_preserves_transaction_reference() -> None:
    outcome = rolled_back_application("reason:failure", "transaction:1")
    assert outcome.kind is ExtensionApplicationOutcomeKind.ROLLED_BACK
    assert outcome.reason_ref == "reason:failure"
    assert outcome.transaction_ref == "transaction:1"
