"""Capability negotiation for SCM semantic contract consumers."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CapabilitySet:
    supported_schema_versions: frozenset[str]
    features: frozenset[str]

@dataclass(frozen=True)
class CapabilityNegotiation:
    compatible_versions: tuple[str, ...]
    shared_features: tuple[str, ...]
    compatible: bool

def negotiate_capabilities(producer: CapabilitySet, consumer: CapabilitySet) -> CapabilityNegotiation:
    versions = tuple(sorted(producer.supported_schema_versions & consumer.supported_schema_versions))
    features = tuple(sorted(producer.features & consumer.features))
    return CapabilityNegotiation(versions, features, bool(versions))
