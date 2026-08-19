from pathlib import Path

import yaml


FIXTURE = Path(__file__).parents[1] / "examples" / "external-framework-mapping" / "external-framework-mapping.yaml"


def test_framework_fixture_has_mapping_types_and_provenance_fields() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    assert data["version"] == "0.1"
    assert data["mappings"]
    for mapping in data["mappings"]:
        assert mapping["framework"]
        assert mapping["source_id"]
        assert mapping["mapping_type"] in {
            "exact", "broader", "narrower", "composite", "contextual", "adjacent", "unmapped"
        }
        assert "status" in mapping
        assert "confidence" in mapping
        assert "rationale" in mapping


def test_unmapped_is_allowed_without_inventing_a_target() -> None:
    data = yaml.safe_load(FIXTURE.read_text())
    unmapped = [m for m in data["mappings"] if m["mapping_type"] == "unmapped"]
    assert unmapped
    assert all(m["canonical_target"] is None for m in unmapped)
