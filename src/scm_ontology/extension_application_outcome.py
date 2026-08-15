from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ExtensionApplicationOutcomeKind(str, Enum):
    APPLIED = "applied"
    REJECTED = "rejected"
    ROLLED_BACK = "rolled_back"


@dataclass(frozen=True)
class ExtensionApplicationOutcome:
    kind: ExtensionApplicationOutcomeKind
    reason_ref: str | None = None
    transaction_ref: str | None = None


def rejected_application(reason_ref: str) -> ExtensionApplicationOutcome:
    return ExtensionApplicationOutcome(
        kind=ExtensionApplicationOutcomeKind.REJECTED,
        reason_ref=reason_ref,
    )


def rolled_back_application(
    reason_ref: str,
    transaction_ref: str,
) -> ExtensionApplicationOutcome:
    return ExtensionApplicationOutcome(
        kind=ExtensionApplicationOutcomeKind.ROLLED_BACK,
        reason_ref=reason_ref,
        transaction_ref=transaction_ref,
    )
