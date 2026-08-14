from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Observation:
    """Canonical reference to an observation at a point in time."""

    observation_id: str
    observed_at: datetime
    subject_id: str

    def __post_init__(self) -> None:
        if not self.observation_id:
            raise ValueError("observation_id must not be empty")
        if not self.subject_id:
            raise ValueError("subject_id must not be empty")
