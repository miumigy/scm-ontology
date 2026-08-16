"""Canonical vocabulary for SCM semantic capabilities."""
from __future__ import annotations
from dataclasses import dataclass

CANONICAL_CAPABILITIES: dict[str, str] = {
    "planning": "Plan supply-chain activities and decisions.",
    "execution": "Represent or coordinate execution of supply-chain actions.",
    "provenance": "Trace the origin and derivation of semantic assertions.",
    "learning": "Represent evidence and knowledge derived from observed outcomes.",
    "reasoning": "Represent semantic inference over the canonical supply-chain model.",
    "temporal": "Represent validity and change of supply-chain facts over time.",
}

@dataclass(frozen=True)
class CanonicalCapability:
    key: str
    description: str

def get_canonical_capability(key: str) -> CanonicalCapability:
    try:
        return CanonicalCapability(key, CANONICAL_CAPABILITIES[key])
    except KeyError as exc:
        raise ValueError(f"unknown canonical capability: {key}") from exc
