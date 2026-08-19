"""P9-B — External Execution Adapter boundary with a deterministic test double.

Phase 8 closed with dry-run operations only. P9-B introduces the bounded
boundary through which a governed ``ExecutionCommand`` may actually cause side
effects in an external system (ERP / WMS / TMS / MES): an injected
``ExternalExecutionAdapter`` that performs the side effect and returns a
deterministic ``ExecutionOutcomeContract`` (P9-A).

The default ``ReferenceExternalExecutionAdapter`` is a deterministic test
double that simulates an external system against an in-memory order book and
derives its outcome entirely from the command content — so tests and the
closed-loop E2E can exercise real side effects reproducibly without any live
system. A real ERP/WMS adapter is implemented later against this same
boundary.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .execution_command import ExecutionCommand
from .execution_outcome_contract import (
    ExecutionOutcomeContract,
    ResultElement,
    build_execution_outcome_contract,
)


class ExternalExecutionError(ValueError):
    """Raised when an external execution adapter violates its boundary."""


class ExternalExecutionAdapter(Protocol):
    """Bounded boundary from a governed command to an external system.

    Implementations MAY cause real side effects inside ``execute`` (that is the
    point of this boundary), MUST be repeatable/deterministic given the command
    content, and MUST return a valid ``ExecutionOutcomeContract``. They MUST
    NOT mutate Canonical Truth directly.
    """

    adapter_id: str

    def supports(self, command_type: str) -> bool:
        """Return whether this adapter can execute commands of the given type."""
        ...

    def execute(
        self,
        command: ExecutionCommand,
        *,
        executed_at: str,
        external_system: object | None = None,
    ) -> ExecutionOutcomeContract:
        """Perform the side effect and return the deterministic outcome."""
        ...


def validate_external_adapter(adapter: object) -> None:
    """Fail closed if ``adapter`` does not satisfy the external boundary."""
    adapter_id = getattr(adapter, "adapter_id", None)
    if not isinstance(adapter_id, str) or not adapter_id.strip():
        raise ExternalExecutionError("adapter must expose a non-empty adapter_id")
    if not callable(getattr(adapter, "supports", None)):
        raise ExternalExecutionError("adapter must expose a callable supports method")
    if not callable(getattr(adapter, "execute", None)):
        raise ExternalExecutionError("adapter must expose a callable execute method")


@dataclass(frozen=True)
class ExternalWriteRecord:
    """Immutable trace of a side effect performed against an external system."""

    command_id: str
    command_type: str
    target_ref: str
    status: str
    external_reference: str
    executed_at: str

    def to_mapping(self) -> dict[str, object]:
        return {
            "contract_version": "P9B.1",
            "command_id": self.command_id,
            "command_type": self.command_type,
            "target_ref": self.target_ref,
            "status": self.status,
            "external_reference": self.external_reference,
            "executed_at": self.executed_at,
        }


class InMemoryExternalSystem:
    """Minimal in-memory stand-in for an external target system.

    It records every side effect it receives, allowing tests to verify that an
    execution actually wrote to the "external" world without a live system. It
    carries no SCM semantics and is not canonical state.
    """

    def __init__(self) -> None:
        self._records: list[ExternalWriteRecord] = []

    @property
    def records(self) -> tuple[ExternalWriteRecord, ...]:
        return tuple(self._records)

    def write(self, record: ExternalWriteRecord) -> None:
        self._records.append(record)

    @property
    def write_count(self) -> int:
        return len(self._records)


class ReferenceExternalExecutionAdapter:
    """Deterministic external-execution test double.

    It supports the R5/Phase 5 command types (replenishment, procurement,
    production, distribution) and simulates a side effect by writing to the
    injected ``external_system`` (an :class:`InMemoryExternalSystem`). The
    outcome is derived deterministically from the command proposal:
    ``simulate_failure: true`` yields a failing result, ``simulate_partial: true``
    yields a partial result across two targets, and otherwise the command
    succeeds. This makes behavior fully reproducible for tests while exercising
    the same execute-boundary a live adapter will use.
    """

    adapter_id: str = "reference-external-execution"
    _SUPPORTED = frozenset({"replenishment", "procurement", "production", "distribution"})

    def supports(self, command_type: str) -> bool:
        return command_type in self._SUPPORTED

    def execute(
        self,
        command: ExecutionCommand,
        *,
        executed_at: str,
        external_system: InMemoryExternalSystem | None = None,
    ) -> ExecutionOutcomeContract:
        proposal = command.decision.proposal.output.proposal
        if not isinstance(proposal, dict):
            proposal = {"action": proposal}
        fail = bool(proposal.get("simulate_failure"))
        partial = bool(proposal.get("simulate_partial"))

        if fail:
            elements = (
                ResultElement(
                    target_ref=f"{command.command_type}:main",
                    status="failure",
                    external_reference=f"EXT-{command.command_id}-FAIL",
                    detail="simulated external system rejected the command",
                ),
            )
            verdict = "failure"
        elif partial:
            elements = (
                ResultElement(
                    target_ref=f"{command.command_type}:line-1",
                    status="success",
                    external_reference=f"EXT-{command.command_id}-L1",
                ),
                ResultElement(
                    target_ref=f"{command.command_type}:line-2",
                    status="failure",
                    external_reference=f"EXT-{command.command_id}-L2",
                    detail="simulated partial failure on line 2",
                ),
            )
            verdict = "partial"
        else:
            elements = (
                ResultElement(
                    target_ref=f"{command.command_type}:main",
                    status="success",
                    external_reference=f"EXT-{command.command_id}-OK",
                ),
            )
            verdict = "success"

        if external_system is not None:
            for element in elements:
                external_system.write(
                    ExternalWriteRecord(
                        command_id=command.command_id,
                        command_type=command.command_type,
                        target_ref=element.target_ref,
                        status=element.status,
                        external_reference=element.external_reference or "N/A",
                        executed_at=executed_at,
                    )
                )

        return build_execution_outcome_contract(
            command,
            elements=elements,
            recorded_at=executed_at,
            verdict=verdict,
            evidence_ids=tuple(command.decision.proposal.output.evidence_ids),
            provenance_ids=tuple(command.decision.proposal.output.provenance_ids),
            detail=(
                "simulated external execution"
                if verdict != "failure"
                else "simulated external execution failed"
            ),
        )


def execute_externally(
    command: ExecutionCommand,
    *,
    adapter: ExternalExecutionAdapter,
    executed_at: str,
    external_system: InMemoryExternalSystem | None = None,
) -> ExecutionOutcomeContract:
    """Execute a governed command through an external adapter.

    Fails closed unless the adapter is valid, supports the command type, and the
    command is an ``ExecutionCommand``. Returns an immutable outcome contract —
    never mutates canonical state.
    """
    if not isinstance(command, ExecutionCommand):
        raise ExternalExecutionError("command must be an ExecutionCommand")
    if not executed_at.strip():
        raise ExternalExecutionError("executed_at must be non-empty")
    validate_external_adapter(adapter)
    try:
        supported = adapter.supports(command.command_type)
    except Exception as exc:
        raise ExternalExecutionError(f"adapter supports check failed: {exc}") from exc
    if not supported:
        raise ExternalExecutionError(
            f"adapter {adapter.adapter_id} does not support command type {command.command_type!r}"
        )
    try:
        outcome = adapter.execute(
            command, executed_at=executed_at, external_system=external_system
        )
    except Exception as exc:
        raise ExternalExecutionError(f"external execution failed: {exc}") from exc
    if not isinstance(outcome, ExecutionOutcomeContract):
        raise ExternalExecutionError("adapter execute must return an ExecutionOutcomeContract")
    return outcome
