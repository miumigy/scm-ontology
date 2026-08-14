from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Constraint:
    """Canonical constraint: a condition that restricts what is allowed."""

    constraint_id: str
    subject: str
    operator: str
    value: Any


@dataclass(frozen=True)
class Policy:
    """Canonical policy: a preference or direction for selecting behavior."""

    policy_id: str
    subject: str
    directive: str
    value: Any
