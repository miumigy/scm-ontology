from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ClaimValidity:
    """Canonical interval for when a claim is semantically applicable."""

    valid_from: Optional[str] = None
    valid_to: Optional[str] = None

    def __post_init__(self) -> None:
        if self.valid_from is not None and not self.valid_from:
            raise ValueError("valid_from must not be empty")
        if self.valid_to is not None and not self.valid_to:
            raise ValueError("valid_to must not be empty")
