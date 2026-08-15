from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .path_evidence import PathEvidence


class PathReasoningResultError(ValueError):
    pass


@dataclass(frozen=True)
class PathReasoningResult:
    result_ref: str
    status: str
    paths: tuple[PathEvidence, ...] = ()
    explanation: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.result_ref.strip():
            raise PathReasoningResultError("result_ref must be non-empty")
        if not self.status.strip():
            raise PathReasoningResultError("status must be non-empty")
        if not isinstance(self.metadata, Mapping):
            raise PathReasoningResultError("metadata must be a mapping")
        if any(not isinstance(path, PathEvidence) for path in self.paths):
            raise PathReasoningResultError("paths must contain PathEvidence values")
