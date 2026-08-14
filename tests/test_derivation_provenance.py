from scm_ontology.derivation_provenance import DerivationProvenance


def test_derivation_provenance_connects_rule_and_input_facts():
    provenance = DerivationProvenance(
        rule_id="R1",
        input_fact_ids=("F1", "F2"),
    )
    assert provenance.rule_id == "R1"
    assert provenance.input_fact_ids == ("F1", "F2")
    assert provenance.source_relationship_ids == ()


def test_derivation_provenance_can_reference_source_relationships():
    provenance = DerivationProvenance(
        rule_id="R1",
        input_fact_ids=("F1",),
        source_relationship_ids=("REL1", "REL2"),
    )
    assert provenance.source_relationship_ids == ("REL1", "REL2")


def test_empty_rule_is_rejected():
    try:
        DerivationProvenance("", ("F1",))
    except ValueError as exc:
        assert "rule_id" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_empty_source_identifier_is_rejected():
    try:
        DerivationProvenance("R1", ("F1", ""))
    except ValueError as exc:
        assert "input_fact_ids" in str(exc)
    else:
        raise AssertionError("expected ValueError")
