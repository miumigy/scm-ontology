import pytest

from scm_ontology.phase7_acceptance import (
    Phase7AcceptanceError,
    run_phase7_acceptance,
)


def test_phase7_acceptance_passes_all_capabilities():
    report = run_phase7_acceptance(accepted_at="2026-08-19T11:00:00Z")
    assert report.accepted is True
    assert report.summary.capability_count == 5
    assert report.summary.operable_count == 5
    assert report.summary.failed_count == 0


def test_phase7_acceptance_covers_all_five_slices():
    report = run_phase7_acceptance(accepted_at="2026-08-19T11:00:00Z")
    keys = {cap.key for cap in report.capabilities}
    assert keys == {
        "reference_data_adapter",
        "mapping_canonicalization",
        "identity_resolution",
        "data_quality_freshness_gate",
        "multi_source_reference_convergence",
    }
    assert all(cap.operable for cap in report.capabilities)


def test_phase7_report_is_deterministic_and_replayable():
    first = run_phase7_acceptance(accepted_at="2026-08-19T11:00:00Z")
    second = run_phase7_acceptance(accepted_at="2026-08-19T11:00:00Z")
    assert first.to_json() == second.to_json()
    assert first.report_id == second.report_id


def test_phase7_report_serializes_with_contract_version():
    report = run_phase7_acceptance(accepted_at="2026-08-19T11:00:00Z")
    mapping = report.to_mapping()
    assert mapping["contract_version"] == "P7F.1"
    assert mapping["is_phase7_acceptance"] is True
    assert mapping["accepted"] is True


def test_phase7_acceptance_fails_closed_on_blank_accepted_at():
    with pytest.raises(Phase7AcceptanceError, match="accepted_at"):
        run_phase7_acceptance(accepted_at="  ")
