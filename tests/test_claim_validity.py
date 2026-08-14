from scm_ontology.claim_validity import ClaimValidity


def test_open_claim_interval():
    validity = ClaimValidity()
    assert validity.valid_from is None
    assert validity.valid_to is None


def test_bounded_claim_interval():
    validity = ClaimValidity("2026-07-01", "2026-12-31")
    assert validity.valid_from == "2026-07-01"
    assert validity.valid_to == "2026-12-31"


def test_open_ended_claim_interval():
    validity = ClaimValidity("2026-07-01", None)
    assert validity.valid_from == "2026-07-01"
    assert validity.valid_to is None


def test_empty_bound_is_rejected():
    try:
        ClaimValidity("")
    except ValueError as exc:
        assert "valid_from" in str(exc)
    else:
        raise AssertionError("expected ValueError")
