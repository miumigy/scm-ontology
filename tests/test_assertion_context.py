import pytest

from scm_ontology.assertion_context import AssertionContext, ContextualRelation
from scm_ontology.core_instance import CanonicalRelation
from scm_ontology.semantic_context import EpistemicKind, SemanticContext


def context(relation_id: str = "rel:1") -> SemanticContext:
    return SemanticContext(
        assertion_ref=relation_id,
        subject_ref="material:1",
        epistemic_kind=EpistemicKind.OBSERVATION,
    )


def relation() -> CanonicalRelation:
    return CanonicalRelation("rel:1", "material:1", "stored_at", "site:1")


def test_relation_can_carry_semantic_context() -> None:
    contextual = ContextualRelation(relation(), AssertionContext("rel:1", context()))
    assert contextual.assertion_context.context.epistemic_kind is EpistemicKind.OBSERVATION


def test_context_must_match_relation_id() -> None:
    with pytest.raises(ValueError, match="assertion_ref"):
        AssertionContext("rel:1", context("rel:2"))


def test_contextual_relation_ids_must_match() -> None:
    with pytest.raises(ValueError, match="ids must match"):
        ContextualRelation(relation(), AssertionContext("rel:2", context("rel:2")))
