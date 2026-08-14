from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Claim:
    """Canonical statement that may be supported or contradicted by evidence.

    A Claim is a semantic assertion, not an observed/derived fact and not an
    executable rule. Its references are intentionally lightweight so source
    systems and graph implementations remain outside the canonical contract.
    """

    claim_id: str
    subject_id: str
    predicate: str
    object_value: Any

    def __post_init__(self) -> None:
        if not self.claim_id:
            raise ValueError("claim_id must not be empty")
        if not self.subject_id:
            raise ValueError("subject_id must not be empty")
        if not self.predicate:
            raise ValueError("predicate must not be empty")
