from datetime import datetime, timezone

from scm_ontology.extension_application_audit import ExtensionApplicationAudit


def test_extension_application_audit_is_immutable_and_complete() -> None:
    audit = ExtensionApplicationAudit(
        proposal_ref="proposal:1",
        registry_version_before="v1",
        registry_version_after="v2",
        applied_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        actor_ref="actor:1",
    )
    assert audit.proposal_ref == "proposal:1"
    assert audit.registry_version_before == "v1"
    assert audit.registry_version_after == "v2"
    assert audit.actor_ref == "actor:1"
