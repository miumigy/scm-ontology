"""Bindings between canonical SCM capabilities and Trace Bundle semantics."""
from __future__ import annotations
from dataclasses import dataclass
from .canonical_capabilities import CANONICAL_CAPABILITIES

CAPABILITY_BINDINGS: dict[str, frozenset[str]] = {
    "planning": frozenset({"decision_trace", "execution_request"}),
    "execution": frozenset({"execution_request", "execution_event"}),
    "provenance": frozenset({"reasoning_provenance", "validation"}),
    "learning": frozenset({"execution_event", "reasoning_provenance"}),
    "reasoning": frozenset({"decision_trace", "reasoning_provenance"}),
    "temporal": frozenset({"decision_trace", "execution_event", "validation"}),
}

@dataclass(frozen=True)
class CapabilityBinding:
    capability: str
    bundle_elements: frozenset[str]

def get_capability_binding(capability: str) -> CapabilityBinding:
    if capability not in CANONICAL_CAPABILITIES:
        raise ValueError(f"unknown canonical capability: {capability}")
    return CapabilityBinding(capability, CAPABILITY_BINDINGS[capability])
