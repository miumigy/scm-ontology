from scm_ontology.multi_source_reference import run_multi_source_reference_path


def test_primary_launch_demo_is_deterministic_and_reference_only():
    first = run_multi_source_reference_path()
    second = run_multi_source_reference_path()

    assert first.to_json() == second.to_json()
    assert first.content_hash == second.content_hash
    assert first.canonical_truth_boundary == "reference"
    assert first.node_count == 4
    assert first.edge_count == 2
    assert len(first.identity_links) == 2
