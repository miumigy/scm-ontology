"""Dataset loading and semantic validation helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .graph import GraphValidator


def load_dataset(path: str | Path) -> dict[str, Any]:
    """Load a YAML graph dataset."""
    with Path(path).open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError("Dataset root must be a mapping")
    return data


def validate_dataset(
    dataset: dict[str, Any],
    *,
    ontology_dir: str | Path = "ontology",
) -> list[str]:
    """Return semantic graph validation errors for a dataset."""
    validator = GraphValidator(ontology_dir)
    return validator.validate(dataset)
