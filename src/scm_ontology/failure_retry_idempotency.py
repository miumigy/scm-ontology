"""P9-F — Failure / Retry / Idempotency for governed external execution.

Adds the reliability semantics a real closed loop needs on top of the P9-C
approval-to-execution runtime and the P9-A outcome contract:

- **Idempotency / duplicate protection** — a command id is executed at most once
  against the external system. A duplicate submission returns the recorded
  outcome without re-executing.
- **Bounded retry** — a ``failure`` outcome is retried up to ``max_attempts``
  with a deterministic attempt counter. A ``partial`` outcome is recorded and NOT
  retried (a retry must never redo the already-succeeded portion). A ``success``
  outcome is recorded as terminal.
- **Recovery semantics** — when retries are exhausted on a failure, the command
  is marked ``failed_permanently`` and an explicit recovery (escalation) record is
  issued so operators can intervene.

This module performs no canonical mutation; every outcome is captured as an
immutable P9-A contract, and re-execution is governed by the recorded run state.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .approval_to_execution_runtime import (
    ApprovalToExecutionResult,
    approve_and_execute,
)
from .execution_command import ExecutionCommand
from .execution_outcome_contract import ExecutionOutcomeContract
from .external_execution_adapter import ExternalExecutionAdapter


class FailureRetryError(ValueError):
    """Raised when a failure/retry policy is violated."""


_TERMINAL_STATUSES = frozenset({"executed", "partial", "failed_permanently"})


@dataclass(frozen=True)
class ExecutionAttempt:
    """One recorded attempt of a command against the external system."""

    attempt_number: int
    outcome: ExecutionOutcomeContract
    attempted_at: str

    def __post_init__(self) -> None:
        if self.attempt_number < 1:
            raise FailureRetryError("attempt_number must be >= 1")
        if not isinstance(self.outcome, ExecutionOutcomeContract):
            raise FailureRetryError("outcome must be an ExecutionOutcomeContract")
        if not self.attempted_at.strip():
            raise FailureRetryError("attempted_at must be non-empty")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "attempt_number": self.attempt_number,
            "attempted_at": self.attempted_at,
            "outcome": self.outcome.to_mapping(),
        }


@dataclass(frozen=True)
class ExecutionRunRecord:
    """Immutable record of all attempts for one command id."""

    command_id: str
    status: str
    attempts: tuple[ExecutionAttempt, ...]
    recovery: RecoverySignal | None = None

    def __post_init__(self) -> None:
        if not self.command_id.strip():
            raise FailureRetryError("command_id must be non-empty")
        if self.status not in _TERMINAL_STATUSES:
            raise FailureRetryError(
                f"status must be one of {sorted(_TERMINAL_STATUSES)}"
            )
        object.__setattr__(self, "attempts", tuple(self.attempts))
        if not self.attempts:
            raise FailureRetryError("attempts must not be empty")

    @property
    def last_outcome(self) -> ExecutionOutcomeContract:
        return self.attempts[-1].outcome

    @property
    def attempt_count(self) -> int:
        return len(self.attempts)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P9F.1",
            "command_id": self.command_id,
            "status": self.status,
            "attempt_count": self.attempt_count,
            "attempts": [attempt.to_mapping() for attempt in self.attempts],
            "recovery": self.recovery.to_mapping() if self.recovery is not None else None,
        }


@dataclass(frozen=True)
class RecoverySignal:
    """Immutable escalation signal issued when automatic retries are exhausted."""

    command_id: str
    reason: str
    issued_at: str
    required_action: str = "manual intervention required"

    def __post_init__(self) -> None:
        if not self.command_id.strip():
            raise FailureRetryError("command_id must be non-empty")
        if not self.reason.strip():
            raise FailureRetryError("reason must be non-empty")
        if not self.issued_at.strip():
            raise FailureRetryError("issued_at must be non-empty")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P9F.2",
            "command_id": self.command_id,
            "reason": self.reason,
            "issued_at": self.issued_at,
            "required_action": self.required_action,
        }


class ExecutionRunRegistry:
    """Append-only store of terminal execution run records (idempotency keyed)."""

    def __init__(self) -> None:
        self._records: dict[str, ExecutionRunRecord] = {}

    @property
    def command_ids(self) -> tuple[str, ...]:
        return tuple(self._records)

    def has(self, command_id: str) -> bool:
        return command_id in self._records

    def get(self, command_id: str) -> ExecutionRunRecord | None:
        return self._records.get(command_id)

    def record(self, record: ExecutionRunRecord) -> None:
        if not isinstance(record, ExecutionRunRecord):
            raise FailureRetryError("record must be an ExecutionRunRecord")
        existing = self._records.get(record.command_id)
        if existing is not None:
            raise FailureRetryError(
                f"command {record.command_id!r} is already recorded; cannot overwrite"
            )
        self._records[record.command_id] = record


@dataclass(frozen=True)
class RunPolicy:
    """Bound of retry attempts for the failure policy."""

    max_attempts: int

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise FailureRetryError("max_attempts must be >= 1")


class RetryableAdapter:
    """Adapter wrapper that can be programmed to fail a fixed number of times.

    This makes retry behavior deterministic and testable: the underlying
    ``ReferenceExternalExecutionAdapter`` runs normally, but the first
    ``failures_before_success`` calls return a failure outcome so the retry
    policy can be exercised without a live or flaky system.
    """

    def __init__(
        self,
        adapter: ExternalExecutionAdapter,
        failures_before_success: int = 0,
        *,
        fail_partial_after: int | None = None,
    ) -> None:
        self._adapter = adapter
        self._failures_left = failures_before_success
        self._calls = 0
        self._fail_partial_after = fail_partial_after

    @property
    def adapter_id(self) -> str:
        return self._adapter.adapter_id

    def supports(self, command_type: str) -> bool:
        return self._adapter.supports(command_type)

    @property
    def call_count(self) -> int:
        return self._calls

    def execute(self, command, *, executed_at, external_system=None) -> ExecutionOutcomeContract:
        from .execution_outcome_contract import ResultElement, build_execution_outcome_contract

        self._calls += 1
        if self._failures_left > 0:
            self._failures_left -= 1
            return build_execution_outcome_contract(
                command,
                elements=(
                    ResultElement(
                        target_ref=f"{command.command_type}:main",
                        status="failure",
                        external_reference=f"RETRY-{command.command_id}-{self._calls}",
                        detail="simulated transient failure",
                    ),
                ),
                recorded_at=executed_at,
                verdict="failure",
            )
        if self._fail_partial_after is not None and self._calls >= self._fail_partial_after:
            return build_execution_outcome_contract(
                command,
                elements=(
                    ResultElement(
                        target_ref=f"{command.command_type}:line-1",
                        status="success",
                        external_reference=f"PART-{command.command_id}-1",
                    ),
                    ResultElement(
                        target_ref=f"{command.command_type}:line-2",
                        status="failure",
                        external_reference=f"PART-{command.command_id}-2",
                        detail="simulated partial failure",
                    ),
                ),
                recorded_at=executed_at,
                verdict="partial",
            )
        return self._adapter.execute(
            command, executed_at=executed_at, external_system=external_system
        )


def run_with_failure_policy(
    command: ExecutionCommand,
    *,
    adapter: ExternalExecutionAdapter,
    policy: RunPolicy,
    registry: ExecutionRunRegistry,
    actor_id: str,
    executed_at: str,
    external_system: object | None = None,
) -> ExecutionRunRecord:
    """Execute a command with idempotency, bounded retry, and recovery semantics.

    - If ``command.command_id`` is already recorded as terminal, return the
      recorded run WITHOUT re-executing (duplicate-command protection).
    - A ``success`` attempt records status ``executed``.
    - A ``partial`` attempt records status ``partial`` and stops (no redo of the
      succeeded portion); a recovery signal is not needed because some progress
      was made, but the run is terminal.
    - A ``failure`` attempt is retried up to ``policy.max_attempts`` total
      attempts; once exhausted the run is recorded as ``failed_permanently`` with
      a ``RecoverySignal`` for operator intervention.
    """
    if not isinstance(command, ExecutionCommand):
        raise FailureRetryError("command must be an ExecutionCommand")
    if not isinstance(policy, RunPolicy):
        raise FailureRetryError("policy must be a RunPolicy")
    if not isinstance(registry, ExecutionRunRegistry):
        raise FailureRetryError("registry must be an ExecutionRunRegistry")
    if not actor_id.strip() or not executed_at.strip():
        raise FailureRetryError("actor_id and executed_at must be non-empty")

    existing = registry.get(command.command_id)
    if existing is not None:
        # Idempotent replay: never re-execute an already terminal command.
        return existing

    attempts: list[ExecutionAttempt] = []
    final_status = "executed"
    recovery: RecoverySignal | None = None

    for attempt_number in range(1, policy.max_attempts + 1):
        result: ApprovalToExecutionResult = approve_and_execute(
            command,
            adapter=adapter,
            executed_at=executed_at,
            actor_id=actor_id,
            external_system=external_system,
        )
        outcome = result.outcome
        attempts.append(
            ExecutionAttempt(
                attempt_number=attempt_number,
                outcome=outcome,
                attempted_at=executed_at,
            )
        )
        if outcome.verdict == "success":
            final_status = "executed"
            break
        if outcome.verdict == "partial":
            final_status = "partial"
            break
        # verdict == "failure": continue to next attempt unless exhausted.
        if attempt_number == policy.max_attempts:
            final_status = "failed_permanently"
            recovery = RecoverySignal(
                command_id=command.command_id,
                reason=(
                    f"external execution failed after {policy.max_attempts} "
                    "attempts; automatic retry exhausted"
                ),
                issued_at=executed_at,
            )

    record = ExecutionRunRecord(
        command_id=command.command_id,
        status=final_status,
        attempts=tuple(attempts),
        recovery=recovery,
    )
    registry.record(record)
    return record
