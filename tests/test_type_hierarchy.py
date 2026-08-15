from scm_ontology.type_hierarchy import direct_parents, is_known_type


def test_canonical_type_hierarchy_is_explicit() -> None:
    assert direct_parents("Facility") == ("Node",)
    assert direct_parents("KPI") == ("Metric",)


def test_unknown_type_is_not_silently_known() -> None:
    assert not is_known_type("CustomerSpecificObject")
