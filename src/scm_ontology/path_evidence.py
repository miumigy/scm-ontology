from __future__ import annotations

from dataclasses import dataclass

from .evidence_provenance import EvidenceRef, EvidenceSet
from .relation_path_query import RelationPathMatch


class PathEvidenceError(ValueError):
    pass


@dataclass(frozen=True)
class PathEvidence:
    path: RelationPathMatch
    evidence: EvidenceSet


def attach_path_evidence(
    path: RelationPathMatch,
    evidence: EvidenceSet,
) -> PathEvidence:
    """Attach transport-neutral provenance to an existing relation path."""
    return PathEvidence(path=path, evidence=evidence)


def evidence_from_sources(path: RelationPathMatch, source_refs: tuple[str, ...]) -> PathEvidence:
    refs = tuple(EvidenceRef(source_ref) for source_ref in source_refs)
    return attach_path_evidence(path, EvidenceSet(refs=refs))
