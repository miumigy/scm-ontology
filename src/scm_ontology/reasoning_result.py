from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .evidence_provenance import EvidenceSet


class ReasoningResultError(ValueError):
    pass


@dataclass(frozen=True)
class ReasoningResult:
    result_ref: str
    status: str
    matches: tuple[str, ...] = ()
    evidence: EvidenceSet = EvidenceSet()
    explanation: str | None = None
    metadata: Mapping[str, Any] = ()

    def __post_init__(self) -> None:
        if not self.result_ref.strip():
            raise ReasoningResultError("result_ref must be non-empty")
        if not self.status.strip():
            raise ReasoningResultError("status must be non-empty")
        if not isinstance(self.evidence, EvidenceSet):
            raise ReasoningResultError("evidence must be an EvidenceSet")
        if not isinstance(self.metadata, Mapping):
            raise ReasoningResultError("metadata must be a mapping")
