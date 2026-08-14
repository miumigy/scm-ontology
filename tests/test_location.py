import pytest

from scm_ontology.location import CanonicalLocation, LocationConceptError, is_location


def test_creates_canonical_location():
    location = CanonicalLocation(
        location_id="WH-001",
        location_type="warehouse",
        name="Kansai Distribution Center",
    )
    assert location.location_id == "WH-001"
    assert is_location(location)


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"location_id": "", "location_type": "warehouse", "name": "WH"}, "location_id"),
        ({"location_id": "L", "location_type": "", "name": "WH"}, "location_type"),
        ({"location_id": "L", "location_type": "warehouse", "name": ""}, "name"),
    ],
)
def test_rejects_invalid_location(kwargs, message):
    with pytest.raises(LocationConceptError, match=message):
        CanonicalLocation(**kwargs)
