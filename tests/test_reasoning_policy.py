import pytest

from scm_ontology.reasoning_policy import (
    ReasoningPolicy,
    ReasoningPolicyError,
    TruthClass,
    validate_graph_mutation,
    validate_truth_transition,
)


def test_inferred_facts_are_rejected_by_default() -> None:
    with pytest.raises(ReasoningPolicyError):
        validate_truth_transition(TruthClass.DERIVED, TruthClass.INFERRED, ReasoningPolicy())


def test_inferred_to_canonical_promotion_is_rejected_by_default() -> None:
    policy = ReasoningPolicy(allow_inferred_facts=True)
    with pytest.raises(ReasoningPolicyError):
        validate_truth_transition(TruthClass.INFERRED, TruthClass.CANONICAL, policy)


def test_graph_mutation_is_rejected_by_default() -> None:
    with pytest.raises(ReasoningPolicyError):
        validate_graph_mutation(ReasoningPolicy())


def test_explicit_policy_can_allow_inference_without_canonical_promotion() -> None:
    policy = ReasoningPolicy(allow_inferred_facts=True)
    validate_truth_transition(TruthClass.DERIVED, TruthClass.INFERRED, policy)
