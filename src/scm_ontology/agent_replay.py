"""P10-F — Agent Replay / Audit.

Every agent observation, proposal, decision, authorization, command, and
outcome is replayable. P10-F records the full Phase 10 agent lifecycle as an
immutable, content-addressed, append-only audit trail that can be replayed to
prove reproducibility.

```text
AgentObservation
  -> AgentProposal
    -> AutonomyVerdict
      -> HumanControlRecord
        -> ExecutionCommand
          -> outcome
             (all recorded as one AgentAuditEntry)
```

P10-F introduces no new canonical semantics and performs no side effect. It
only persists an auditable, replayable record of the agent's governed path.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any

from .agent_observation import AgentObservation
from .agent_tool import AgentProposal
from .human_control import HumanControlRecord
from .policy_autonomy import AutonomyVerdict
from .execution_command import ExecutionCommand


class AgentReplayError(ValueError):
    """Raised when an agent audit entry or replay violates P10-F."""


@dataclass(frozen=True)
class AgentAuditEntry:
    """Immutable, content-addressed record of one full agent lifecycle step."""

    entry_id: str
    agent_id: str
    observation: AgentObservation | None = None
    proposal: AgentProposal | None = None
    autonomy: AutonomyVerdict | None = None
    control: HumanControlRecord | None = None
    command: ExecutionCommand | None = None
    outcome_ref: str = ""
    recorded_at: str = ""

    def __post_init__(self) -> None:
        if not self.agent_id.strip():
            raise AgentReplayError("agent_id must be non-empty")
        if not self.entry_id.strip():
            raise AgentReplayError("entry_id must be non-empty")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P10F.1",
            "entry_id": self.entry_id,
            "agent_id": self.agent_id,
            "observation_id": self.observation.observation_id if self.observation else None,
            "proposal_id": self.proposal.proposal_id if self.proposal else None,
            "autonomy": self.autonomy.to_mapping() if self.autonomy else None,
            "control": self.control.to_mapping() if self.control else None,
            "command_id": self.command.command_id if self.command else None,
            "outcome_ref": self.outcome_ref,
            "recorded_at": self.recorded_at,
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _entry_id(mapping: dict[str, Any]) -> str:
    return sha256(
        json.dumps(mapping, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def record_agent_entry(
    *,
    agent_id: str,
    observation: AgentObservation | None = None,
    proposal: AgentProposal | None = None,
    autonomy: AutonomyVerdict | None = None,
    control: HumanControlRecord | None = None,
    command: ExecutionCommand | None = None,
    outcome_ref: str = "",
    recorded_at: str = "",
) -> AgentAuditEntry:
    """Record one agent lifecycle step as a content-addressed audit entry."""
    if not isinstance(agent_id, str) or not agent_id.strip():
        raise AgentReplayError("agent_id must be non-empty")

    payload = {
        "agent_id": agent_id,
        "observation": observation.to_mapping() if observation else None,
        "proposal": proposal.to_mapping() if proposal else None,
        "autonomy": autonomy.to_mapping() if autonomy else None,
        "control": control.to_mapping() if control else None,
        "command": command.to_mapping() if command else None,
        "outcome_ref": outcome_ref,
        "recorded_at": recorded_at,
    }
    entry_id = _entry_id(payload)
    return AgentAuditEntry(
        entry_id=entry_id,
        agent_id=agent_id,
        observation=observation,
        proposal=proposal,
        autonomy=autonomy,
        control=control,
        command=command,
        outcome_ref=outcome_ref,
        recorded_at=recorded_at,
    )


@dataclass(frozen=True)
class AgentAuditTrail:
    """Append-only, immutable trail of agent lifecycle entries for one agent."""

    agent_id: str
    entries: tuple[AgentAuditEntry, ...] = ()

    def __post_init__(self) -> None:
        if not self.agent_id.strip():
            raise AgentReplayError("agent_id must be non-empty")
        if any(e.agent_id != self.agent_id for e in self.entries):
            raise AgentReplayError("all entries must belong to the same agent")

    def record(
        self,
        *,
        observation: AgentObservation | None = None,
        proposal: AgentProposal | None = None,
        autonomy: AutonomyVerdict | None = None,
        control: HumanControlRecord | None = None,
        command: ExecutionCommand | None = None,
        outcome_ref: str = "",
        recorded_at: str = "",
    ) -> "AgentAuditTrail":
        """Return a new trail with one more entry appended (immutable)."""
        entry = record_agent_entry(
            agent_id=self.agent_id,
            observation=observation,
            proposal=proposal,
            autonomy=autonomy,
            control=control,
            command=command,
            outcome_ref=outcome_ref,
            recorded_at=recorded_at,
        )
        return AgentAuditTrail(agent_id=self.agent_id, entries=self.entries + (entry,))

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P10F.1",
            "agent_id": self.agent_id,
            "entries": [entry.to_mapping() for entry in self.entries],
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    def replay(self) -> "AgentAuditTrail":
        """Replay the trail, proving deterministic reproducibility.

        Re-computes each entry's content address from its payload and verifies
        it matches the recorded ``entry_id``. If any entry is tampered with,
        replay raises ``AgentReplayError``.
        """
        replayed_entries: list[AgentAuditEntry] = []
        for entry in self.entries:
            payload = {
                "agent_id": entry.agent_id,
                "observation": entry.observation.to_mapping() if entry.observation else None,
                "proposal": entry.proposal.to_mapping() if entry.proposal else None,
                "autonomy": entry.autonomy.to_mapping() if entry.autonomy else None,
                "control": entry.control.to_mapping() if entry.control else None,
                "command": entry.command.to_mapping() if entry.command else None,
                "outcome_ref": entry.outcome_ref,
                "recorded_at": entry.recorded_at,
            }
            if _entry_id(payload) != entry.entry_id:
                raise AgentReplayError(
                    "agent audit entry content digest mismatch"
                )
            replayed_entries.append(entry)
        return AgentAuditTrail(agent_id=self.agent_id, entries=tuple(replayed_entries))
