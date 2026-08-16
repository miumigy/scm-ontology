import pytest
from scm_ontology.snapshot_causal_query import SnapshotCausalChainNotFound, trace_snapshot_causal_chain
from scm_ontology.snapshot_lineage import SnapshotTransition

def _transition(frm, to, event, outcome):
    return SnapshotTransition(frm, f"fp-{frm}", event, outcome, to, f"fp-{to}", "2026-08-16T02:00:00Z")

def test_trace_snapshot_causal_chain_returns_newest_to_oldest():
    transitions = (_transition("s0", "s1", "e1", "o1"), _transition("s1", "s2", "e2", "o2"), _transition("s2", "s3", "e3", "o3"))
    chain = trace_snapshot_causal_chain(transitions, snapshot_id="s3")
    assert [t.to_snapshot_id for t in chain] == ["s3", "s2", "s1"]
    assert [t.execution_event_id for t in chain] == ["e3", "e2", "e1"]

def test_trace_snapshot_causal_chain_rejects_cycles():
    transitions = (_transition("s1", "s2", "e1", "o1"), _transition("s2", "s1", "e2", "o2"))
    with pytest.raises(ValueError, match="cycle"):
        trace_snapshot_causal_chain(transitions, snapshot_id="s1")

def test_trace_snapshot_causal_chain_reports_unknown_snapshot():
    with pytest.raises(SnapshotCausalChainNotFound):
        trace_snapshot_causal_chain((), snapshot_id="missing")
