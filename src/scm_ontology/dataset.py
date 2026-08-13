"""Dataset loading and semantic validation helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .graph import validate_graph_dataset

ROOT = Path(__file__).resolve().parents[2]


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
    """Validate an in-memory dataset using the canonical graph validator.

    The lower-level validator currently accepts paths. This API serializes the
    supplied dataset to a temporary YAML file so callers do not need to know
    the validator's file-based contract.
    """
    import tempfile

    ontology_dir = Path(ontology_dir)
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", encoding="utf-8", delete=False
    ) as handle:
        yaml.safe_dump(dataset, handle, sort_keys=False)
        dataset_path = Path(handle.name)

    try:
        return validate_graph_dataset(
            dataset_path,
            ontology_dir / "relationships.yaml",
            ontology_dir / "entities.yaml",
        )
    finally:
        dataset_path.unlink(missing_ok=True)
