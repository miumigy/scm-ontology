"""Reusable empirical evidence derived from traced plan/actual variances."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .plan_actual import PlanActualComparison


@dataclass(frozen=True)
class LearningEvidence:
    metric: str
    sample_count: int
    mean_variance: float | None
    min_variance: float | None
    max_variance: float | None
    status: str
    source_event_ids: tuple[str, ...]


def derive_learning_evidence(comparisons: Iterable[PlanActualComparison]) -> tuple[LearningEvidence, ...]:
    """Aggregate only observed numeric variances; no missing values are imputed."""
    grouped: dict[str, list[tuple[float, str]]] = {}
    for comparison in comparisons:
        for variance in comparison.variances:
            if variance.variance is not None and isinstance(variance.variance, (int, float)):
                grouped.setdefault(variance.metric, []).append((float(variance.variance), comparison.execution_event_id))
    evidence: list[LearningEvidence] = []
    for metric in sorted(grouped):
        samples = grouped[metric]
        values = [value for value, _ in samples]
        mean = sum(values) / len(values)
        status = "persistent_positive_variance" if mean > 0 else ("persistent_negative_variance" if mean < 0 else "on_target")
        evidence.append(LearningEvidence(metric, len(values), mean, min(values), max(values), status, tuple(event_id for _, event_id in samples)))
    return tuple(evidence)


def learning_evidence_to_mapping(evidence: Iterable[LearningEvidence]) -> dict[str, Any]:
    return {"evidence": [{"metric": x.metric, "sample_count": x.sample_count, "mean_variance": x.mean_variance, "min_variance": x.min_variance, "max_variance": x.max_variance, "status": x.status, "source_event_ids": list(x.source_event_ids)} for x in evidence]}
