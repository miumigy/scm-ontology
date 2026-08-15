from pathlib import Path

DOC = Path("docs/milestones/S285-m8-canonical-application-record.md")


def test_s285_requires_application_record_identity_and_scope() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "a unique application record identifier",
        "the Decision Record that explicitly authorized the application",
        "the application actor or governing authority",
        "the target Canonical entities, attributes, and/or predicates affected",
        "the requested operation and bounded scope",
        "the pre-application Canonical state reference",
        "the resulting Canonical state reference",
    ):
        assert phrase in text


def test_s285_requires_explicit_outcomes() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Applied",
        "Rejected",
        "Failed",
        "Superseded",
        "A rejected or failed application MUST NOT be represented as an Applied result",
    ):
        assert phrase in text


def test_s285_preserves_auditability() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Every Applied result MUST reference an Approved Decision Record",
        "Application history MUST be append-only",
        "An Application Record MUST NOT silently rewrite a previous Application Record",
        "Source identity, provenance, and evidence MUST remain traceable after application",
        "Replay MUST be possible",
    ):
        assert phrase in text


def test_s285_protects_mutation_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Creating, storing, or replaying an Application Record MUST NOT automatically mutate the Canonical Graph",
        "create a new canonical entity, attribute, or predicate implicitly",
        "infer Canonical Truth from the Application Record alone",
        "discard conflicting source assertions or provenance",
        "import vendor-specific semantics into the Canonical Ontology",
        "Reasoning MUST remain read-only",
    ):
        assert phrase in text
