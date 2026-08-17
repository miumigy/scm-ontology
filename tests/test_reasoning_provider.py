import pytest

from scm_ontology.reasoning_input import ReasoningInput
from scm_ontology.reasoning_output import ReasoningOutput
from scm_ontology.reasoning_provider import ReasoningProviderError, invoke_reasoning_provider


def reasoning_input():
    return ReasoningInput(
        context_id="ctx-1",
        observations=(),
        evidence_ids=("e1",),
        provenance_ids=("p1",),
    )


class EchoProvider:
    provider_id = "echo"

    def reason(self, value):
        return ReasoningOutput(
            context_id=value.context_id,
            proposal="replenish",
            rationale="provider proposal",
            evidence_ids=value.evidence_ids,
            provenance_ids=value.provenance_ids,
            confidence=0.9,
        )


def test_provider_boundary_returns_immutable_reasoning_output():
    result = invoke_reasoning_provider(EchoProvider(), reasoning_input())
    assert result.context_id == "ctx-1"
    assert result.proposal == "replenish"
    assert result.evidence_ids == ("e1",)
    assert result.provenance_ids == ("p1",)


def test_provider_boundary_rejects_invalid_provider():
    with pytest.raises(ReasoningProviderError, match="provider_id"):
        invoke_reasoning_provider(object(), reasoning_input())

    class NoReason:
        provider_id = "no-reason"

    with pytest.raises(ReasoningProviderError, match="callable reason"):
        invoke_reasoning_provider(NoReason(), reasoning_input())


def test_provider_boundary_normalizes_provider_failure():
    class Failing:
        provider_id = "failing"

        def reason(self, value):
            raise RuntimeError("boom")

    with pytest.raises(ReasoningProviderError, match="reasoning provider failed: boom"):
        invoke_reasoning_provider(Failing(), reasoning_input())


def test_provider_boundary_rejects_wrong_output_and_context():
    class WrongType:
        provider_id = "wrong-type"

        def reason(self, value):
            return {"context_id": value.context_id}

    with pytest.raises(ReasoningProviderError, match="must return ReasoningOutput"):
        invoke_reasoning_provider(WrongType(), reasoning_input())

    class WrongContext:
        provider_id = "wrong-context"

        def reason(self, value):
            return ReasoningOutput(
                context_id="other",
                proposal="x",
                rationale="wrong context",
            )

    with pytest.raises(ReasoningProviderError, match="context_id"):
        invoke_reasoning_provider(WrongContext(), reasoning_input())
