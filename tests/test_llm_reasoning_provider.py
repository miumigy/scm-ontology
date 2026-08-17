import json

import pytest

from scm_ontology.graph_reasoning_projection import GraphReasoningObservation
from scm_ontology.llm_reasoning_provider import (
    LLMReasoningProvider,
    LlmProviderError,
    build_reasoning_prompt,
    parse_reasoning_response,
)
from scm_ontology.reasoning_assembly import assemble_reasoning_input
from scm_ontology.reasoning_provider import ReasoningProviderError, invoke_reasoning_provider


class StubLlmClient:
    provider_id = "stub-gpt"

    def __init__(self, response):
        self.response = response
        self.calls = []

    def complete(self, prompt):
        self.calls.append(prompt)
        return self.response


def reasoning_input():
    observation = GraphReasoningObservation(
        question_id="warehouse-stock",
        value={"warehouse": "WH-1", "stock": 5, "threshold": 10},
        evidence_ids=("e-stock-1",),
        provenance_ids=("p-erp-1",),
    )
    return assemble_reasoning_input("ctx-r2-llm", (observation,))


def conformant_json():
    return json.dumps(
        {
            "proposal": {"action": "replenish", "quantity": 10},
            "rationale": "warehouse stock is below threshold",
            "confidence": 0.9,
        }
    )


def test_llm_provider_runs_and_preserves_context_evidence():
    client = StubLlmClient(conformant_json())
    provider = LLMReasoningProvider(client=client, provider_id="llm-gpt")
    output = invoke_reasoning_provider(provider, reasoning_input())
    assert output.context_id == "ctx-r2-llm"
    assert output.proposal == {"action": "replenish", "quantity": 10}
    assert output.evidence_ids == ("e-stock-1",)
    assert output.provenance_ids == ("p-erp-1",)
    assert output.confidence == 0.9
    assert len(client.calls) == 1


def test_llm_provider_prompt_is_deterministic_and_scoped():
    client = StubLlmClient(conformant_json())
    provider = LLMReasoningProvider(client=client)
    invoke_reasoning_provider(provider, reasoning_input())
    prompt = client.calls[0]
    assert "ctx-r2-llm" in prompt
    assert "e-stock-1" in prompt
    assert "p-erp-1" in prompt
    # prompt is stable across identical inputs
    client2 = StubLlmClient(conformant_json())
    provider2 = LLMReasoningProvider(client=client2)
    invoke_reasoning_provider(provider2, reasoning_input())
    assert client.calls[0] == client2.calls[0]


def test_llm_provider_parses_code_fenced_json():
    raw = "```json\n" + conformant_json() + "\n```"
    output = parse_reasoning_response(reasoning_input(), raw)
    assert output.proposal == {"action": "replenish", "quantity": 10}


def test_llm_provider_fails_closed_on_non_json():
    with pytest.raises(LlmProviderError, match="not valid JSON"):
        parse_reasoning_response(reasoning_input(), "not json at all")


def test_llm_provider_fails_closed_on_malformed_json():
    with pytest.raises(LlmProviderError, match="proposal must be non-empty"):
        parse_reasoning_response(reasoning_input(), json.dumps({"rationale": "r"}))
    with pytest.raises(LlmProviderError, match="rationale"):
        parse_reasoning_response(reasoning_input(), json.dumps({"proposal": {"a": 1}}))


def test_llm_provider_fails_closed_on_empty_response():
    client = StubLlmClient("")
    provider = LLMReasoningProvider(client=client)
    with pytest.raises(ReasoningProviderError, match="reasoning provider failed: model returned an empty response"):
        invoke_reasoning_provider(provider, reasoning_input())


def test_llm_provider_ignores_model_invented_evidence():
    # Model tries to inject foreign evidence; the boundary must not carry it.
    raw = json.dumps(
        {
            "proposal": {"action": "replenish", "quantity": 10},
            "rationale": "r",
            "evidence_ids": ["e-invented"],
        }
    )
    output = parse_reasoning_response(reasoning_input(), raw)
    assert output.evidence_ids == ("e-stock-1",)


def test_build_reasoning_prompt_returns_deterministic_payload():
    p1 = build_reasoning_prompt(reasoning_input())
    p2 = build_reasoning_prompt(reasoning_input())
    assert p1 == p2
    assert json.loads(p1.split("\n", 1)[1])["context_id"] == "ctx-r2-llm"
