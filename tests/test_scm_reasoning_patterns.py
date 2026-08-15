import pytest

from scm_ontology.scm_reasoning_patterns import (
    DEFAULT_SCM_REASONING_PATTERNS,
    SCMReasoningPattern,
    SCMReasoningPatternError,
    SITE_DEPENDENCY,
    SUPPLY_DEPENDENCY,
)


def test_default_patterns_are_transport_neutral() -> None:
    assert SUPPLY_DEPENDENCY.path_predicates == ("depends_on", "supplied_by")
    assert SITE_DEPENDENCY.path_predicates == ("supplied_by", "located_at")
    assert len(DEFAULT_SCM_REASONING_PATTERNS) == 3


def test_pattern_requires_a_path() -> None:
    with pytest.raises(SCMReasoningPatternError):
        SCMReasoningPattern("x", "Invalid", "", ())
