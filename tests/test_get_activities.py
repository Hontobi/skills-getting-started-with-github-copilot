"""
Tests for the GET /activities endpoint.
"""

import pytest


def test_get_activities_returns_all_activities(client, reset_activities):
    """Test that GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 9
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_get_activities_includes_correct_structure(client, reset_activities):
    """Test that activities have the correct structure"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    activity = data["Chess Club"]
    
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_get_activities_includes_participants(client, reset_activities):
    """Test that activities include their current participants"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    chess_club = data["Chess Club"]
    
    assert len(chess_club["participants"]) == 2
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]


def test_get_activities_includes_empty_activities(client, reset_activities):
    """Test that activities with no participants are included"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    basketball = data["Basketball Team"]
    
    assert len(basketball["participants"]) == 0
