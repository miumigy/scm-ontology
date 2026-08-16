"""Canonical accountability query from a decision to its supporting evidence."""
from __future__ import annotations
from dataclasses import dataclass
from .semantic_runtime import DecisionTrace


class EvidenceRecord(dict):
    """JSON-compatible evidence value carrying its canonical evidence identifier."""

    def __init__(self, evidence_id: str, value: object) -> None:
        self.evidence_id = evidence_id
        if isinstance(value, dict):
            super().__init__(value)
        else:
            super().__init__({"value": value})


@dataclass(frozen=True)
class EvidenceAccountability:
    decision_id: str
    evidence: tuple[EvidenceRecord, ...] | object

    @property
    def evidence_id(self) -> str:
        """Return the canonical evidence identifier for this accountability result."""
        # Current tracing stores one or more EvidenceRecord values.
        if isinstance(self.evidence, tuple):
            if len(self.evidence) != 1:
                raise AttributeError("evidence_id is only defined for a single evidence record")
            return self.evidence[0].evidence_id
        # Keep compatibility with the original two-argument evidence contract,
        # where the first field itself was the evidence identifier.
        return self.decision_id


class EvidenceAccountabilityNotFound(LookupError):
    pass


def trace_evidence_accountability(
    decision: DecisionTrace, *, evidence_by_id: dict[str, object]
) -> EvidenceAccountability:
    missing = [item for item in decision.evidence if item not in evidence_by_id]
    if missing:
        raise EvidenceAccountabilityNotFound(", ".join(missing))
    records = tuple(EvidenceRecord(item, evidence_by_id[item]) for item in decision.evidence)
    return EvidenceAccountability(decision.decision_id, records)
