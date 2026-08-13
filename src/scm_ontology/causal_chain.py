"""Deterministic multi-hop causal event chain evaluation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .causal import CausalRule, CausalRuleSet, derive_event
from .simulation import Event, SimulationError


class CausalChainError(SimulationError):
    """Raised when a causal chain violates its semantic contract."""


@dataclass(frozen=True)
class CausalChain:
    """Auditable ordered chain of causally derived events."""

    events: tuple[Event, ...]
    rules: tuple[str, ...]

    @property
    def terminal_event(self) -> Event:
        return self.events[-1]

    @property
    def depth(self) -> int:
        return len(self.events) - 1


def propagate_chain(
    source_event: Event,
    rules: CausalRuleSet,
    event_ids: Mapping[int, str],
    max_depth: int = 10,
) -> CausalChain:
    """Propagate matching causal rules deterministically without mutating State."""
    if max_depth < 0:
        raise CausalChainError("max_depth must be non-negative")

    events = [source_event]
    applied_rules: list[str] = []
    current = source_event
    seen_signatures: set[tuple[str, str]] = set()

    for depth in range(1, max_depth + 1):
        matches = rules.matching(current)
        if not matches:
            break
        if len(matches) > 1:
            raise CausalChainError(
                f"ambiguous causal rules for event type {current.event_type}"
            )

        rule: CausalRule = matches[0]
        signature = (current.event_type, rule.rule_id)
        if signature in seen_signatures:
            raise CausalChainError(f"causal cycle detected at rule {rule.rule_id}")
        seen_signatures.add(signature)

        event_id = event_ids.get(depth)
        if not event_id:
            raise CausalChainError(f"missing deterministic event id for depth {depth}")
        current = derive_event(current, rule, event_id=event_id)
        events.append(current)
        applied_rules.append(rule.rule_id)

    return CausalChain(tuple(events), tuple(applied_rules))
