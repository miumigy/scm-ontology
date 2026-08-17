import pytest

from scm_ontology.reasoning_assembly import assemble_reasoning_input
from scm_ontology.reasoning_provider import ReasoningProviderError, invoke_reasoning_provider
from scm_ontology.rule_reasoning_provider import (
    ReasoningRule,
    RuleReasoningProvider,
    RuleReasoningProviderError,
    when_measurement_below,
)
from scm_ontology.graph_reasoning_projection import GraphReasoningObservation


def reasoning_input(stock: int = 5):
    observation = GraphReasoningObservation(
        question_id="warehouse-stock",
        value={"warehouse": "WH-1", "stock": stock, "threshold": 10},
        evidence_ids=("e-stock-1",),
        provenance_ids=("p-erp-1",),
    )
    return assemble_reasoning_input("ctx-r2-rule", (observation,))


def replenishment_rules():
    desc, matches = when_measurement_below("warehouse-stock", "stock", 10)
    low = ReasoningRule(
        rule_id="replenish-low-stock",
        proposal={"action": "replenish", "quantity": 10},
        rationale="warehouse stock is below threshold",
        matches=matches,
        condition_description=desc,
        confidence=0.95,
    )
    return (low,), low


def test_rule_provider_fires_first_matching_rule():
    rules, _ = replenishment_rules()
    provider = RuleReasoningProvider(provider_id="rule-replenish", rules=rules)
    output = invoke_reasoning_provider(provider, reasoning_input())
    assert output.context_id == "ctx-r2-rule"
    assert output.proposal == {"action": "replenish", "quantity": 10}
    assert output.rationale.endswith("[replenish-low-stock]")
    assert output.evidence_ids == ("e-stock-1",)
    assert output.provenance_ids == ("p-erp-1",)
    assert output.confidence == 0.95


def test_rule_provider_is_deterministic():
    rules, _ = replenishment_rules()
    provider = RuleReasoningProvider(provider_id="rule-replenish", rules=rules)
    first = invoke_reasoning_provider(provider, reasoning_input())
    second = invoke_reasoning_provider(provider, reasoning_input())
    assert first.to_mapping() == second.to_mapping()


def test_rule_provider_fails_closed_when_no_rule_matches():
    rules, _ = replenishment_rules()
    provider = RuleReasoningProvider(provider_id="rule-replenish", rules=rules)
    # The S368 boundary normalizes the provider's fail-closed error.
    with pytest.raises(ReasoningProviderError, match="no matching rule"):
        invoke_reasoning_provider(provider, reasoning_input(stock=20))


def test_provider_rejects_duplicate_rule_ids():
    rule = ReasoningRule(
        rule_id="dup",
        proposal="keep",
        rationale="duplicate",
        matches=lambda observations: True,
    )
    with pytest.raises(RuleReasoningProviderError, match="unique"):
        RuleReasoningProvider(provider_id="p", rules=(rule, rule))


def test_provider_rejects_empty_rules():
    with pytest.raises(RuleReasoningProviderError, match="rules must not be empty"):
        RuleReasoningProvider(provider_id="p", rules=())


def test_rule_validates_proposal_and_confidence():
    with pytest.raises(RuleReasoningProviderError, match="proposal must be non-empty"):
        ReasoningRule(
            rule_id="r",
            proposal=None,
            rationale="x",
            matches=lambda observations: True,
        )
    with pytest.raises(RuleReasoningProviderError, match="confidence"):
        ReasoningRule(
            rule_id="r",
            proposal="x",
            rationale="x",
            matches=lambda observations: True,
            confidence=1.5,
        )


def test_when_measurement_below_helper():
    desc, matches = when_measurement_below("warehouse-stock", "stock", 10)
    assert matches(reasoning_input().observations) is True
    assert matches(reasoning_input(stock=20).observations) is False
    assert "warehouse-stock.stock < 10" in desc
