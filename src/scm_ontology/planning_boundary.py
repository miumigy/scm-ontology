"""Explicit boundary between semantic reasoning and planning engines."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any

from .auditable_reasoning import AuditableReasoningResult


@dataclass(frozen=True)
class PlanningRequest:
    request_id: str
    reasoning_result_id: str
    at: str
    source_node_id: str
    target_node_id: str
    objective: str
    constraints: dict[str, Any]


def build_planning_request(
    reasoning: AuditableReasoningResult,
    *,
    source_node_id: str,
    target_node_id: str,
    objective: str,
    constraints: dict[str, Any] | None = None,
) -> PlanningRequest:
    """Create a planning request without selecting or recommending a plan."""
    if reasoning.status != "feasible":
        raise ValueError("planning request requires a feasible reasoning result")
    if not objective.strip():
        raise ValueError("objective must be non-empty")
    if source_node_id not in reasoning.node_ids or target_node_id not in reasoning.node_ids:
        raise ValueError("planning endpoints must belong to the reasoning result path")
    normalized = {
        "reasoning_result_id": reasoning.result_id,
        "at": reasoning.at,
        "source_node_id": source_node_id,
        "target_node_id": target_node_id,
        "objective": objective,
        "constraints": constraints or {},
    }
    request_id = sha256(json.dumps(normalized, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return PlanningRequest(
        request_id=request_id,
        reasoning_result_id=reasoning.result_id,
        at=reasoning.at,
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        objective=objective,
        constraints=dict(constraints or {}),
    )


def planning_request_to_mapping(request: PlanningRequest) -> dict[str, Any]:
    return {
        "request_id": request.request_id,
        "reasoning_result_id": request.reasoning_result_id,
        "at": request.at,
        "source_node_id": request.source_node_id,
        "target_node_id": request.target_node_id,
        "objective": request.objective,
        "constraints": dict(request.constraints),
    }
