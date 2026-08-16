"""Temporal selection rules for provenance-bearing SCM facts."""
from __future__ import annotations
from datetime import datetime
from .fact_provenance import ProvenancedFact

def _parse(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None

def is_valid_at(fact: ProvenancedFact, at: str) -> bool:
    point = _parse(at)
    if point is None:
        return False
    p = fact.provenance
    start = _parse(p.valid_from)
    end = _parse(p.valid_to)
    return (start is None or point >= start) and (end is None or point < end)

def select_valid_facts(facts: tuple[ProvenancedFact, ...], *, at: str) -> tuple[ProvenancedFact, ...]:
    return tuple(fact for fact in facts if is_valid_at(fact, at))
