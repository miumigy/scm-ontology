import pytest

from scm_ontology.causal import (
    CausalPropagationError,
    CausalRule,
    EventProvenance,
    derive_event,
    propagate_event,
)
from scm_ontology.simulation import Event


def supplier_delay(event_id="EVT-001"):
    return Event(event_id, "SUPPLIER_DELAY", 10, "SUP-001", {"magnitudeDays": 7})


def rule():
    return CausalRule("RULE-001", "SUPPLIER_DELAY", "MATERIAL_SHORTAGE_RISK")


def test_derive_event_preserves_lineage_deterministically():
    a = derive_event(supplier_delay(), rule(), event_id="EVT-002")
    b = derive_event(supplier_delay(), rule(), event_id="EVT-002")
    assert a == b
    assert a.event_type == "MATERIAL_SHORTAGE_RISK"
    assert a.provenance == EventProvenance("EVT-001", "RULE-001", 1)


def test_propagate_event_returns_none_without_matching_rule():
    assert propagate_event(supplier_delay(), {"OTHER": CausalRule("OTHER", "SHIPMENT_DELAY", "OTD_RISK")}, event_id="EVT-002") is None


def test_duplicate_rule_in_same_lineage_is_rejected():
    source = Event("EVT-001", "SUPPLIER_DELAY", 10, "SUP-001")
    loop_rule = CausalRule("RULE-LOOP", "SUPPLIER_DELAY", "SUPPLIER_DELAY")
    derived = derive_event(source, loop_rule, event_id="EVT-002")
    with pytest.raises(CausalPropagationError, match="already applied"):
        derive_event(derived, loop_rule, event_id="EVT-003")


def test_ambiguous_matching_rules_are_rejected():
    rules = {
        "R1": CausalRule("R1", "SUPPLIER_DELAY", "MATERIAL_SHORTAGE_RISK"),
        "R2": CausalRule("R2", "SUPPLIER_DELAY", "SUPPLY_RISK"),
    }
    with pytest.raises(CausalPropagationError, match="ambiguous"):
        propagate_event(supplier_delay(), rules, event_id="EVT-002")


def test_wrong_source_event_type_is_rejected():
    with pytest.raises(CausalPropagationError, match="cannot consume"):
        derive_event(Event("EVT-X", "DEMAND_SPIKE", 10, "P-001"), rule(), event_id="EVT-002")
