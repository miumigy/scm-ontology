"""Canonical provenance primitives for derived semantic facts."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Provenance:
    """Machine-readable evidence for a derived semantic fact."""

    rule_id: str
    source_relationship_ids: Tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.rule_id:
            raise ValueError("rule_id must not be empty")
        if not self.source_relationship_ids:
            raise ValueError("source_relationship_ids must not be empty")
        if any(not value for value in self.source_relationship_ids):
            raise ValueError("source relationship ids must not be empty")


@dataclass(frozen=True)
class ExplanationStep:
    """One deterministic semantic explanation step."""

    statement: str

    def __post_init__(self) -> None:
        if not self.statement:
            raise ValueError("statement must not be empty")


@dataclass(frozen=True)
class SemanticExplanation:
    """Structured explanation without prescribing natural-language generation."""

    steps: Tuple[ExplanationStep, ...]

    def __post_init__(self) -> None:
        if not self.steps:
            raise ValueError("steps must not be empty")
