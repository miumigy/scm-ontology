"""Versioned request/response protocol for accountability queries."""
from __future__ import annotations
from dataclasses import dataclass
from .accountability_runtime import AccountabilityRuntime
from .end_to_end_accountability import EndToEndAccountability, trace_end_to_end_accountability
from .decision_accountability import DecisionAccountabilityNotFound

PROTOCOL_VERSION = "1.0.0"

@dataclass(frozen=True)
class AccountabilityQueryRequest:
    snapshot_id: str
    contract_version: str = PROTOCOL_VERSION

@dataclass(frozen=True)
class AccountabilityQueryResponse:
    contract_version: str
    status: str
    accountability: dict[str, object] | None = None
    error: str | None = None

def execute_accountability_query(
    request: AccountabilityQueryRequest,
    *,
    transitions,
    decisions,
    evidence_by_id,
    facts_by_evidence_id,
) -> AccountabilityQueryResponse:
    if request.contract_version != PROTOCOL_VERSION:
        return AccountabilityQueryResponse(PROTOCOL_VERSION, "contract_version_mismatch", error=request.contract_version)
    try:
        result = trace_end_to_end_accountability(
            transitions, decisions, snapshot_id=request.snapshot_id,
            evidence_by_id=evidence_by_id, facts_by_evidence_id=facts_by_evidence_id,
        )
    except (DecisionAccountabilityNotFound, LookupError) as exc:
        return AccountabilityQueryResponse(PROTOCOL_VERSION, "not_found", error=str(exc))
    return AccountabilityQueryResponse(PROTOCOL_VERSION, "resolved", AccountabilityRuntime().mapping(result))

def query_response_to_mapping(response: AccountabilityQueryResponse) -> dict[str, object]:
    payload: dict[str, object] = {"contract_version": response.contract_version, "status": response.status}
    if response.accountability is not None:
        payload["accountability"] = response.accountability
    if response.error is not None:
        payload["error"] = response.error
    return payload
