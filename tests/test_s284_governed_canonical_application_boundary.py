from pathlib import Path

DOC = Path("docs/history/phase8/S284-m8-governed-canonical-application-boundary.md")


def test_s284_requires_explicit_application_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Approved Decision Record",
        "Application Request",
        "Governance / Preconditions Check",
        "Explicit Canonical Application",
        "Application Record",
    ):
        assert phrase in text


def test_s284_requires_governed_preconditions() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "the referenced Decision Record is Approved",
        "the decision has not been superseded or revoked",
        "all affected Canonical identities and facts are explicitly identified",
        "required provenance and evidence references are present",
        "the application scope is explicit",
        "the application actor or governing authority is recorded",
    ):
        assert phrase in text


def test_s284_protects_canonical_semantics() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Canonical mutation MUST occur only through an explicit governed application step",
        "Application MUST NOT silently create a new canonical entity, attribute, or predicate",
        "Application MUST NOT silently overwrite unrelated Canonical Facts",
        "Reasoning MUST remain read-only",
        "Mapping success, identity similarity, provenance, evidence, or model confidence alone MUST NOT authorize Canonical mutation",
        "Vendor-specific semantics MUST NOT be introduced into the Canonical Ontology through application",
    ):
        assert phrase in text


def test_s284_preserves_auditability() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "source assertions, evidence, provenance, and Decision Record MUST remain traceable after application",
        "Failed or rejected application attempts MUST remain auditable",
        "Application history MUST be append-only and replayable",
    ):
        assert phrase in text
