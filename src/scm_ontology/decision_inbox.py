"""SCM OS Decision Inbox (Phase 6, P6-B).

An operator-facing inbox to *inspect* each governed decision's full
inspectable surface — proposal, rationale, evidence, provenance, authorization
status, and command state — without recomputing or re-running the decision.

P6-B composes the already-produced R5 decision results (S358-S362) and the
governed decision chain they carry (a ``GovernedExecutionResult`` wrapping the
S348 ``DecisionRuntimeResult``). It projects each into an immutable,
deterministic, JSON-safe ``InboxItem`` and folds them into a content-addressed
``DecisionInbox`` with an inbox summary.

P6-B never re-derives a decision, never mutates Canonical Truth, and performs
no external side effect. It is a read-only projection for operators.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Iterable

from .distribution_application import DistributionDecision
from .procurement_application import ProcurementDecision
from .production_application import ProductionDecision
from .replenishment_application import ReplenishmentDecision


class InboxError(ValueError):
    """Raised when a decision-inbox input or invocation is invalid."""


_R5_DECISION_TYPES = (
    ReplenishmentDecision,
    ProcurementDecision,
    ProductionDecision,
    DistributionDecision,
)

_APPLICATION_BY_TYPE: dict[type, str] = {
    ReplenishmentDecision: "replenishment",
    ProcurementDecision: "procurement",
    ProductionDecision: "production",
    DistributionDecision: "distribution",
}

# Known fields expected on every signed R5 decision.
_DECISION_FIELDS = ("action", "rationale")


@dataclass(frozen=True)
class InboxDecision:
    """One governed R5 decision offered to the operator inbox.

    ``decision_id`` is the stable item id; ``reviewed`` is a stateless
    operator-supplied flag (the inbox itself records no mutable read state).
    """

    decision: Any
    decision_id: str
    reviewed: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.decision_id, str) or not self.decision_id.strip():
            raise InboxError("decision_id must be non-empty")
        if not isinstance(self.reviewed, bool):
            raise InboxError("reviewed must be a bool")
        if not isinstance(self.decision, _R5_DECISION_TYPES):
            raise InboxError(
                f"unsupported decision artifact: {type(self.decision).__name__}"
            )
        for field in _DECISION_FIELDS:
            value = getattr(self.decision, field, None)
            if not isinstance(value, str) or not value.strip():
                raise InboxError(
                    f"decision '{self.decision_id}' must expose a non-empty {field}"
                )


@dataclass(frozen=True)
class InboxItem:
    """Immutable inspectable record for one governed decision."""

    decision_id: str
    application: str
    action: str
    rationale: str
    status: str
    context_id: str | None
    actor_id: str | None
    authority: str | None
    authorized_at: str | None
    command_id: str | None
    command_type: str | None
    evidence_ids: tuple[str, ...]
    provenance_ids: tuple[str, ...]
    dry_run_result_id: str | None
    reviewed: bool

    def to_mapping(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "decision_id": self.decision_id,
            "application": self.application,
            "action": self.action,
            "rationale": self.rationale,
            "status": self.status,
            "reviewed": self.reviewed,
            "evidence_ids": list(self.evidence_ids),
            "provenance_ids": list(self.provenance_ids),
        }
        for name in (
            "context_id", "actor_id", "authority", "authorized_at",
            "command_id", "command_type", "dry_run_result_id",
        ):
            value2 = getattr(self, name)
            if value2 is not None:
                value[name] = value2
        return value


@dataclass(frozen=True)
class InboxSummary:
    """Deterministic aggregate counts across a decision inbox."""

    item_count: int
    actionable_count: int
    no_action_count: int
    reviewed_count: int
    unreviewed_count: int

    def to_mapping(self) -> dict[str, Any]:
        return {
            "item_count": self.item_count,
            "actionable_count": self.actionable_count,
            "no_action_count": self.no_action_count,
            "reviewed_count": self.reviewed_count,
            "unreviewed_count": self.unreviewed_count,
        }


def _governed_fields(governed: Any) -> dict[str, Any]:
    """Read the governed decision-chain fields without re-running anything."""
    result = governed.decision                    # DecisionRuntimeResult
    command = result.execution_command            # ExecutionCommand
    auth = command.decision                       # AuthorizedDecision
    output = auth.proposal.output                 # ReasoningOutput
    return {
        "context_id": result.context_id,
        "actor_id": auth.actor_id,
        "authority": auth.authority,
        "authorized_at": auth.authorized_at,
        "command_id": command.command_id,
        "command_type": command.command_type,
        "evidence_ids": tuple(sorted(set(output.evidence_ids))),
        "provenance_ids": tuple(sorted(set(output.provenance_ids))),
        "dry_run_result_id": governed.dry_run.result_id,
    }


def _project(entry: InboxDecision) -> InboxItem:
    """Project one InboxDecision into an immutable InboxItem."""
    decision = entry.decision
    governed = getattr(decision, "governed", None)

    application = _APPLICATION_BY_TYPE[type(decision)]
    action = decision.action
    rationale = decision.rationale

    if governed is None:
        return InboxItem(
            decision_id=entry.decision_id,
            application=application,
            action=action,
            rationale=rationale,
            status="no_action",
            context_id=None,
            actor_id=None,
            authority=None,
            authorized_at=None,
            command_id=None,
            command_type=None,
            evidence_ids=(),
            provenance_ids=(),
            dry_run_result_id=None,
            reviewed=entry.reviewed,
        )

    fields = _governed_fields(governed)
    return InboxItem(
        decision_id=entry.decision_id,
        application=application,
        action=action,
        rationale=rationale,
        status="dry_run",
        context_id=fields["context_id"],
        actor_id=fields["actor_id"],
        authority=fields["authority"],
        authorized_at=fields["authorized_at"],
        command_id=fields["command_id"],
        command_type=fields["command_type"],
        evidence_ids=fields["evidence_ids"],
        provenance_ids=fields["provenance_ids"],
        dry_run_result_id=fields["dry_run_result_id"],
        reviewed=entry.reviewed,
    )


@dataclass(frozen=True)
class DecisionInbox:
    """Immutable, content-addressed decision inbox."""

    inbox_id: str
    viewed_at: str
    viewer_actor_id: str
    items: tuple[InboxItem, ...]
    summary: InboxSummary

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P6B.1",
            "is_decision_inbox": True,
            "inbox_id": self.inbox_id,
            "viewed_at": self.viewed_at,
            "viewer_actor_id": self.viewer_actor_id,
            "summary": self.summary.to_mapping(),
            "items": [item.to_mapping() for item in self.items],
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _inbox_id(
    items: tuple[InboxItem, ...], viewed_at: str, viewer_actor_id: str
) -> str:
    payload = {
        "viewed_at": viewed_at,
        "viewer_actor_id": viewer_actor_id,
        "items": [item.to_mapping() for item in items],
    }
    return sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _summary(items: tuple[InboxItem, ...]) -> InboxSummary:
    actionable = sum(1 for item in items if item.status == "dry_run")
    no_action = sum(1 for item in items if item.status == "no_action")
    reviewed = sum(1 for item in items if item.reviewed)
    return InboxSummary(
        item_count=len(items),
        actionable_count=actionable,
        no_action_count=no_action,
        reviewed_count=reviewed,
        unreviewed_count=len(items) - reviewed,
    )


def build_decision_inbox(
    decisions: Iterable[InboxDecision],
    *,
    viewed_at: str,
    viewer_actor_id: str,
) -> DecisionInbox:
    """Build an immutable decision inbox without recomputing any decision."""
    if not isinstance(viewed_at, str) or not viewed_at.strip():
        raise InboxError("viewed_at must be non-empty")
    if not isinstance(viewer_actor_id, str) or not viewer_actor_id.strip():
        raise InboxError("viewer_actor_id must be non-empty")

    try:
        entries = tuple(decisions)
    except TypeError as exc:
        raise InboxError("decisions must be iterable") from exc
    if not entries:
        raise InboxError("decisions must not be empty")
    for entry in entries:
        if not isinstance(entry, InboxDecision):
            raise InboxError("every decision must be an InboxDecision")

    decision_ids = [entry.decision_id for entry in entries]
    if len(decision_ids) != len(set(decision_ids)):
        raise InboxError("decision ids must be unique within the inbox")

    items = tuple(_project(entry) for entry in entries)
    return DecisionInbox(
        inbox_id=_inbox_id(items, viewed_at, viewer_actor_id),
        viewed_at=viewed_at,
        viewer_actor_id=viewer_actor_id,
        items=items,
        summary=_summary(items),
    )
