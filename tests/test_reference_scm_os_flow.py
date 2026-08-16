from scm_ontology.decision_context import DecisionObservation
from scm_ontology.decision_proposal import DecisionProposal
from scm_ontology.reference_canonicalization import SourceMapping
from scm_ontology.reference_scm_os_flow import (
    ReferenceFlowError,
    ReferenceFlowInput,
    reference_flow_to_json,
    run_reference_flow,
)


def request() -> ReferenceFlowInput:
    return ReferenceFlowInput(
        source_record={"sku": "東京-A", "qty": 12},
        source_mapping=SourceMapping("wms-fixture", (("sku", "item_id"), ("qty", "quantity"))),
        context_id="ctx-001",
        question_id="inventory-position",
        decision_id="dec-001",
        decision_type="review",
        action={"type": "review_inventory"},
        rationale="Canonical inventory observation requires review.",
        evidence_ids=("ev-2", "ev-1"),
        provenance_ids=("prov-2", "prov-1"),
    )


def test_reference_flow_composes_s335_s333_s334():
    result = run_reference_flow(request())
    assert result.canonical_record["canonical"] == {"item_id": "東京-A", "quantity": 12}
    assert result.context.context_id == "ctx-001"
    assert result.context.observations[0].question_id == "inventory-position"
    assert result.proposal.context_id == "ctx-001"


def test_reference_flow_is_deterministic_and_utf8_safe():
    result = run_reference_flow(request())
    first = reference_flow_to_json(result)
    second = reference_flow_to_json(result)
    assert first == second
    assert "東京-A" in first
    assert first.index('"canonical_record"') < first.index('"decision_context"') < first.index('"decision_proposal"')


def test_reference_flow_fails_closed_before_context_or_proposal():
    bad = request()
    bad = ReferenceFlowInput(
        source_record={"sku": "東京-A"},
        source_mapping=bad.source_mapping,
        context_id=bad.context_id,
        question_id=bad.question_id,
        decision_id=bad.decision_id,
        decision_type=bad.decision_type,
        action=bad.action,
        rationale=bad.rationale,
    )
    try:
        run_reference_flow(bad)
    except ReferenceFlowError:
        return
    raise AssertionError("canonicalization failure must stop the flow")
