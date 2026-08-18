import io
from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.demand_supply_gap import (
    DemandSupplyRecord,
    resolve_demand_supply_gap,
)
from scm_ontology.operational_workflow import (
    OperationalStep,
    run_operational_workflow,
)
from scm_ontology.production_application import (
    ProductionObservation,
    run_production_application,
)
from scm_ontology.scm_os_cockpit import (
    CockpitError,
    CockpitFixture,
    CockpitState,
    build_cockpit_state,
    make_cockpit_handler,
    run_cockpit_reference_path,
)
from scm_ontology.replenishment_application import (
    ReplenishmentObservation,
    run_replenishment_application,
)


def run_args(**overrides):
    args = dict(
        context_id="ctx-cockpit",
        recorded_at="2026-08-18T12:00:00Z",
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-18T12:00:00Z",
        dry_ran_at="2026-08-18T12:00:00Z",
    )
    args.update(overrides)
    return args


def fixture(**overrides):
    args = run_args()
    args.update(overrides)
    decision_kwargs = {k: v for k, v in args.items() if k != "recorded_at"}
    decision_r = run_replenishment_application(
        ReplenishmentObservation(
            product_id="P-1", location_id="WH-1", on_hand=5.0,
            reorder_point=10.0, reorder_quantity=25.0,
            evidence_ids=("e1",), provenance_ids=("p1",),
        ),
        command_id="cmd-r",
        **{k: v for k, v in decision_kwargs.items() if k != "command_id"},
    )
    decision_p = run_production_application(
        ProductionObservation(
            resource_id="LINE-1", required=80.0, capacity=100.0,
            evidence_ids=("e2",), provenance_ids=("p2",),
        ),
        command_id="cmd-p",
        **{k: v for k, v in decision_kwargs.items() if k != "command_id"},
    )
    gaps = resolve_demand_supply_gap(
        (
            DemandSupplyRecord(
                item_id="A-100", quantity=120.0, kind="demand", unit="unit",
                period_start="2026-08-18", period_end="2026-08-18",
                evidence_id="e1", provenance_id="p1",
            ),
            DemandSupplyRecord(
                item_id="A-100", quantity=90.0, kind="supply", unit="unit",
                period_start="2026-08-18", period_end="2026-08-18",
                evidence_id="e2", provenance_id="p2",
            ),
        )
    )
    workflow = run_operational_workflow(
        (
            OperationalStep(step_id="w1", application="replenishment", command_id="cmd-r", decision=decision_r),
            OperationalStep(step_id="w2", application="production", command_id="cmd-p", decision=decision_p),
        ),
        workflow_id="wf-fixture", recorded_at=args["recorded_at"], actor_id=args["actor_id"],
    )
    base = dict(
        context_id=args["context_id"],
        recorded_at=args["recorded_at"],
        actor_id=args["actor_id"],
        decisions=(decision_r, decision_p),
        gaps=gaps,
        workflow=workflow,
    )
    base.update(overrides)
    return CockpitFixture(**base)


def state(**overrides):
    return build_cockpit_state(fixture(**overrides))


# ---------------------------------------------------------------------------
# State construction
# ---------------------------------------------------------------------------


def test_state_is_versioned_and_operational_tool():
    st = state()
    m = st.to_mapping()
    assert m["contract_version"] == "P6A.1"
    assert m["is_operational_tool"] is True
    assert m["context_id"] == "ctx-cockpit"


def test_state_exposes_all_domains():
    st = state()
    m = st.to_mapping()["domains"]
    assert set(m.keys()) == {"decisions", "exceptions", "simulation", "execution", "governance"}
    assert len(m["decisions"]) == 2
    assert len(m["exceptions"]) == 1
    assert len(m["execution"]) == 4  # 2 dry runs + 2 workflow command states
    assert len(m["governance"]) == 2


def test_overview_counts():
    st = state()
    o = st.to_mapping()["overview"]
    assert o["decision_count"] == 2
    assert o["actionable_decisions"] == 2
    assert o["exception_count"] == 1
    assert o["workflow_steps"] == 2
    assert o["execution_dry_runs"] == 2
    assert o["governance_audits"] == 2
    assert o["governance_in_dry_run"] == 2


def test_state_is_deterministic_and_content_addressed():
    a = state()
    b = state()
    assert a.to_json() == b.to_json()
    assert a.snapshot_id == b.snapshot_id
    c = state(recorded_at="2026-08-18T13:00:00Z")
    assert a.snapshot_id != c.snapshot_id


def test_state_is_immutable():
    st = state()
    with pytest.raises(FrozenInstanceError):
        st.context_id = "mutated"


def test_reference_path_populates_every_domain():
    st = run_cockpit_reference_path()
    m = st.to_mapping()
    assert m["snapshot_id"]
    assert m["overview"]["decision_count"] == 2
    assert m["overview"]["exception_count"] == 1
    assert m["overview"]["simulation_steps"] == 2
    assert m["overview"]["workflow_steps"] == 2
    assert m["overview"]["governance_audits"] == 2
    assert m["overview"]["governance_in_dry_run"] == 2


def test_reference_path_is_deterministic():
    a = run_cockpit_reference_path()
    b = run_cockpit_reference_path()
    assert a.to_json() == b.to_json()


# ---------------------------------------------------------------------------
# Fail-closed validation
# ---------------------------------------------------------------------------


def test_fixture_rejects_blank_context():
    with pytest.raises(CockpitError, match="context_id"):
        CockpitFixture(context_id="", recorded_at="T", actor_id="a")


def test_fixture_rejects_unsupported_decision():
    with pytest.raises(CockpitError, match="unsupported decision artifact"):
        CockpitFixture(context_id="c", recorded_at="T", actor_id="a", decisions=(object(),))


def test_fixture_rejects_non_gap_exception():
    with pytest.raises(CockpitError, match="DemandSupplyGap"):
        CockpitFixture(context_id="c", recorded_at="T", actor_id="a", gaps=(object(),))


def test_build_rejects_non_fixture():
    with pytest.raises(CockpitError, match="must be a CockpitFixture"):
        build_cockpit_state(object())


def test_unknown_domain_json_rejected():
    st = state()
    with pytest.raises(CockpitError, match="unknown domain"):
        st.domain_json("bogus")


# ---------------------------------------------------------------------------
# HTTP adapter (handler-level, no port binding / side effects)
# ---------------------------------------------------------------------------


class _FakeSocket:
    def __init__(self, request_bytes: bytes) -> None:
        self._request = io.BytesIO(request_bytes)
        self.wbuffer = io.BytesIO()

    def sendall(self, data: bytes) -> None:
        self.wbuffer.write(data)

    def makefile(self, mode: str, *args, **kwargs):
        if "r" in mode:
            return self._request
        return self.wbuffer


def _get(handler_cls, path: str, method: str = "GET"):
    request = f"{method} {path} HTTP/1.1\r\nHost: cockpit\r\n\r\n".encode()
    sock = _FakeSocket(request)
    # BaseHTTPRequestHandler.__init__ handles the first request automatically.
    handler_cls(sock, ("127.0.0.1", 0), None)
    sock.wbuffer.seek(0)
    raw = sock.wbuffer.read().decode("utf-8", "replace")
    head, _, body = raw.partition("\r\n\r\n")
    status = head.splitlines()[0]
    return status, body


def _state_handler():
    return make_cockpit_handler(state())


def test_http_index_returns_html():
    status, body = _get(_state_handler(), "/")
    assert "200" in status
    assert body.startswith("<!doctype html>")
    assert "SCM OS Cockpit" in body
    assert "P6A.1" in body


def test_http_state_json():
    status, body = _get(_state_handler(), "/api/state")
    assert "200" in status
    import json
    payload = json.loads(body)
    assert payload["contract_version"] == "P6A.1"
    assert payload["is_operational_tool"] is True


def test_http_domain_endpoints():
    for domain, checks in [
        ("decisions", 2),
        ("exceptions", 1),
        ("simulation", 0),
        ("execution", 4),
        ("governance", 2),
    ]:
        status, body = _get(_state_handler(), f"/api/{domain}")
        assert "200" in status, domain
        import json
        assert len(json.loads(body)) == checks


def test_http_unknown_route_404():
    status, _ = _get(_state_handler(), "/api/bogus")
    assert "404" in status


def test_http_post_is_method_not_allowed():
    status, _ = _get(_state_handler(), "/api/state", method="POST")
    assert "405" in status


def test_http_handler_rejects_non_state():
    with pytest.raises(CockpitError, match="must be a CockpitState"):
        make_cockpit_handler(object())


# ---------------------------------------------------------------------------
# Side-effect freedom
# ---------------------------------------------------------------------------


def test_http_read_only_no_side_effect(tmp_path):
    sentinel = tmp_path / "side-effect"
    assert not sentinel.exists()
    _get(_state_handler(), "/api/state")
    _get(_state_handler(), "/")
    assert not sentinel.exists()
    assert set(tmp_path.iterdir()) == set()
