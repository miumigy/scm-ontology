from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


class EvidenceProvenanceError(ValueError):
    pass


@dataclass(frozen=True)
class EvidenceRef:
    source_ref: str
    observed_at: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.source_ref.strip():
            raise EvidenceProvenanceError("source_ref must be non-empty")
        if not isinstance(self.metadata, Mapping):
            raise EvidenceProvenanceError("metadata must be a mapping")


@dataclass(frozen=True)
class EvidenceSet:
    refs: tuple[EvidenceRef, ...] = ()

    def __post_init__(self) -> None:
        source_refs = [ref.source_ref for ref in self.refs]
        if len(source_refs) != len(set(source_refs)):
            raise EvidenceProvenanceError("source_ref must be unique within an evidence set")
