import pytest

from scm_ontology.observation_entity_link import ObservationEntityLinkError, link_observation_entity


def test_links_observation_to_entity():
    link = link_observation_entity("obs-1", "SITE-A")
    assert link.observation_id == "obs-1"
    assert link.entity_id == "SITE-A"
    assert link.relationship == "observed_for"


def test_link_is_deterministic():
    args = ("obs-1", "SITE-A", "observed_for")
    assert link_observation_entity(*args) == link_observation_entity(*args)


@pytest.mark.parametrize(
    "observation_id,entity_id,relationship,message",
    [
        ("", "SITE-A", "observed_for", "observation_id"),
        ("obs-1", "", "observed_for", "entity_id"),
        ("obs-1", "SITE-A", "measures", "relationship must be observed_for"),
    ],
)
def test_link_fields_are_validated(observation_id, entity_id, relationship, message):
    with pytest.raises(ObservationEntityLinkError, match=message):
        link_observation_entity(observation_id, entity_id, relationship)
