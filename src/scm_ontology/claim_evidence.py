from dataclasses import dataclass


@dataclass(frozen=True)
class ClaimEvidenceRelationship:
    """Canonical semantic link from a claim to supporting evidence."""

    relationship_id: str
    claim_id: str
    predicate: str
    evidence_id: str

    def __post_init__(self) -> None:
        if not self.relationship_id:
            raise ValueError("relationship_id must not be empty")
        if not self.claim_id:
            raise ValueError("claim_id must not be empty")
        if not self.predicate:
            raise ValueError("predicate must not be empty")
        if not self.evidence_id:
            raise ValueError("evidence_id must not be empty")
