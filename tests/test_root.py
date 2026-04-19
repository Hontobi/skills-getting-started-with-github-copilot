"""
Tests for the root endpoint (GET /).
"""

import pytest


def test_root_redirect(client, reset_activities):
    """Test that the root endpoint redirects to /static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
