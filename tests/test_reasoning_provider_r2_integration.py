"""Phase R2 integration: run the governed decision loop with each provider family."""
import json

from scm_ontology.decision_runtime import run_decision_loop
from scm_ontology.graph_reasoning_projection import GraphReasoningObservation
from scm_ontology.llm_reasoning_provider import LLMReasoningProvider
from scm_ontology.rule_reasoning_provider import ReasoningRule, RuleReasoningProvider, when_measurement_below


def observation():
    return GraphReasoningObservation(
        question_id="warehouse-stock",
        value={"warehouse": "WH-1", "stock": 5, "threshold": 10},
        evidence_ids=("e-stock-1",),
        provenance_ids=("p-erp-1",),
    )


def run_with(provider):
    return run_decision_loop(
        context_id="ctx-r2-integration",
        observations=(observation(),),
        provider=provider,
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T21:00:00Z",
        command_type="replenishment",
        command_id="cmd-r2-integration",
    )


class StubLlmClient:
    provider_id = "stub-gpt"

    def complete(self, prompt):
        return json.dumps(
            {
                "proposal": {"action": "replenish", "quantity": 10},
                "rationale": "warehouse stock is below threshold",
                "confidence": 0.9,
            }
        )


def test_governed_loop_runs_with_rule_provider():
    desc, matches = when_measurement_below("warehouse-stock", "stock", 10)
    rule = ReasoningRule(
        rule_id="replenish-low-stock",
        proposal={"action": "replenish", "quantity": 10},
        rationale="warehouse stock is below threshold",
        matches=matches,
        condition_description=desc,
        confidence=0.95,
    )
    provider = RuleReasoningProvider(provider_id="rule-replenish", rules=(rule,))
    result = run_with(provider)
    assert result.context_id == "ctx-r2-integration"
    cmd = result.execution_command.to_mapping()
    assert cmd["proposal"] == {"action": "replenish", "quantity": 10}
    assert cmd["evidence_ids"] == ["e-stock-1"]


def test_governed_loop_runs_with_llm_provider():
    provider = LLMReasoningProvider(client=StubLlmClient(), provider_id="llm-gpt")
    result = run_with(provider)
    assert result.context_id == "ctx-r2-integration"
    cmd = result.execution_command.to_mapping()
    assert cmd["proposal"] == {"action": "replenish", "quantity": 10}
    assert cmd["provenance_ids"] == ["p-erp-1"]
    # The immutable command carries the proposal, auth, and evidence.
    assert result.execution_command.to_mapping()["actor_id"] == "planner-1"


def test_r2_run_is_deterministic_across_provider_families_in_structure():
    # Both families follow the same governed loop shape: one context, immutable command.
    rule_result = run_with(RuleReasoningProvider(
        provider_id="rule-replenish",
        rules=(ReasoningRule(
            rule_id="r",
            proposal={"action": "replenish", "quantity": 10},
            rationale="low stock",
            matches=lambda observations: True,
            confidence=0.9,
        ),),
    ))
    llm_result = run_with(LLMReasoningProvider(client=StubLlmClient()))
    assert rule_result.to_mapping()["context_id"] == llm_result.to_mapping()["context_id"]
    assert rule_result.to_mapping()["execution_command"]["command_type"] == "replenishment"
    assert llm_result.to_mapping()["execution_command"]["command_type"] == "replenishment"
