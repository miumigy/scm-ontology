from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.decision_inbox import (
    InboxDecision,
    InboxError,
    build_decision_inbox,
)
from scm_ontology.distribution_application import (
    DistributionObservation,
    run_distribution_application,
)
from scm_ontology.replenishment_application import (
    ReplenishmentObservation,
    run_replenishment_application,
)


def decision_args(**overrides):
    args = dict(
        context_id="ctx-inbox",
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-18T12:00:00Z",
        dry_ran_at="2026-08-18T12:00:01Z",
    )
    args.update(overrides)
    return args


def actionable_decision(**overrides):
    args = decision_args()
    args.update(overrides)
    return run_replenishment_application(
        ReplenishmentObservation(
            product_id="P-1", location_id="WH-1", on_hand=5.0,
            reorder_point=10.0, reorder_quantity=25.0,
            evidence_ids=("e1", "e2"), provenance_ids=("p1",),
        ),
        command_id="cmd-r",
        **{k: v for k, v in args.items() if k != "command_id"},
    )


def no_action_decision(**overrides):
    args = decision_args()
    args.update(overrides)
    return run_distribution_application(
        DistributionObservation(
            shipment_id="S", item_id="I", required_quantity=120.0, capacity=100.0,
            origin_location_id="WH", destination_location_id="DC",
            evidence_ids=("e3",), provenance_ids=("p3",),
        ),
        command_id="cmd-d",
        **{k: v for k, v in args.items() if k != "command_id"},
    )


def entries():
    return (
        InboxDecision(actionable_decision(), "dec-1"),
        InboxDecision(no_action_decision(), "dec-2", reviewed=True),
    )


def inbox_args(**overrides):
    args = dict(viewed_at="2026-08-18T12:00:05Z", viewer_actor_id="operator-1")
    args.update(overrides)
    return args


def inbox(**overrides):
    return build_decision_inbox(entries(), **inbox_args(**overrides))


def test_inbox_version_and_label():
    result = inbox()
    m = result.to_mapping()
    assert m["contract_version"] == "P6B.1"
    assert m["is_decision_inbox"] is True
    assert m["viewer_actor_id"] == "operator-1"


def test_actionable_item_exposes_full_chain():
    result = inbox()
    item = result.items[0]
    assert item.status == "dry_run"
    assert item.application == "replenishment"
    assert item.action == "replenish"
    assert item.context_id == "ctx-inbox"
    assert item.actor_id == "planner-1"
    assert item.authority == "supply-chain-manager"
    assert item.authorized_at == "2026-08-18T12:00:00Z"
    assert item.command_id == "cmd-r"
    assert item.command_type == "replenishment"
    assert item.evidence_ids == ("e1", "e2")
    assert item.provenance_ids == ("p1",)
    assert item.dry_run_result_id
    assert item.reviewed is False


def test_no_action_item_has_no_command_or_authorization():
    result = inbox()
    item = result.items[1]
    assert item.status == "no_action"
    assert item.application == "distribution"
    assert item.action == "escalate"
    assert item.context_id is None
    assert item.actor_id is None
    assert item.command_id is None
    assert item.evidence_ids == ()
    assert item.reviewed is True


def test_summary_counts():
    result = inbox()
    s = result.to_mapping()["summary"]
    assert s["item_count"] == 2
    assert s["actionable_count"] == 1
    assert s["no_action_count"] == 1
    assert s["reviewed_count"] == 1
    assert s["unreviewed_count"] == 1


def test_inbox_is_deterministic_and_content_addressed():
    a = inbox()
    b = inbox()
    assert a.to_json() == b.to_json()
    assert a.inbox_id == b.inbox_id
    c = inbox(**(inbox_args() | {"viewed_at": "2026-08-18T13:00:00Z"}))
    assert a.inbox_id != c.inbox_id


def test_inbox_is_immutable():
    result = inbox()
    with pytest.raises(FrozenInstanceError):
        result.viewed_at = "mutated"


def test_evidence_is_projected_without_recomputing():
    result = inbox()
    # The decision was already run; the inbox only reads its artifacts.
    item = result.items[0]
    assert ("e1", "e2") == item.evidence_ids
    assert ("p1",) == item.provenance_ids


def test_rejects_empty_entries():
    with pytest.raises(InboxError, match="decisions must not be empty"):
        build_decision_inbox((), **inbox_args())


def test_rejects_duplicate_decision_ids():
    dup = entries()[0]
    with pytest.raises(InboxError, match="decision ids must be unique"):
        build_decision_inbox((dup, dup), **inbox_args())


def test_rejects_blank_viewed_at():
    with pytest.raises(InboxError, match="viewed_at"):
        build_decision_inbox(entries(), **inbox_args(viewed_at=""))


def test_rejects_blank_viewer():
    with pytest.raises(InboxError, match="viewer_actor_id"):
        build_decision_inbox(entries(), **inbox_args(viewer_actor_id=""))


def test_inbox_decision_rejects_blank_id():
    with pytest.raises(InboxError, match="decision_id"):
        InboxDecision(actionable_decision(), " ")


def test_inbox_decision_rejects_unsupported_type():
    with pytest.raises(InboxError, match="unsupported decision artifact"):
        InboxDecision(object(), "dec-1")


def test_inbox_decision_rejects_non_bool_reviewed():
    with pytest.raises(InboxError, match="reviewed must be a bool"):
        InboxDecision(actionable_decision(), "dec-1", reviewed="yes")


def test_non_empty_decisions_with_no_action_only():
    result = build_decision_inbox(
        (InboxDecision(no_action_decision(), "dec-2"),), **inbox_args()
    )
    assert result.to_mapping()["summary"]["actionable_count"] == 0
    assert result.to_mapping()["summary"]["no_action_count"] == 1
