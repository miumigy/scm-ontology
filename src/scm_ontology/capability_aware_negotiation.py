"""Capability-aware negotiation over the canonical SCM semantic surface."""
from __future__ import annotations
from dataclasses import dataclass
from .capability_bindings import get_capability_binding
from .capability_negotiation import CapabilitySet, negotiate_capabilities

@dataclass(frozen=True)
class SemanticNegotiation:
    compatible_versions: tuple[str, ...]
    shared_capabilities: tuple[str, ...]
    shared_semantic_elements: tuple[str, ...]
    compatible: bool

def negotiate_semantic_surface(producer: CapabilitySet, consumer: CapabilitySet) -> SemanticNegotiation:
    base = negotiate_capabilities(producer, consumer)
    shared = tuple(sorted(producer.features & consumer.features))
    elements: set[str] = set()
    for capability in shared:
        elements.update(get_capability_binding(capability).bundle_elements)
    return SemanticNegotiation(base.compatible_versions, shared, tuple(sorted(elements)), base.compatible)
