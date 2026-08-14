from __future__ import annotations

from dataclasses import dataclass

from .canonical_model import (
    CANONICAL_CONCEPTS,
    CANONICAL_RELATIONSHIPS,
    ConceptLayer,
    RelationshipCategory,
    concept_names,
)


@dataclass(frozen=True)
class IntegrityIssue:
    code: str
    message: str


def audit_canonical_model() -> tuple[IntegrityIssue, ...]:
    issues: list[IntegrityIssue] = []

    concept_name_list = [concept.name for concept in CANONICAL_CONCEPTS]
    duplicates = sorted({name for name in concept_name_list if concept_name_list.count(name) > 1})
    issues.extend(
        IntegrityIssue("duplicate_concept", f"duplicate canonical concept: {name}")
        for name in duplicates
    )

    relationship_predicate_list = [relation.predicate for relation in CANONICAL_RELATIONSHIPS]
    duplicate_predicates = sorted(
        {predicate for predicate in relationship_predicate_list if relationship_predicate_list.count(predicate) > 1}
    )
    issues.extend(
        IntegrityIssue("duplicate_predicate", f"duplicate relationship predicate: {predicate}")
        for predicate in duplicate_predicates
    )

    names = concept_names()
    for relation in CANONICAL_RELATIONSHIPS:
        if relation.source not in names:
            issues.append(
                IntegrityIssue(
                    "unknown_source",
                    f"relationship {relation.predicate!r} has unknown source {relation.source!r}",
                )
            )
        if relation.target not in names:
            issues.append(
                IntegrityIssue(
                    "unknown_target",
                    f"relationship {relation.predicate!r} has unknown target {relation.target!r}",
                )
            )
        if not isinstance(relation.category, RelationshipCategory):
            issues.append(
                IntegrityIssue(
                    "invalid_category",
                    f"relationship {relation.predicate!r} has invalid category",
                )
            )

    derived_names = {
        concept.name for concept in CANONICAL_CONCEPTS if concept.layer is ConceptLayer.DERIVED
    }
    expected_derived = {"KPI", "PerformanceAssessment", "Variance", "RiskScore"}
    missing_derived = sorted(expected_derived - derived_names)
    for name in missing_derived:
        issues.append(
            IntegrityIssue("derived_classification", f"expected derived concept is missing: {name}")
        )

    required_boundaries = {
        "Recommendation",
        "Decision",
        "Action",
        "Execution",
        "Outcome",
        "Measurement",
        "LearningResult",
    }
    missing_boundaries = sorted(required_boundaries - names)
    for name in missing_boundaries:
        issues.append(
            IntegrityIssue("boundary_concept", f"required lifecycle concept is missing: {name}")
        )

    return tuple(issues)


def assert_canonical_model_integrity() -> None:
    issues = audit_canonical_model()
    if issues:
        details = "\n".join(f"[{issue.code}] {issue.message}" for issue in issues)
        raise AssertionError(f"canonical model integrity audit failed:\n{details}")
