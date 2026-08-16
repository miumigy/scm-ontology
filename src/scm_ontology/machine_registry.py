"""Machine-readable Canonical Ontology registry loader and consistency checks."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .canonical_model import CANONICAL_CONCEPTS, CANONICAL_RELATIONSHIPS


class MachineRegistryError(ValueError):
    """Raised when the checked-in machine-readable registry is invalid."""


@dataclass(frozen=True)
class MachineRegistry:
    registry_id: str
    version: str
    status: str
    concepts: tuple[dict[str, Any], ...]
    relationships: tuple[dict[str, Any], ...]

    @classmethod
    def load(cls, path: str | Path | None = None) -> "MachineRegistry":
        registry_path = Path(path) if path is not None else _default_registry_path()
        payload = json.loads(registry_path.read_text(encoding="utf-8"))
        registry = cls(
            registry_id=payload["registryId"],
            version=payload["version"],
            status=payload["status"],
            concepts=tuple(payload["concepts"]),
            relationships=tuple(payload["relationships"]),
        )
        registry.validate()
        return registry

    def validate(self) -> None:
        concept_ids = [item["id"] for item in self.concepts]
        if len(concept_ids) != len(set(concept_ids)):
            raise MachineRegistryError("concept ids must be unique")

        names = set(concept_ids)
        predicates = [item["predicate"] for item in self.relationships]
        if len(predicates) != len(set(predicates)):
            raise MachineRegistryError("relationship predicates must be unique")

        for relationship in self.relationships:
            if relationship["source"] not in names or relationship["target"] not in names:
                raise MachineRegistryError("relationship endpoint is not a declared concept")

        if self.status not in {"reference", "draft", "deprecated"}:
            raise MachineRegistryError("unsupported registry status")

    def assert_matches_python_registry(self) -> None:
        python_concepts = {concept.name for concept in CANONICAL_CONCEPTS}
        machine_concepts = {concept["id"] for concept in self.concepts}
        if machine_concepts != python_concepts:
            raise MachineRegistryError("machine registry concepts drift from canonical_model")

        python_predicates = {relation.predicate for relation in CANONICAL_RELATIONSHIPS}
        machine_predicates = {relation["predicate"] for relation in self.relationships}
        if machine_predicates != python_predicates:
            raise MachineRegistryError("machine registry predicates drift from canonical_model")


def _default_registry_path() -> Path:
    return Path(__file__).resolve().parents[2] / "registry" / "canonical-registry.v0.2.json"


def load_canonical_registry(path: str | Path | None = None) -> MachineRegistry:
    return MachineRegistry.load(path)
