from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.decision_runtime import (
    DecisionRuntimeError,
    DecisionRuntimeResult,
    MockReasoningProvider,
    run_decision_loop,
)
from scm_ontology.graph_reasoning_projection import GraphReasoningObservation
from scm_ontology.reasoning_output import ReasoningOutput
from scm_ontology.reasoning_provider import invoke_reasoning_provider


def observation():
    return GraphReasoningObservation(
        question_id="warehouse-stock",
        value={"warehouse": "WH-1", "stock": 5, "threshold": 10},
        evidence_ids=("e-stock-1",),
        provenance_ids=("p-erp-1",),
    )


def provider():
    return MockReasoningProvider(
        provider_id="mock-v0",
        proposal={"action": "replenish", "quantity": 10},
        rationale="warehouse stock is below threshold",
        confidence=0.95,
    )


def run_args(**overrides):
    args = dict(
        context_id="ctx-runtime-1",
        observations=(observation(),),
        provider=provider(),
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T21:00:00Z",
        command_type="replenishment",
        command_id="cmd-runtime-1",
    )
    args.update(overrides)
    return args


def test_runtime_runs_full_governed_loop_end_to_end():
    result = run_decision_loop(**run_args())

    assert isinstance(result, DecisionRuntimeResult)
    assert result.context_id == "ctx-runtime-1"
    assert result.reasoning_input.context_id == "ctx-runtime-1"
    assert result.reasoning_output.context_id == "ctx-runtime-1"
    assert result.validated_proposal.output.context_id == "ctx-runtime-1"
    assert result.authorized_decision.context_id == "ctx-runtime-1"
    assert result.execution_command.context_id == "ctx-runtime-1"

    assert result.reasoning_output.proposal == {"action": "replenish", "quantity": 10}
    assert result.reasoning_output.evidence_ids == ("e-stock-1",)
    assert result.reasoning_output.provenance_ids == ("p-erp-1",)
    assert result.execution_command.command_type == "replenishment"
    assert result.execution_command.command_id == "cmd-runtime-1"


def test_runtime_preserves_evidence_and_provenance_throughout():
    result = run_decision_loop(**run_args())
    assert result.reasoning_input.evidence_ids == ("e-stock-1",)
    assert result.reasoning_input.provenance_ids == ("p-erp-1",)
    assert result.reasoning_output.evidence_ids == ("e-stock-1",)
    assert result.reasoning_output.provenance_ids == ("p-erp-1",)
    assert result.execution_command.decision.proposal.output.evidence_ids == ("e-stock-1",)
    assert result.execution_command.decision.proposal.output.provenance_ids == ("p-erp-1",)


def test_runtime_is_deterministic():
    first = run_decision_loop(**run_args())
    second = run_decision_loop(**run_args())
    assert first.to_json() == second.to_json()


def test_result_mapping_is_json_safe_and_has_contract_version():
    result = run_decision_loop(**run_args())
    mapping = result.to_mapping()
    assert mapping["contract_version"] == "S348.1"
    assert mapping["context_id"] == "ctx-runtime-1"
    assert isinstance(mapping["execution_command"], dict)

    import json
    decoded = json.loads(result.to_json())
    assert decoded["execution_command"]["command_id"] == "cmd-runtime-1"


def test_result_artifacts_are_immutable():
    result = run_decision_loop(**run_args())
    for obj in (
        result,
        result.reasoning_input,
        result.reasoning_output,
        result.validated_proposal,
        result.authorized_decision,
        result.execution_command,
    ):
        with pytest.raises(FrozenInstanceError):
            obj.context_id = "other"


def test_runtime_fails_closed_on_empty_observations():
    with pytest.raises(DecisionRuntimeError, match="context assembly"):
        run_decision_loop(**run_args(observations=()))


def test_runtime_fails_closed_on_blank_context_id():
    with pytest.raises(DecisionRuntimeError, match="context_id"):
        run_decision_loop(**run_args(context_id="   "))


def test_runtime_fails_closed_when_provider_returns_mismatched_context(tmp_path):
    class ProviderWithWrongContext:
        provider_id = "wrong-context"

        def reason(self, reasoning_input):
            return ReasoningOutput(
                context_id="other",
                proposal="replenish",
                rationale="mismatch",
                evidence_ids=reasoning_input.evidence_ids,
                provenance_ids=reasoning_input.provenance_ids,
            )

    with pytest.raises(DecisionRuntimeError, match="reasoning"):
        run_decision_loop(**run_args(provider=ProviderWithWrongContext()))


def test_runtime_fails_closed_when_evidence_not_subset_of_input():
    class ProviderWithForeignEvidence:
        provider_id = "foreign-evidence"

        def reason(self, reasoning_input):
            return ReasoningOutput(
                context_id=reasoning_input.context_id,
                proposal="replenish",
                rationale="foreign evidence",
                evidence_ids=("e-other",),
                provenance_ids=reasoning_input.provenance_ids,
            )

    with pytest.raises(DecisionRuntimeError, match="proposal validation"):
        run_decision_loop(**run_args(provider=ProviderWithForeignEvidence()))


def test_runtime_fails_closed_on_blank_authorization_actor():
    with pytest.raises(DecisionRuntimeError, match="authorization"):
        run_decision_loop(**run_args(actor_id=""))


def test_runtime_fails_closed_on_blank_command_type():
    with pytest.raises(DecisionRuntimeError, match="command construction"):
        run_decision_loop(**run_args(command_type=""))


def test_mock_provider_conforms_to_reasoning_provider_boundary():
    result = run_decision_loop(**run_args())
    invoked = invoke_reasoning_provider(provider(), result.reasoning_input)
    assert invoked.context_id == "ctx-runtime-1"
    assert invoked.proposal == {"action": "replenish", "quantity": 10}


def test_mock_provider_rejects_invalid_construction():
    with pytest.raises(DecisionRuntimeError, match="proposal must be non-empty"):
        MockReasoningProvider(provider_id="p", proposal=None, rationale="r")
    with pytest.raises(DecisionRuntimeError, match="confidence"):
        MockReasoningProvider(provider_id="p", proposal="x", rationale="r", confidence=1.5)


def test_runtime_with_mock_provider_is_side_effect_free(tmp_path):
    sentinel = tmp_path / "side-effect"
    assert not sentinel.exists()
    run_decision_loop(**run_args())
    assert not sentinel.exists()
    assert set(tmp_path.iterdir()) == set()
