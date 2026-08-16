"""S336 reference end-to-end SCM OS flow.

This orchestration composes existing S335, S333, and S334 contracts without
creating new canonical semantics or executing a decision.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping
import json

from .decision_context import DecisionContext, DecisionObservation, build_decision_context
from .decision_proposal import DecisionProposal
from .reference_canonicalization import SourceMapping, canonicalize_record


class ReferenceFlowError(ValueError):
    """Raised when the reference flow cannot safely proceed."""


@dataclass(frozen=True)
class ReferenceFlowInput:
    source_record: Mapping[str, Any]
    source_mapping: SourceMapping
    context_id: str
    question_id: str
    decision_id: str
    decision_type: str
    action: Any
    rationale: str
    evidence_ids: tuple[str, ...] = ()
    provenance_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class ReferenceFlowResult:
    canonical_record: dict[str, Any]
    context: DecisionContext
    proposal: DecisionProposal


def run_reference_flow(request: ReferenceFlowInput) -> ReferenceFlowResult:
    """Run the governed reference flow; canonicalization failure stops the flow."""
    try:
        canonical = canonicalize_record(request.source_record, request.source_mapping)
    except Exception as exc:
        raise ReferenceFlowError("reference flow stopped at canonicalization") from exc

    observation = DecisionObservation(
        question_id=request.question_id,
        value=canonical["canonical"],
        evidence_ids=request.evidence_ids,
        provenance_ids=request.provenance_ids,
    )
    context = build_decision_context(request.context_id, (observation,))
    proposal = DecisionProposal(
        decision_id=request.decision_id,
        decision_type=request.decision_type,
        context_id=context.context_id,
        action=request.action,
        rationale=request.rationale,
        evidence_ids=request.evidence_ids,
        provenance_ids=request.provenance_ids,
    )
    return ReferenceFlowResult(canonical, context, proposal)


def reference_flow_to_json(result: ReferenceFlowResult) -> str:
    """Serialize the complete reference flow deterministically as UTF-8 JSON."""
    payload = {
        "contract_version": "S336.1",
        "canonical_record": result.canonical_record,
        "decision_context": {"contract_version": "S333.1", **result.context.to_mapping()},
        "decision_proposal": {"contract_version": "S334.1", **result.proposal.to_mapping()},
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
