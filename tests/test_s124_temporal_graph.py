from pathlib import Path


FIXTURE = Path(__file__).parents[1] / "examples" / "s124" / "temporal-graph.yaml"


def test_temporal_fixture_preserves_distinct_time_dimensions() -> None:
    text = FIXTURE.read_text()
    assert "valid_from:" in text
    assert "transaction_time:" in text
    assert "observation_time:" in text
    assert "actual_time:" in text


def test_temporal_fixture_does_not_use_single_timestamp_semantics() -> None:
    text = FIXTURE.read_text()
    assert "timestamp:" not in text


def test_actual_scenario_is_explicit() -> None:
    text = FIXTURE.read_text()
    assert "scenario: actual" in text
