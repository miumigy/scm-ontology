"""Deterministic multi-hop supply-risk business-question boundary.

S329 consumes an already-canonical directed dependency graph and explicit risk
observations. It propagates risk only along declared edges; it does not infer
relationships, mutate the graph, optimize mitigations, or make operational
policy decisions.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Iterable


class MultiHopSupplyRiskError(ValueError):
    """Raised when an S329 input violates the canonical contract."""


@dataclass(frozen=True)
class SupplyDependency:
    upstream_id: str
    downstream_id: str
    dependency_type: str = "supplies"
    evidence_id: str | None = None
    provenance_id: str | None = None

    def __post_init__(self) -> None:
        if not self.upstream_id.strip() or not self.downstream_id.strip():
            raise MultiHopSupplyRiskError("upstream_id and downstream_id must be non-empty")
        if not self.dependency_type.strip():
            raise MultiHopSupplyRiskError("dependency_type must be non-empty")
        if self.upstream_id == self.downstream_id:
            raise MultiHopSupplyRiskError("self-dependencies are not allowed")


@dataclass(frozen=True)
class SupplyRiskObservation:
    node_id: str
    risk_score: float
    evidence_id: str | None = None
    provenance_id: str | None = None

    def __post_init__(self) -> None:
        if not self.node_id.strip():
            raise MultiHopSupplyRiskError("node_id must be non-empty")
        if not isinstance(self.risk_score, (int, float)) or isinstance(self.risk_score, bool):
            raise MultiHopSupplyRiskError("risk_score must be numeric")
        if not 0 <= self.risk_score <= 1:
            raise MultiHopSupplyRiskError("risk_score must be between 0 and 1")


@dataclass(frozen=True)
class MultiHopSupplyRisk:
    node_id: str
    risk_score: float
    hop_count: int
    path: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    provenance_ids: tuple[str, ...]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "risk_score": self.risk_score,
            "hop_count": self.hop_count,
            "path": list(self.path),
            "evidence_ids": list(self.evidence_ids),
            "provenance_ids": list(self.provenance_ids),
        }


def resolve_multi_hop_supply_risk(
    dependencies: Iterable[SupplyDependency],
    observations: Iterable[SupplyRiskObservation],
    *,
    max_hops: int = 5,
) -> tuple[MultiHopSupplyRisk, ...]:
    """Propagate the maximum upstream risk over explicit dependency paths.

    Risk is propagated without attenuation: the highest observed upstream risk
    reachable within ``max_hops`` is reported for each downstream node. This is
    a semantic observation, not a probability or a mitigation recommendation.
    """
    if max_hops < 1:
        raise MultiHopSupplyRiskError("max_hops must be >= 1")
    outgoing: dict[str, list[SupplyDependency]] = {}
    for dependency in dependencies:
        outgoing.setdefault(dependency.upstream_id, []).append(dependency)
    for edges in outgoing.values():
        edges.sort(key=lambda x: (x.downstream_id, x.dependency_type))
    observed = {x.node_id: x for x in observations}
    results: dict[tuple[str, tuple[str, ...]], MultiHopSupplyRisk] = {}
    queue: list[tuple[str, float, tuple[str, ...], tuple[str, ...], tuple[str, ...]]] = []
    for observation in sorted(observed.values(), key=lambda x: x.node_id):
        queue.append((observation.node_id, observation.risk_score, (observation.node_id,),
                      tuple(x for x in (observation.evidence_id,) if x),
                      tuple(x for x in (observation.provenance_id,) if x)))
    seen: set[tuple[str, tuple[str, ...]]] = set()
    while queue:
        node, score, path, evidence_ids, provenance_ids = queue.pop(0)
        state = (node, path)
        if state in seen or len(path) - 1 >= max_hops:
            continue
        seen.add(state)
        for edge in outgoing.get(node, []):
            downstream = edge.downstream_id
            if downstream in path:
                continue
            next_path = path + (downstream,)
            next_evidence = tuple(sorted(set(evidence_ids) | {edge.evidence_id} - {None}))
            next_provenance = tuple(sorted(set(provenance_ids) | {edge.provenance_id} - {None}))
            candidate = MultiHopSupplyRisk(downstream, score, len(next_path) - 1, next_path, next_evidence, next_provenance)
            key = (downstream, next_path)
            previous = results.get(key)
            if previous is None or candidate.risk_score > previous.risk_score:
                results[key] = candidate
            queue.append((downstream, score, next_path, next_evidence, next_provenance))
    return tuple(sorted(results.values(), key=lambda x: (x.node_id, x.hop_count, x.path)))


def multi_hop_supply_risk_to_mapping(result: Iterable[MultiHopSupplyRisk]) -> dict[str, Any]:
    return {"contract_version": "S329.1", "risks": [x.to_mapping() for x in result]}


def multi_hop_supply_risk_to_json(result: Iterable[MultiHopSupplyRisk]) -> str:
    return json.dumps(multi_hop_supply_risk_to_mapping(result), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
