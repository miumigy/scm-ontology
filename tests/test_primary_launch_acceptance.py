import pytest

from scm_ontology.primary_launch import (
    PrimaryLaunchError,
    run_primary_launch,
)
from scm_ontology.primary_launch_acceptance import (
    PrimaryLaunchAcceptanceError,
    PrimaryLaunchAcceptanceReport,
    run_primary_launch_acceptance,
)


def test_primary_launch_golden_path_accepted():
    result = run_primary_launch(
        context_id="launch",
        operator_id="operator-launch",
        authority="scm-os-reference",
        observed_at="2026-08-19T10:00:00Z",
    )
    assert result.accepted is True
    assert result.summary.step_count == 11
    assert result.summary.ok_count == 11
    assert result.ontology_release == "SCM Ontology v0.1"
    assert result.os_release == "SCM OS Reference v0.1"


def test_primary_launch_golden_path_is_deterministic():
    a = run_primary_launch(
        context_id="launch", operator_id="operator-launch",
        authority="scm-os-reference", observed_at="2026-08-19T10:00:00Z",
    )
    b = run_primary_launch(
        context_id="launch", operator_id="operator-launch",
        authority="scm-os-reference", observed_at="2026-08-19T10:00:00Z",
    )
    assert a.result_id == b.result_id
    assert a.to_json() == b.to_json()


def test_primary_launch_fails_closed_on_blank_scope():
    with pytest.raises(PrimaryLaunchError):
        run_primary_launch(
            context_id=" ", operator_id="operator",
            authority="scm-os-reference", observed_at="2026-08-19T10:00:00Z",
        )


def test_primary_launch_acceptance_reports_accepted():
    report = run_primary_launch_acceptance(accepted_at="2026-08-19T10:00:00Z")
    assert isinstance(report, PrimaryLaunchAcceptanceReport)
    assert report.accepted is True
    assert report.summary.item_count == 11
    assert report.summary.operable_count == 11
    assert report.summary.failed_count == 0


def test_acceptance_includes_all_checklist_keys():
    report = run_primary_launch_acceptance(accepted_at="2026-08-19T10:00:00Z")
    keys = {item.key for item in report.items}
    assert keys == {
        "architecture_coherence",
        "clean_installation",
        "golden_path_execution",
        "canonical_truth_boundary",
        "provenance_evidence",
        "governance_authorization",
        "execution_safety",
        "agent_safety",
        "replay_audit",
        "documentation",
        "ci_entry",
    }


def test_every_checklist_item_operable_with_evidence():
    report = run_primary_launch_acceptance(accepted_at="2026-08-19T10:00:00Z")
    for item in report.items:
        assert item.operable is True, item.key
        assert item.evidence_id


def test_acceptance_report_is_deterministic():
    a = run_primary_launch_acceptance(accepted_at="2026-08-19T10:00:00Z")
    b = run_primary_launch_acceptance(accepted_at="2026-08-19T10:00:00Z")
    assert a.report_id == b.report_id
    assert a.to_json() == b.to_json()
    c = run_primary_launch_acceptance(accepted_at="2026-08-19T11:00:00Z")
    assert a.report_id != c.report_id


def test_acceptance_fails_closed_on_blank_timestamp():
    with pytest.raises(PrimaryLaunchAcceptanceError):
        run_primary_launch_acceptance(accepted_at=" ")
