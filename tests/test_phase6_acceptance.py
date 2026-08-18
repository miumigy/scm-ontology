from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.phase6_acceptance import (
    Phase6AcceptanceError,
    CapabilityResult,
    run_phase6_acceptance,
)


def report(**overrides):
    args = dict(accepted_at="2026-08-18T16:00:05Z")
    args.update(overrides)
    return run_phase6_acceptance(**args)


def test_report_versioned_and_labeled():
    r = report()
    m = r.to_mapping()
    assert m["contract_version"] == "P6F.1"
    assert m["is_phase6_acceptance"] is True


def test_phase_is_accepted_when_all_operable():
    r = report()
    assert r.accepted is True
    m = r.to_mapping()
    assert m["summary"]["capability_count"] == 6
    assert m["summary"]["operable_count"] == 6
    assert m["summary"]["failed_count"] == 0


def test_capabilities_span_all_phase6_surfaces():
    r = report()
    keys = [c.key for c in r.capabilities]
    assert "cockpit" in keys
    assert "decision_inbox" in keys
    assert "simulation_optimization_workspace" in keys
    assert "execution_workspace" in keys
    assert "control_plane_e2e" in keys
    assert "governed_application" in keys


def test_each_capability_has_evidence_id():
    r = report()
    for cap in r.capabilities:
        assert cap.operable is True
        assert len(cap.evidence_id) == 64
        assert cap.error is None


def test_report_is_deterministic_and_content_addressed():
    a = report()
    b = report()
    assert a.to_json() == b.to_json()
    assert a.report_id == b.report_id
    c = report(accepted_at="2026-08-18T17:00:00Z")
    assert a.report_id != c.report_id


def test_report_is_immutable():
    r = report()
    with pytest.raises(FrozenInstanceError):
        r.accepted_at = "mutated"


def test_rejects_blank_accepted_at():
    with pytest.raises(Phase6AcceptanceError, match="accepted_at"):
        run_phase6_acceptance(accepted_at="   ")


def test_capability_result_is_immutable():
    cap = CapabilityResult(key="k", name="n", operable=True, evidence_id="x")
    with pytest.raises(FrozenInstanceError):
        cap.operable = False
