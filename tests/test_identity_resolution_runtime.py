from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.identity_resolution_runtime import (
    DecisionOutcome,
    IdentityCandidate,
    IdentityDecision,
    IdentityEvidence,
    IdentityRecord,
    IdentityResolutionError,
    IdentityResolutionPolicy,
    IdentityResolutionRun,
    IdentityResolver,
    IdentitySignal,
    ResolutionOutcome,
    reference_identity_records,
    run_reference_identity_path,
)
from scm_ontology.mapping_canonicalization_runtime import (
    CanonicalizationResult,
    MappingState,
)

POLICY = IdentityResolutionPolicy(policy_id="p", policy_version="P7C.1")


def _record(source, ident, ref, gtin):
    return IdentityRecord(
        source_system=source,
        source_identity=ident,
        canonical_entity_ref=ref,
        canonical_attributes={"gtin": gtin},
        provenance=f"{source}:{ident}",
    )


def _resolve(*records):
    return IdentityResolver(POLICY).identify(records, decision_at="2026-08-19T10:00:00Z")


def test_reference_path_matches_across_sources_deterministically():
    first = run_reference_identity_path()
    second = run_reference_identity_path()
    assert first.matched_count == 1
    assert first.to_json() == second.to_json()
    matched = [c for c in first.candidates if c.outcome == ResolutionOutcome.MATCHED]
    assert len(matched) == 1
    assert matched[0].canonical_entity_ref == "Material:MAT-1000"
    assert matched[0].confidence == 1.0
    for decision in first.decisions:
        assert decision.canonical_mutation is False


def test_matched_candidate_is_accepted_and_not_mutating():
    run = _resolve(
        _record("erp", "a", "Material:X", "G"),
        _record("wms", "b", "Material:X", "G"),
    )
    matched = run.candidates[0]
    assert matched.outcome == ResolutionOutcome.MATCHED
    assert matched.canonical_entity_ref == "Material:X"
    assert any(d.outcome == DecisionOutcome.ACCEPTED for d in run.decisions)
    for decision in run.decisions:
        assert decision.canonical_mutation is False


def test_conflicting_key_points_to_different_canonical_entities():
    run = _resolve(
        _record("erp", "a", "Material:A", "G"),
        _record("wms", "b", "Material:B", "G"),
    )
    conflict = run.candidates[0]
    assert conflict.outcome == ResolutionOutcome.CONFLICT
    assert conflict.canonical_entity_ref is None
    assert any(d.outcome == DecisionOutcome.CONFLICTING for d in run.decisions)


def test_ambiguous_when_multiple_records_share_key_on_one_source():
    run = _resolve(
        _record("erp", "a1", "Material:X", "G"),
        _record("erp", "a2", "Material:X", "G"),
        _record("wms", "b", "Material:X", "G"),
    )
    assert ResolutionOutcome.AMBIGUOUS in {c.outcome for c in run.candidates}


def test_not_matched_when_key_is_single_source_only():
    run = _resolve(_record("erp", "a", "Material:X", "GAN"))
    nm = run.candidates[0]
    assert nm.outcome == ResolutionOutcome.NOT_MATCHED
    assert nm.confidence == 0.0


def test_unresolved_when_identity_signal_missing_or_blank():
    missing = _record("erp", "a", "Material:X", None)
    blank = IdentityRecord(
        source_system="erp", source_identity="b", canonical_entity_ref="Material:Y",
        canonical_attributes={"gtin": "  "}, provenance="p",
    )
    run = _resolve(missing, blank)
    assert all(c.outcome == ResolutionOutcome.UNRESOLVED for c in run.candidates)
    assert run.unresolved_count == 2


def test_evidence_is_attribute_and_preserved():
    run = _resolve(
        _record("erp", "a", "Material:X", "G"),
        _record("wms", "b", "Material:X", "G"),
    )
    candidate = run.candidates[0]
    assert len(candidate.evidence) == 2
    for evidence in candidate.evidence:
        assert evidence.signal == "gtin"
        assert evidence.value == "G"
        assert evidence.provenance


def test_decisions_form_append_only_chain():
    run = _resolve(
        _record("erp", "a", "Material:X", "G"),
        _record("wms", "b", "Material:X", "G"),
        _record("tms", "c", "Shipment:C", "H"),
    )
    ids = [d.decision_id for d in run.decisions]
    assert len(ids) == len(set(ids))
    for index, decision in enumerate(run.decisions[1:], start=1):
        assert decision.prev_decision_id == run.decisions[index - 1].decision_id


def test_from_canonicalization_rejects_unmapped():
    mapped = CanonicalizationResult(
        result_id="r", source_system="erp", source_location="loc", scope="s",
        decision_state=MappingState.MAPPED,
        canonical_type="Material", canonical_target="MAT-1",
        canonical_attributes={"materialId": "MAT-1"},
        mapping_confidence=1.0, provenance="p", reason="r",
        mapping_rule_id="R", adapter_version="A",
    )
    record = IdentityRecord.from_canonicalization(mapped)
    assert record.canonical_entity_ref == "MAT-1"
    gap = CanonicalizationResult(
        result_id="r", source_system="erp", source_location="loc", scope="s",
        decision_state=MappingState.UNMAPPABLE, mapping_confidence=None,
        provenance="p", reason="r", mapping_rule_id="R", adapter_version="A",
    )
    with pytest.raises(IdentityResolutionError, match="unmapped"):
        IdentityRecord.from_canonicalization(gap)


def test_policy_fails_closed():
    with pytest.raises(IdentityResolutionError, match="policy_id"):
        IdentityResolutionPolicy(policy_id=" ", policy_version="v")
    with pytest.raises(IdentityResolutionError, match="at least one"):
        IdentityResolutionPolicy(policy_id="p", policy_version="v", signals=())
    with pytest.raises(IdentityResolutionError, match="unique"):
        IdentityResolutionPolicy(
            policy_id="p", policy_version="v", signals=(IdentitySignal("a"), IdentitySignal("a")),
        )


def test_canonical_mutation_forbidden():
    with pytest.raises(IdentityResolutionError, match="must not mutate"):
        IdentityDecision(
            decision_id="d", outcome=DecisionOutcome.ACCEPTED, policy_id="p",
            policy_version="v", candidate_id="c", decision_at="t",
            canonical_mutation=True,
        )


def test_record_fails_closed():
    with pytest.raises(IdentityResolutionError, match="source_system"):
        _record(" ", "a", "Material:X", "G")
    with pytest.raises(IdentityResolutionError, match="canonical_entity_ref"):
        _record("erp", "a", " ", "G")
