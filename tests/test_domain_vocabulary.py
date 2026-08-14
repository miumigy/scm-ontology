import pytest

from scm_ontology.domain_vocabulary import DomainVocabularyEntry, DomainVocabularyError


def test_accepts_canonical_domain_term():
    entry = DomainVocabularyEntry(
        name="Inventory",
        definition="A quantity of goods held at a supply chain entity.",
        core_primitive="Entity",
        synonyms=("stock",),
    )
    assert entry.name == "Inventory"
    assert entry.core_primitive == "Entity"


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"name": "", "definition": "x", "core_primitive": "Entity"}, "name"),
        ({"name": "Inventory", "definition": "", "core_primitive": "Entity"}, "definition"),
        ({"name": "Inventory", "definition": "x", "core_primitive": ""}, "core_primitive"),
        ({"name": "Inventory", "definition": "x", "core_primitive": "Entity", "synonyms": ("",)}, "synonyms"),
    ],
)
def test_rejects_invalid_domain_term(kwargs, message):
    with pytest.raises(DomainVocabularyError, match=message):
        DomainVocabularyEntry(**kwargs)
