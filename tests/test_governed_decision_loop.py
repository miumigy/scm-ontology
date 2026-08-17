from scm_ontology.decision_authorization import authorize_decision
from scm_ontology.execution_command import build_execution_command
from scm_ontology.graph_reasoning_projection import GraphReasoningObservation
from scm_ontology.proposal_validation import validate_decision_proposal
from scm_ontology.reasoning_assembly import assemble_reasoning_input
from scm_ontology.reasoning_output import ReasoningOutput
from scm_ontology.reasoning_provider import invoke_reasoning_provider


class ReplenishmentProvider:
    provider_id = "test-provider"

    def reason(self, reasoning_input):
        return ReasoningOutput(
            context_id=reasoning_input.context_id,
            proposal={"action": "replenish", "quantity": 10},
            rationale="warehouse stock is below threshold",
            evidence_ids=reasoning_input.evidence_ids,
            provenance_ids=reasoning_input.provenance_ids,
            confidence=0.95,
        )


def test_governed_decision_loop_is_end_to_end_and_deterministic():
    observation = GraphReasoningObservation(
        question_id="warehouse-stock",
        value={"warehouse": "WH-1", "stock": 5, "threshold": 10},
        evidence_ids=("e-stock-1",),
        provenance_ids=("p-erp-1",),
    )
    reasoning_input = assemble_reasoning_input("ctx-371", (observation,))
    output = invoke_reasoning_provider(ReplenishmentProvider(), reasoning_input)
    proposal = validate_decision_proposal(reasoning_input, output)
    decision = authorize_decision(
        proposal,
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T21:00:00Z",
    )
    command = build_execution_command(
        decision,
        command_type="replenishment",
        command_id="cmd-371-001",
    )

    assert command.context_id == "ctx-371"
    assert command.to_mapping() == {
        "contract_version": "S346.1",
        "command_id": "cmd-371-001",
        "command_type": "replenishment",
        "context_id": "ctx-371",
        "proposal": {"action": "replenish", "quantity": 10},
        "actor_id": "planner-1",
        "authority": "supply-chain-manager",
        "authorized_at": "2026-08-17T21:00:00Z",
        "evidence_ids": ["e-stock-1"],
        "provenance_ids": ["p-erp-1"],
    }
