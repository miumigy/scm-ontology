from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ReasoningPolicyError(ValueError):
    pass


class TruthClass(str, Enum):
    CANONICAL = "canonical"
    DERIVED = "derived"
    INFERRED = "inferred"


@dataclass(frozen=True)
class ReasoningPolicy:
    allow_inferred_facts: bool = False
    allow_graph_mutation: bool = False
    allow_canonical_promotion: bool = False


def validate_truth_transition(
    source: TruthClass,
    target: TruthClass,
    policy: ReasoningPolicy,
) -> None:
    """Reject unsafe transitions between truth classes by default."""
    if source == target:
        return
    if target is TruthClass.INFERRED and not policy.allow_inferred_facts:
        raise ReasoningPolicyError("inferred facts are disabled by policy")
    if source is TruthClass.INFERRED and target is TruthClass.CANONICAL and not policy.allow_canonical_promotion:
        raise ReasoningPolicyError("inferred facts cannot be promoted to canonical truth")


def validate_graph_mutation(policy: ReasoningPolicy) -> None:
    if not policy.allow_graph_mutation:
        raise ReasoningPolicyError("reasoning policy forbids graph mutation")
