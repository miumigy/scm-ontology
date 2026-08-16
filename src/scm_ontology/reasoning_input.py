"""Immutable input boundary between ready decision context and reasoning engines."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .context_readiness import require_context_ready
from .decision_context import DecisionContext


class ReasoningInputError(ValueError):
    """Raised when a reasoning input cannot be constructed."""


@dataclass(frozen=True)
class ReasoningInput:
    context_id: str
    observations: tuple[Any, ...]
    evidence_ids: tuple[str, ...]
    provenance_ids: tuple[str, ...]

    def to_mapping(self) -> dict[str, object]:
        return {
            "contract_version": "S342.1",
            "context_id": self.context_id,
            "observations": [
                {
                    "question_id": o.question_id,
                    "value": o.value,
                    "evidence_ids": list(o.evidence_ids),
                    "provenance_ids": list(o.provenance_ids),
                }
                for o in self.observations
            ],
            "evidence_ids": list(self.evidence_ids),
            "provenance_ids": list(self.provenance_ids),
        }


def build_reasoning_input(context: DecisionContext) -> ReasoningInput:
    """Convert a ready DecisionContext into a storage/engine-neutral input."""
    require_context_ready(context)
    observations = tuple(context.observations)
    evidence_ids = tuple(sorted({eid for o in observations for eid in o.evidence_ids}))
    provenance_ids = tuple(sorted({pid for o in observations for pid in o.provenance_ids}))
    return ReasoningInput(
        context_id=context.context_id,
        observations=observations,
        evidence_ids=evidence_ids,
        provenance_ids=provenance_ids,
    )
