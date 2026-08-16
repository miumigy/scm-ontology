"""Deterministic propagation of explicit network disruption observations.

S331 traverses only declared directed dependencies. It does not infer graph
relationships, mutate Canonical Truth, or recommend mitigation actions.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Iterable


class NetworkDisruptionError(ValueError):
    """Raised when an S331 input violates the canonical contract."""


@dataclass(frozen=True)
class DisruptionObservation:
    node_id: str
    severity: float
    evidence_id: str | None = None
    provenance_id: str | None = None

    def __post_init__(self) -> None:
        if not self.node_id.strip():
            raise NetworkDisruptionError("node_id must be non-empty")
        if not isinstance(self.severity, (int, float)) or isinstance(self.severity, bool):
            raise NetworkDisruptionError("severity must be numeric")
        if not 0 <= self.severity <= 1:
            raise NetworkDisruptionError("severity must be between 0 and 1")


@dataclass(frozen=True)
class DisruptionDependency:
    upstream_node_id: str
    downstream_node_id: str
    propagation_factor: float = 1.0

    def __post_init__(self) -> None:
        if not self.upstream_node_id.strip() or not self.downstream_node_id.strip():
            raise NetworkDisruptionError("dependency node ids must be non-empty")
        if self.upstream_node_id == self.downstream_node_id:
            raise NetworkDisruptionError("self-dependency is not allowed")
        if not isinstance(self.propagation_factor, (int, float)) or isinstance(self.propagation_factor, bool):
            raise NetworkDisruptionError("propagation_factor must be numeric")
        if not 0 <= self.propagation_factor <= 1:
            raise NetworkDisruptionError("propagation_factor must be between 0 and 1")


@dataclass(frozen=True)
class DisruptionImpact:
    source_node_id: str
    affected_node_id: str
    hop_count: int
    impact_score: float
    path: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    provenance_ids: tuple[str, ...]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "source_node_id": self.source_node_id,
            "affected_node_id": self.affected_node_id,
            "hop_count": self.hop_count,
            "impact_score": self.impact_score,
            "path": list(self.path),
            "evidence_ids": list(self.evidence_ids),
            "provenance_ids": list(self.provenance_ids),
        }


def resolve_network_disruption_propagation(
    observations: Iterable[DisruptionObservation],
    dependencies: Iterable[DisruptionDependency],
    *,
    max_hops: int = 5,
) -> tuple[DisruptionImpact, ...]:
    """Propagate explicit disruption severity over declared directed paths."""
    if max_hops < 1:
        raise NetworkDisruptionError("max_hops must be >= 1")

    adjacency: dict[str, list[DisruptionDependency]] = {}
    for dependency in dependencies:
        adjacency.setdefault(dependency.upstream_node_id, []).append(dependency)
    for edges in adjacency.values():
        edges.sort(key=lambda edge: (edge.downstream_node_id, edge.propagation_factor))

    results: list[DisruptionImpact] = []
    for observation in sorted(observations, key=lambda item: item.node_id):
        evidence_ids = (observation.evidence_id,) if observation.evidence_id else ()
        provenance_ids = (observation.provenance_id,) if observation.provenance_id else ()
        frontier: list[tuple[str, float, tuple[str, ...]]] = [(observation.node_id, observation.severity, (observation.node_id,))]
        visited: set[tuple[str, tuple[str, ...]]] = set()

        while frontier:
            node_id, score, path = frontier.pop(0)
            if len(path) - 1 >= max_hops:
                continue
            for edge in adjacency.get(node_id, []):
                if edge.downstream_node_id in path:
                    continue
                next_score = score * edge.propagation_factor
                next_path = path + (edge.downstream_node_id,)
                state = (edge.downstream_node_id, next_path)
                if state in visited:
                    continue
                visited.add(state)
                results.append(
                    DisruptionImpact(
                        source_node_id=observation.node_id,
                        affected_node_id=edge.downstream_node_id,
                        hop_count=len(next_path) - 1,
                        impact_score=next_score,
                        path=next_path,
                        evidence_ids=evidence_ids,
                        provenance_ids=provenance_ids,
                    )
                )
                frontier.append((edge.downstream_node_id, next_score, next_path))

    return tuple(sorted(results, key=lambda item: (item.source_node_id, item.hop_count, item.path)))


def network_disruption_to_mapping(result: Iterable[DisruptionImpact]) -> dict[str, Any]:
    return {"contract_version": "S331.1", "impacts": [item.to_mapping() for item in result]}


def network_disruption_to_json(result: Iterable[DisruptionImpact]) -> str:
    return json.dumps(network_disruption_to_mapping(result), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
