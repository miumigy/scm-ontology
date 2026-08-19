"""P10-B — Tool / Action Boundary.

Agents propose actions; they never perform canonical mutations directly. This
slice draws an explicit tool boundary: every agent tool produces a structured,
content-addressed ``AgentProposal`` (a proposed action with rationale and
evidence) that must still traverse proposal validation (S344) and
authorization (S345) before it may become an ``ExecutionCommand``.

An agent tool boundary:

- restricts agent tools to read (P10-A observations) and propose (P10-B);
- forbids direct canonical-graph mutation from any tool output;
- routes every proposed action through the governed proposal -> authorization
  -> execution command path;
- keeps each proposal immutable, evidence-aware, and replay-auditable.

P10-B introduces no new canonical semantics and performs no side effect. A tool
may only emit an ``AgentProposal``; turning it into an ``ExecutionCommand`` is
the responsibility of the governed decision layer, not of the agent.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Callable

from .agent_observation import AgentObservation
from .execution_command import ExecutionCommand
from .decision_authorization import AuthorizedDecision
from .proposal_validation import validate_decision_proposal
from .reasoning_input import ReasoningInput
from .reasoning_output import ReasoningOutput


class AgentToolError(ValueError):
    """Raised when an agent tool violates the P10-B tool boundary."""


@dataclass(frozen=True)
class AgentProposal:
    """Structured, evidence-aware proposed action produced by an agent tool.

    A proposal is never an execution: it must be authorized and turned into an
    ``ExecutionCommand`` through the governed decision layer before any side
    effect may occur.
    """

    agent_id: str
    context_id: str
    action: str
    payload: dict[str, Any]
    rationale: str
    evidence_ids: tuple[str, ...] = ()
    provenance_ids: tuple[str, ...] = ()
    confidence: float | None = None
    proposal_id: str = field(default="", init=False)

    def __post_init__(self) -> None:
        if not self.agent_id.strip():
            raise AgentToolError("agent_id must be non-empty")
        if not self.context_id.strip():
            raise AgentToolError("context_id must be non-empty")
        if not self.action.strip():
            raise AgentToolError("action must be non-empty")
        if not self.rationale.strip():
            raise AgentToolError("rationale must be non-empty")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise AgentToolError("confidence must be between 0 and 1")
        object.__setattr__(self, "evidence_ids", tuple(sorted(set(self.evidence_ids))))
        object.__setattr__(self, "provenance_ids", tuple(sorted(set(self.provenance_ids))))
        object.__setattr__(self, "proposal_id", self._compute_id())

    def _compute_id(self) -> str:
        payload = json.dumps(
            {
                "agent_id": self.agent_id,
                "context_id": self.context_id,
                "action": self.action,
                "payload": self.payload,
                "rationale": self.rationale,
                "evidence_ids": list(self.evidence_ids),
                "provenance_ids": list(self.provenance_ids),
                "confidence": self.confidence,
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        )
        return sha256(payload.encode()).hexdigest()

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P10B.1",
            "proposal_id": self.proposal_id,
            "agent_id": self.agent_id,
            "context_id": self.context_id,
            "action": self.action,
            "payload": self.payload,
            "rationale": self.rationale,
            "evidence_ids": list(self.evidence_ids),
            "provenance_ids": list(self.provenance_ids),
            "confidence": self.confidence,
        }

    def to_reasoning_output(self) -> ReasoningOutput:
        """Convert the proposal into the governed reasoning-output boundary."""
        return ReasoningOutput(
            context_id=self.context_id,
            proposal={"action": self.action, "payload": self.payload},
            rationale=self.rationale,
            evidence_ids=self.evidence_ids,
            provenance_ids=self.provenance_ids,
            confidence=self.confidence,
        )


@dataclass(frozen=True)
class AgentToolResult:
    """Immutable result of invoking an agent tool under the P10-B boundary."""

    tool_id: str
    agent_id: str
    observation: AgentObservation | None
    proposal: AgentProposal | None
    result_id: str

    @property
    def can_mutate(self) -> bool:
        """Agent tools never emit a canonical mutation."""
        return False

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P10B.1",
            "tool_id": self.tool_id,
            "agent_id": self.agent_id,
            "can_mutate": False,
            "result_id": self.result_id,
            "observation_id": self.observation.observation_id if self.observation else None,
            "proposal": self.proposal.to_mapping() if self.proposal else None,
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _result_id(tool_id: str, agent_id: str, observation_id: str | None, proposal_id: str | None) -> str:
    payload = json.dumps(
        {
            "tool_id": tool_id,
            "agent_id": agent_id,
            "observation_id": observation_id,
            "proposal_id": proposal_id,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return sha256(payload.encode()).hexdigest()


def run_agent_tool(
    *,
    tool_id: str,
    agent_id: str,
    observation: AgentObservation | None,
    propose: Callable[[AgentObservation | None], AgentProposal],
) -> AgentToolResult:
    """Run an agent tool under the P10-B boundary.

    The tool's ``propose`` callable may read the observation and must return an
    ``AgentProposal``. It may never perform a canonical mutation — the boundary
    enforces that the tool returns only a proposal, and application of the
    proposal to an execution command belongs to the governed decision layer.
    """
    if not tool_id.strip():
        raise AgentToolError("tool_id must be non-empty")
    if not agent_id.strip():
        raise AgentToolError("agent_id must be non-empty")
    if not callable(propose):
        raise AgentToolError("propose must be callable")

    proposal = propose(observation)
    if not isinstance(proposal, AgentProposal):
        raise AgentToolError("agent tool must return an AgentProposal")
    if proposal.agent_id != agent_id:
        raise AgentToolError("proposal agent_id must match the tool agent")

    return AgentToolResult(
        tool_id=tool_id,
        agent_id=agent_id,
        observation=observation,
        proposal=proposal,
        result_id=_result_id(
            tool_id,
            agent_id,
            observation.observation_id if observation else None,
            proposal.proposal_id,
        ),
    )


def proposal_to_execution_command(
    proposal: AgentProposal,
    *,
    reasoning_input: ReasoningInput,
    actor_id: str,
    authority: str,
    authorized_at: str,
    command_type: str,
    command_id: str,
) -> ExecutionCommand:
    """Route an agent proposal through the governed decision layer into a command.

    The agent proposal must first validate against the reasoning input (S344)
    and be authorized (S345). If either gate fails, no ``ExecutionCommand`` is
    produced — the proposal never becomes a side effect without governance.
    """
    from .decision_authorization import authorize_decision
    from .execution_command import build_execution_command

    output = proposal.to_reasoning_output()
    validated = validate_decision_proposal(reasoning_input, output)
    authorized: AuthorizedDecision = authorize_decision(
        validated,
        actor_id=actor_id,
        authority=authority,
        authorized_at=authorized_at,
    )
    return build_execution_command(
        authorized,
        command_type=command_type,
        command_id=command_id,
    )
