from scm_ontology.evidence import EvidenceReference
from scm_ontology.observation import Observation


def test_observation_can_be_referenced_as_evidence_without_new_link_type():
    observation = Observation(
        observation_id="O1",
        observed_at=__import__("datetime").datetime(2026, 8, 1, 10, 30),
        subject_id="Shipment-001",
    )
    evidence = EvidenceReference(
        evidence_id="E1",
        evidence_type="observation",
        reference=observation.observation_id,
    )

    assert evidence.evidence_type == "observation"
    assert evidence.reference == "O1"
    assert observation.subject_id == "Shipment-001"


def test_observation_and_evidence_keep_distinct_semantic_roles():
    observation = Observation(
        observation_id="O1",
        observed_at=__import__("datetime").datetime(2026, 8, 1, 10, 30),
        subject_id="Shipment-001",
    )
    evidence = EvidenceReference(
        evidence_id="E1",
        evidence_type="observation",
        reference="O1",
    )

    assert observation.observation_id != evidence.evidence_id
    assert observation.observed_at is not None
    assert evidence.reference == observation.observation_id
