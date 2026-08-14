from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceReference:
    """Canonical reference to a source supporting a semantic claim."""

    evidence_id: str
    evidence_type: str
    reference: str

    def __post_init__(self) -> None:
        if not self.evidence_id:
            raise ValueError("evidence_id must not be empty")
        if not self.evidence_type:
            raise ValueError("evidence_type must not be empty")
        if not self.reference:
            raise ValueError("reference must not be empty")
