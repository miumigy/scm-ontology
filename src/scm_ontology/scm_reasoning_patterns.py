from __future__ import annotations

from dataclasses import dataclass


class SCMReasoningPatternError(ValueError):
    pass


@dataclass(frozen=True)
class SCMReasoningPattern:
    pattern_id: str
    name: str
    description: str
    path_predicates: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.pattern_id.strip() or not self.name.strip():
            raise SCMReasoningPatternError("pattern_id and name must be non-empty")
        if not self.path_predicates:
            raise SCMReasoningPatternError("path_predicates must not be empty")
        if any(not predicate.strip() for predicate in self.path_predicates):
            raise SCMReasoningPatternError("path_predicates must contain non-empty values")


SUPPLY_DEPENDENCY = SCMReasoningPattern(
    "supply_dependency",
    "Supply Dependency",
    "Trace a product or material dependency through its supplying organization or site.",
    ("depends_on", "supplied_by"),
)

SITE_DEPENDENCY = SCMReasoningPattern(
    "site_dependency",
    "Site Dependency",
    "Trace a supply dependency through a supplier to a physical site.",
    ("supplied_by", "located_at"),
)

FLOW_DEPENDENCY = SCMReasoningPattern(
    "flow_dependency",
    "Flow Dependency",
    "Trace a material or product flow between physical nodes.",
    ("moves", "from", "to"),
)

DEFAULT_SCM_REASONING_PATTERNS = (
    SUPPLY_DEPENDENCY,
    SITE_DEPENDENCY,
    FLOW_DEPENDENCY,
)
