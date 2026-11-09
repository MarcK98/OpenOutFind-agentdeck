"""AgentDeck fork: with the hub off, nothing may touch the network."""
from unittest.mock import patch

import pytest

from openoutfind.contacts import service

pytestmark = pytest.mark.hub_off


def test_hub_flag_is_off_by_default():
    assert service.HUB_ENABLED is False


def test_no_entry_point_makes_a_request():
    with patch.object(service.requests, "post") as post, patch.object(service.requests, "get") as get:
        class Lead:
            profile_url = "https://www.linkedin.com/in/x"
            country_code = "US"
        assert service.resolve(Lead()) is None
        assert service.contribute(Lead(), ["a@b.com"], "betterContact") is None
        assert service.share_profiles([{"contact_linkedin_profile_url": "u"}], "US", {}) is None
        assert service.share_companies([], "US", {}) is None
        assert service.register_operator() is False
        assert service.hub_balance() == {"balance": None, "known": False}
        assert service._mint({"operator_email": "a@b.com"}) == ""
        assert service._send("profiles", {}) is None
    post.assert_not_called()
    get.assert_not_called()
