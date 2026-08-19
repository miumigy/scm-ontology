"""P9-A — Closed-loop execution outcome contract (success / failure / partial).

Extends the S347/S348 execution-outcome foundation with an explicit outcome
contract for governed real execution: a command may produce one or more
per-target ``ResultElement`` records, each carrying its own status, evidence,
and external reference. The elements are aggregated into a phase verdict
(``success``, ``partial``, ``failure``, or ``rejected``) that preserves
provenance and evidence on the outcome record itself.

This contract performs no external side effect and never mutates Canonical
Truth. It is the deterministic, content-addressed boundary that P9-B (external
execution adapter) and P9-D (outcome-to-event canonicalization) build on.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any

from .execution_command import ExecutionCommand


class ExecutionOutcomeContractError(ValueError):
    """Raised when an execution outcome contract is invalid."""


_ELEMENT_STATUSES = frozenset({"success", "failure"})
_PHASE_STATUSES = frozenset({"success", "partial", "failure", "rejected"})


@dataclass(frozen=True)
class ResultElement:
    """Immutable outcome of a single execution target within a command."""

    target_ref: str
    status: str
    external_reference: str | None = None
    detail: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.target_ref, str) or not self.target_ref.strip():
            raise ExecutionOutcomeContractError("target_ref must be non-empty")
        if self.status not in _ELEMENT_STATUSES:
            raise ExecutionOutcomeContractError(
                "element status must be one of success, failure"
            )
        if self.external_reference is not None and not self.external_reference.strip():
            raise ExecutionOutcomeContractError(
                "external_reference must be non-empty when provided"
            )

    def to_mapping(self) -> dict[str, Any]:
        return {
            "target_ref": self.target_ref,
            "status": self.status,
            "external_reference": self.external_reference,
            "detail": self.detail,
        }


@dataclass(frozen=True)
class ExecutionOutcomeContract:
    """Immutable, content-addressed outcome record for a governed command.

    The phase verdict is derived deterministically from the element set:

    - ``success`` — every element succeeded;
    - ``partial`` — at least one element succeeded and at least one failed;
    - ``failure`` — every element failed (no element succeeded);
    - ``rejected`` — recorded when no execution was attempted (e.g. governance
      or adapter declined the command before side effects).
    """

    command: ExecutionCommand
    verdict: str
    elements: tuple[ResultElement, ...]
    outcome_id: str
    recorded_at: str
    evidence_ids: tuple[str, ...] = ()
    provenance_ids: tuple[str, ...] = ()
    detail: str | None = None

    def __post_init__(self) -> None:
        if self.verdict not in _PHASE_STATUSES:
            raise ExecutionOutcomeContractError(
                "verdict must be one of success, partial, failure, rejected"
            )
        if not isinstance(self.elements, (tuple, list)):
            raise ExecutionOutcomeContractError("elements must be a sequence")
        object.__setattr__(self, "elements", tuple(self.elements))
        if self.verdict != "rejected" and not self.elements:
            raise ExecutionOutcomeContractError(
                "elements must be non-empty unless the verdict is rejected"
            )
        if not isinstance(self.outcome_id, str) or not self.outcome_id.strip():
            raise ExecutionOutcomeContractError("outcome_id must be non-empty")
        if not isinstance(self.recorded_at, str) or not self.recorded_at.strip():
            raise ExecutionOutcomeContractError("recorded_at must be non-empty")
        if any(not value.strip() for value in self.evidence_ids):
            raise ExecutionOutcomeContractError(
                "evidence_ids must contain non-empty identifiers"
            )
        if any(not value.strip() for value in self.provenance_ids):
            raise ExecutionOutcomeContractError(
                "provenance_ids must contain non-empty identifiers"
            )
        expected = "" if self.verdict == "rejected" else _derive_verdict(self.elements)
        if self.verdict == "rejected":
            if self.elements:
                raise ExecutionOutcomeContractError(
                    "rejected verdict must have no execution elements"
                )
        elif expected != self.verdict:
            raise ExecutionOutcomeContractError(
                f"verdict {self.verdict!r} inconsistent with elements (expected {expected!r})"
            )

    @property
    def command_id(self) -> str:
        return self.command.command_id

    @property
    def context_id(self) -> str:
        return self.command.context_id

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P9A.1",
            "outcome_id": self.outcome_id,
            "command_id": self.command_id,
            "context_id": self.context_id,
            "command_type": self.command.command_type,
            "verdict": self.verdict,
            "recorded_at": self.recorded_at,
            "elements": [element.to_mapping() for element in self.elements],
            "evidence_ids": list(self.evidence_ids),
            "provenance_ids": list(self.provenance_ids),
            "detail": self.detail,
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _derive_verdict(elements: tuple[ResultElement, ...]) -> str:
    succeeded = sum(1 for element in elements if element.status == "success")
    if succeeded == 0:
        return "failure"
    if succeeded == len(elements):
        return "success"
    return "partial"


def _outcome_id(
    command: ExecutionCommand,
    verdict: str,
    elements: tuple[ResultElement, ...],
    evidence_ids: tuple[str, ...],
    provenance_ids: tuple[str, ...],
) -> str:
    canonical = {
        "command": command.to_mapping(),
        "verdict": verdict,
        "elements": [element.to_mapping() for element in elements],
        "evidence_ids": list(evidence_ids),
        "provenance_ids": list(provenance_ids),
    }
    return sha256(
        json.dumps(
            canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()


def build_execution_outcome_contract(
    command: ExecutionCommand,
    *,
    elements: tuple[ResultElement, ...] | list[ResultElement],
    recorded_at: str,
    verdict: str | None = None,
    evidence_ids: tuple[str, ...] | list[str] = (),
    provenance_ids: tuple[str, ...] | list[str] = (),
    detail: str | None = None,
) -> ExecutionOutcomeContract:
    """Build an immutable execution outcome contract for a governed command.

    The verdict is derived from the elements unless the caller explicitly
    supplies one (used for the ``rejected`` case, where no side effect was
    attempted).
    """
    if not isinstance(command, ExecutionCommand):
        raise ExecutionOutcomeContractError("command must be an ExecutionCommand")
    if not recorded_at.strip():
        raise ExecutionOutcomeContractError("recorded_at must be non-empty")

    element_tuple = tuple(elements)
    if verdict is None:
        verdict = _derive_verdict(element_tuple)
    evidence = tuple(evidence_ids)
    provenance = tuple(provenance_ids)

    return ExecutionOutcomeContract(
        command=command,
        verdict=verdict,
        elements=element_tuple,
        outcome_id=_outcome_id(command, verdict, element_tuple, evidence, provenance),
        recorded_at=recorded_at,
        evidence_ids=evidence,
        provenance_ids=provenance,
        detail=detail,
    )


def reject_execution_outcome_contract(
    command: ExecutionCommand,
    *,
    recorded_at: str,
    evidence_ids: tuple[str, ...] | list[str] = (),
    provenance_ids: tuple[str, ...] | list[str] = (),
    detail: str | None = None,
) -> ExecutionOutcomeContract:
    """Build a ``rejected`` outcome contract with no execution elements."""
    return build_execution_outcome_contract(
        command,
        elements=(),
        recorded_at=recorded_at,
        verdict="rejected",
        evidence_ids=evidence_ids,
        provenance_ids=provenance_ids,
        detail=detail,
    )
