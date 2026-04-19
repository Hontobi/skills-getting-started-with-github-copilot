"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint.
"""

import pytest


def test_unregister_successful(client, reset_activities):
    """Test successful unregistration removes participant from activity"""
    # First, add a participant
    client.post(
        "/activities/Basketball Team/signup",
        params={"email": "student@mergington.edu"}
    )
    
    # Then unregister
    response = client.delete(
        "/activities/Basketball Team/unregister",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered student@mergington.edu from Basketball Team" in data["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "student@mergington.edu" not in activities["Basketball Team"]["participants"]


def test_unregister_existing_participant(client, reset_activities):
    """Test unregistering an existing participant"""
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    
    assert response.status_code == 200
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    assert len(activities["Chess Club"]["participants"]) == 1


def test_unregister_nonexistent_activity(client, reset_activities):
    """Test unregister from non-existent activity returns 404"""
    response = client.delete(
        "/activities/Non Existent Club/unregister",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_unregister_not_signed_up_student(client, reset_activities):
    """Test unregistering a student not signed up returns 400"""
    response = client.delete(
        "/activities/Basketball Team/unregister",
        params={"email": "notstudent@mergington.edu"}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student not signed up for this activity"


def test_unregister_student_already_removed(client, reset_activities):
    """Test unregistering a student twice returns 400 on second attempt"""
    # First unregister
    response1 = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    assert response1.status_code == 200
    
    # Second unregister should fail
    response2 = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    assert response2.status_code == 400
    data = response2.json()
    assert data["detail"] == "Student not signed up for this activity"


def test_signup_and_unregister_workflow(client, reset_activities):
    """Test the complete signup and unregister workflow"""
    student_email = "workflow@mergington.edu"
    
    # Sign up
    signup_response = client.post(
        "/activities/Art Club/signup",
        params={"email": student_email}
    )
    assert signup_response.status_code == 200
    
    # Verify signup
    activities_response = client.get("/activities")
    assert student_email in activities_response.json()["Art Club"]["participants"]
    
    # Unregister
    unregister_response = client.delete(
        "/activities/Art Club/unregister",
        params={"email": student_email}
    )
    assert unregister_response.status_code == 200
    
    # Verify unregister
    activities_response = client.get("/activities")
    assert student_email not in activities_response.json()["Art Club"]["participants"]
