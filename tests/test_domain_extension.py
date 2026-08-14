import pytest

from scm_ontology.domain_extension import DomainExtension, DomainExtensionError, validate_domain_extension


def test_accepts_explicit_core_mapping():
    extension = DomainExtension(
        name="Inventory",
        core_primitive="Entity",
        definition="A domain concept representing inventory relevant to an SCM context.",
    )
    assert validate_domain_extension(extension) == extension


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"name": "", "core_primitive": "Entity", "definition": "x"}, "name"),
        ({"name": "Inventory", "core_primitive": "", "definition": "x"}, "core_primitive"),
        ({"name": "Inventory", "core_primitive": "Entity", "definition": ""}, "definition"),
    ],
)
def test_requires_explicit_domain_contract(kwargs, message):
    with pytest.raises(DomainExtensionError, match=message):
        DomainExtension(**kwargs)
