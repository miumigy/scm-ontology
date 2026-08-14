from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .validation import OntologyValidator, ValidationIssue


@dataclass(frozen=True)
class ValidationSummary:
    issues: tuple[ValidationIssue, ...]

    @property
    def is_valid(self) -> bool:
        return not self.issues


class SemanticModelValidator:
    """Validate canonical ontology documents across semantic boundary rules.

    S118 validates local ontology structure. S129 adds cross-layer semantic
    invariants that protect the canonical model from graph/source-model drift.
    """

    _FORBIDDEN_CONFLATIONS = {
        ("Measurement", "Metric"),
        ("Metric", "KPI"),
        ("KPI", "Target"),
        ("Target", "Actual"),
        ("Recommendation", "Decision"),
        ("Decision", "Action"),
        ("Observation", "Inference"),
        ("Forecast", "Actual"),
        ("Plan", "Actual"),
        ("Event", "State"),
        ("Location", "Node"),
        ("Lane", "Route"),
        ("Route", "Flow"),
    }

    def validate(self, document: dict[str, Any]) -> ValidationSummary:
        issues = list(OntologyValidator().validate(document))
        concepts = {c.get("name"): c for c in document.get("concepts", []) if c.get("name")}
        relationships = document.get("relationships", [])

        for index, relationship in enumerate(relationships):
            source = relationship.get("source")
            target = relationship.get("target")
            predicate = relationship.get("predicate")
            if (
                (source, target) in self._FORBIDDEN_CONFLATIONS
                and predicate in {"equals", "equivalent_to", "same_as"}
            ):
                issues.append(
                    ValidationIssue(
                        "SEMANTIC_CONFLATION",
                        f"'{source}' and '{target}' must remain distinct concepts.",
                        f"relationships[{index}]",
                    )
                )
            if source == target and predicate in {"equals", "equivalent_to", "same_as"}:
                issues.append(
                    ValidationIssue(
                        "SELF_EQUIVALENCE",
                        "A concept must not be declared equivalent to itself as a semantic relationship.",
                        f"relationships[{index}]",
                    )
                )

        for index, concept in enumerate(document.get("concepts", [])):
            name = concept.get("name")
            category = concept.get("category")
            if category == "derived" and name in {"Product", "Material", "Inventory", "Order", "Supply", "Capacity", "Demand"}:
                issues.append(
                    ValidationIssue(
                        "PRIMITIVE_DERIVED_MISMATCH",
                        f"Core operational concept '{name}' must not be classified as derived.",
                        f"concepts[{index}].category",
                    )
                )
            if category == "derived" and name in {"InventoryTurns", "DaysOfSupply", "ServiceLevel", "CapacityUtilization", "RiskScore"}:
                continue
            if name in concepts and concept.get("derived_from") and category != "derived":
                issues.append(
                    ValidationIssue(
                        "DERIVATION_CATEGORY_MISMATCH",
                        "A concept declaring derived_from should be classified as derived.",
                        f"concepts[{index}]",
                    )
                )

        return ValidationSummary(tuple(issues))

    def is_valid(self, document: dict[str, Any]) -> bool:
        return self.validate(document).is_valid
