import json
from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.multi_source_reference import (
    MultiSourceError,
    converge,
    reference_datasets,
    reference_mapping_rules,
    reference_quality_policies,
    run_multi_source_reference_path,
)
from scm_ontology.identity_resolution_runtime import IdentityResolutionPolicy
from scm_ontology.reference_data_adapter import (
    CsvAdapterConfig,
    SourceManifest,
    adapt_csv,
)


def test_reference_path_converges_reproducibly():
    first = run_multi_source_reference_path()
    second = run_multi_source_reference_path()
    assert first.node_count == 4
    assert first.edge_count == 2
    assert len(first.identity_links) == 2
    assert first.canonical_truth_boundary == "reference"
    assert first.content_hash == second.content_hash
    assert first.to_json() == second.to_json()


def test_product_nodes_converge_from_two_sources():
    graph = run_multi_source_reference_path()
    product = graph.node("Product:0850000000101")
    assert {source[0] for source in product.sources} == {"erp", "wms"}


def test_edges_resolve_to_converged_nodes():
    graph = run_multi_source_reference_path()
    carried = [e for e in graph.edges if e.predicate == "carriedBy"]
    assert len(carried) == 2
    for edge in carried:
        assert edge.subject_key.startswith("Shipment:")
        assert edge.object_key.startswith("Product:085000000010")


def test_identity_links_trace_resolved_matches():
    graph = run_multi_source_reference_path()
    all_members = {member for link in graph.identity_links for member in link}
    assert any("MAT-1000" in member for member in all_members)
    assert any("PROD-1000" in member for member in all_members)


def test_graph_is_immutable_reference_boundary():
    graph = run_multi_source_reference_path()
    with pytest.raises(FrozenInstanceError):
        graph.nodes = ()
    payload = json.loads(graph.to_json())
    assert payload["canonical_truth_boundary"] == "reference"
    assert payload["content_hash"] == graph.content_hash


def test_converge_fails_closed_when_quality_gate_blocks():
    manifest = SourceManifest(
        source_system="erp", adapter_version="P7A.1", data_contract_version="P7A.1",
        mapping_config_version="M8-reference", extracted_at="2026-08-19T09:00:00Z",
        scope="enterprise:other", adapter_kind="csv",
    )
    bad = adapt_csv(
        [{"material_id": "MAT-X", "gtin": "G", "description": "x"}],
        manifest,
        CsvAdapterConfig(source_system="erp", record_id_column="material_id"),
    )
    with pytest.raises(MultiSourceError, match="quality gate blocked"):
        converge(
            (bad,),
            quality_policies=reference_quality_policies(),
            mapping_rules=reference_mapping_rules(),
            identity_policy=IdentityResolutionPolicy(policy_id="p", policy_version="v"),
            decision_at="2026-08-19T09:30:00Z",
            now="2026-08-19T09:30:00Z",
        )


def test_reference_datasets_are_three_heterogeneous_sources():
    datasets = reference_datasets()
    assert [dataset.manifest.adapter_kind for dataset in datasets] == ["csv", "json", "sql"]
    assert [dataset.manifest.source_system for dataset in datasets] == ["erp", "wms", "tms"]
