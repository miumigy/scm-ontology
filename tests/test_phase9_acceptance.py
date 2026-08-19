import pytest

from scm_ontology.phase9_acceptance import (
    Phase9AcceptanceError,
    Phase9AcceptanceReport,
    run_phase9_acceptance,
)


def test_phase9_acceptance_reports_accepted():
    report = run_phase9_acceptance(accepted_at="2026-08-19T10:00:00Z")
    assert isinstance(report, Phase9AcceptanceReport)
    assert report.accepted is True
    assert report.summary.capability_count == 7
    assert report.summary.operable_count == 7
    assert report.summary.failed_count == 0


def test_acceptance_includes_all_capabilities():
    report = run_phase9_acceptance(accepted_at="2026-08-19T10:00:00Z")
    keys = {cap.key for cap in report.capabilities}
    assert keys == {
        "execution_outcome_contract",
        "external_execution_adapter",
        "approval_to_execution",
        "outcome_to_event_canonicalization",
        "closed_loop_e2e",
        "failure_retry_idempotency",
        "governed_closed_loop_gate",
    }


def test_every_capability_operable():
    report = run_phase9_acceptance(accepted_at="2026-08-19T10:00:00Z")
    for cap in report.capabilities:
        assert cap.operable is True, cap.key
        assert cap.evidence_id  # content-addressed evidence for audit/replay


def test_acceptance_report_is_deterministic():
    a = run_phase9_acceptance(accepted_at="2026-08-19T10:00:00Z")
    b = run_phase9_acceptance(accepted_at="2026-08-19T10:00:00Z")
    assert a.to_json() == b.to_json()
    assert a.report_id == b.report_id
    c = run_phase9_acceptance(accepted_at="2026-08-19T11:00:00Z")
    assert a.report_id != c.report_id


def test_acceptance_fails_closed_on_blank_timestamp():
    with pytest.raises(Phase9AcceptanceError):
        run_phase9_acceptance(accepted_at=" ")
