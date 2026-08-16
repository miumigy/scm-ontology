import pytest

from scm_ontology.proposal_validation import ProposalValidationError, validate_decision_proposal
from scm_ontology.reasoning_input import ReasoningInput
from scm_ontology.reasoning_output import ReasoningOutput


def reasoning_input():
    return ReasoningInput(
        context_id="ctx-1",
        observations=(),
        evidence_ids=("e1", "e2"),
        provenance_ids=("p1", "p2"),
    )


def output(**kwargs):
    values = {
        "context_id": "ctx-1",
        "proposal": {"action": "replenish"},
        "rationale": "stock position is below policy threshold",
        "evidence_ids": ("e1",),
        "provenance_ids": ("p1",),
        "confidence": 0.9,
    }
    values.update(kwargs)
    return ReasoningOutput(**values)


def test_validate_decision_proposal_accepts_supported_immutable_output():
    result = validate_decision_proposal(reasoning_input(), output())
    assert result.output is not None
    assert result.to_mapping()["contract_version"] == "S344.1"


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"context_id": "ctx-2"}, "context_id"),
        ({"proposal": ""}, "proposal"),
        ({"evidence_ids": ()}, "evidence_ids"),
        ({"provenance_ids": ()}, "provenance_ids"),
        ({"evidence_ids": ("foreign",)}, "evidence_ids"),
        ({"provenance_ids": ("foreign",)}, "provenance_ids"),
    ],
)
def test_validate_decision_proposal_fails_closed(kwargs, message):
    with pytest.raises(ProposalValidationError, match=message):
        validate_decision_proposal(reasoning_input(), output(**kwargs))
