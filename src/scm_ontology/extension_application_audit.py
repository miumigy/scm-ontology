from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ExtensionApplicationAudit:
    proposal_ref: str
    registry_version_before: str
    registry_version_after: str
    applied_at: datetime
    actor_ref: str
