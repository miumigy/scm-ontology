import pytest

from scm_ontology.causal import CausalRule, CausalRuleSet
from scm_ontology.causal_chain import CausalChainError, propagate_chain
from scm_ontology.simulation import Event


def rules():
    return CausalRuleSet(
        (
            CausalRule("R1", "SUPPLIER_DELAY", "MATERIAL_SHORTAGE"),
            CausalRule("R2", "MATERIAL_SHORTAGE", "PRODUCTION_DELAY"),
            CausalRule("R3", "PRODUCTION_DELAY", "SHIPMENT_DELAY"),
        )
    )


def source():
    return Event("E0", "SUPPLIER_DELAY", 1, "SUP-A", {"magnitudeDays": 7})


def test_multi_hop_chain_is_deterministic_and_preserves_lineage():
    chain = propagate_chain(
        source(), rules(), {1: "E1", 2: "E2", 3: "E3"}, max_depth=5
    )
    assert [e.event_type for e in chain.events] == [
        "SUPPLIER_DELAY",
        "MATERIAL_SHORTAGE",
        "PRODUCTION_DELAY",
        "SHIPMENT_DELAY",
    ]
    assert chain.rules == ("R1", "R2", "R3")
    assert chain.depth == 3
    assert chain.terminal_event.event_id == "E3"
    assert chain.events[1].provenance.caused_by_event_id == "E0"
    assert chain.events[2].provenance.caused_by_event_id == "E1"
    assert chain.events[3].provenance.caused_by_event_id == "E2"


def test_chain_rejects_ambiguous_rule():
    ambiguous = CausalRuleSet(
        (
            CausalRule("R1", "SUPPLIER_DELAY", "MATERIAL_SHORTAGE"),
            CausalRule("R2", "SUPPLIER_DELAY", "PRODUCTION_DELAY"),
        )
    )
    with pytest.raises(CausalChainError, match="ambiguous"):
        propagate_chain(source(), ambiguous, {1: "E1"})


def test_chain_rejects_cycle():
    cyclic = CausalRuleSet(
        (
            CausalRule("R1", "SUPPLIER_DELAY", "MATERIAL_SHORTAGE"),
            CausalRule("R2", "MATERIAL_SHORTAGE", "SUPPLIER_DELAY"),
        )
    )
    with pytest.raises(CausalChainError, match="cycle"):
        propagate_chain(source(), cyclic, {1: "E1", 2: "E2"}, max_depth=5)


def test_chain_requires_deterministic_event_ids():
    with pytest.raises(CausalChainError, match="event id"):
        propagate_chain(source(), rules(), {}, max_depth=3)
