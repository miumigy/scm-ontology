import json

import pytest

from scm_ontology.phase8_acceptance import (
    Phase8AcceptanceError,
    Phase8AcceptanceReport,
    run_phase8_acceptance,
)


def test_phase8_acceptance_accepted() -> None:
    report = run_phase8_acceptance(accepted_at="2026-08-19T00:00:00Z")
    assert isinstance(report, Phase8AcceptanceReport)
    assert report.accepted is True
    assert report.summary.capability_count == 6
    assert report.summary.operable_count == 6
    assert report.summary.failed_count == 0


def test_all_capabilities_operable_with_evidence() -> None:
    report = run_phase8_acceptance(accepted_at="2026-08-19T00:00:00Z")
    assert all(cap.operable for cap in report.capabilities)
    assert all(cap.evidence_id for cap in report.capabilities)
    # the P8-F interchangeable-backends gate is present and accepted
    gate = next(c for c in report.capabilities if c.key == "interchangeable_backends")
    assert gate.detail["accepted"] is True


def test_report_is_deterministic() -> None:
    a = run_phase8_acceptance(accepted_at="2026-08-19T00:00:00Z")
    b = run_phase8_acceptance(accepted_at="2026-08-19T00:00:00Z")
    assert a.report_id == b.report_id
    assert a.to_json() == b.to_json()


def test_report_changes_with_accepted_at() -> None:
    a = run_phase8_acceptance(accepted_at="2026-08-19T00:00:00Z")
    b = run_phase8_acceptance(accepted_at="2026-08-19T01:00:00Z")
    assert a.report_id != b.report_id


def test_report_mapping_shape() -> None:
    report = run_phase8_acceptance(accepted_at="2026-08-19T00:00:00Z")
    mapping = report.to_mapping()
    assert mapping["contract_version"] == "P8F.1"
    assert mapping["is_phase8_acceptance"] is True
    assert mapping["accepted"] is True
    assert len(mapping["capabilities"]) == 6


def test_fail_closed_on_empty_accepted_at() -> None:
    with pytest.raises(Phase8AcceptanceError, match="accepted_at"):
        run_phase8_acceptance(accepted_at="   ")
