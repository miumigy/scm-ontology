from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.canonical_event import CanonicalEvent
from scm_ontology.canonical_event_lineage import (
    CanonicalEventLineage,
    CanonicalEventLineageError,
    extract_event_lineage,
)
from datetime import datetime, timezone


def event():
    return CanonicalEvent(
        event_type="execution_outcome_recorded",
        occurred_at=datetime(2026, 8, 16, 22, 10, tzinfo=timezone.utc),
        entity_id="cmd-1",
        attributes={
            "evidence_ids": ["e1", "e2"],
            "provenance_ids": ["p1", "p2"],
        },
    )


def test_lineage_is_immutable_and_deterministic():
    result = extract_event_lineage(event())
    assert isinstance(result, CanonicalEventLineage)
    assert result.event_id == "cmd-1"
    assert result.evidence_ids == ("e1", "e2")
    assert result.provenance_ids == ("p1", "p2")
    assert result.to_mapping() == {
        "contract_version": "S349.1",
        "event_id": "cmd-1",
        "evidence_ids": ["e1", "e2"],
        "provenance_ids": ["p1", "p2"],
    }
    with pytest.raises(FrozenInstanceError):
        result.event_id = "cmd-2"


def test_lineage_freezes_source_sequences():
    source = event()
    result = extract_event_lineage(source)
    source.attributes["evidence_ids"].append("e3")
    assert result.evidence_ids == ("e1", "e2")


def test_lineage_rejects_malformed_identifiers():
    with pytest.raises(CanonicalEventLineageError):
        CanonicalEventLineage(event_id="", evidence_ids=(), provenance_ids=())
    with pytest.raises(CanonicalEventLineageError):
        CanonicalEventLineage(event_id="cmd-1", evidence_ids=("",), provenance_ids=())
    with pytest.raises(CanonicalEventLineageError):
        CanonicalEventLineage(event_id="cmd-1", evidence_ids=(), provenance_ids=(" ",))


def test_lineage_rejects_non_string_sequences():
    invalid = CanonicalEvent(
        event_type="execution_outcome_recorded",
        occurred_at=datetime(2026, 8, 16, 22, 10, tzinfo=timezone.utc),
        entity_id="cmd-1",
        attributes={"evidence_ids": [1], "provenance_ids": ["p1"]},
    )
    with pytest.raises(CanonicalEventLineageError):
        extract_event_lineage(invalid)
