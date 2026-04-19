"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_signup_successful(client, reset_activities):
    """Test successful signup adds participant to activity"""
    response = client.post(
        "/activities/Basketball Team/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "Signed up newstudent@mergington.edu for Basketball Team" in data["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "newstudent@mergington.edu" in activities["Basketball Team"]["participants"]


def test_signup_to_activity_with_existing_participants(client, reset_activities):
    """Test signup to activity that already has participants"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    assert response.status_code == 200
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert len(activities["Chess Club"]["participants"]) == 3
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_nonexistent_activity(client, reset_activities):
    """Test signup to non-existent activity returns 404"""
    response = client.post(
        "/activities/Non Existent Club/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_signup_duplicate_email(client, reset_activities):
    """Test signing up with duplicate email returns 400"""
    # First signup should succeed
    response1 = client.post(
        "/activities/Basketball Team/signup",
        params={"email": "student@mergington.edu"}
    )
    assert response1.status_code == 200
    
    # Second signup with same email should fail
    response2 = client.post(
        "/activities/Basketball Team/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response2.status_code == 400
    data = response2.json()
    assert data["detail"] == "Student already signed up"


def test_signup_same_email_different_activities(client, reset_activities):
    """Test that same student can sign up for multiple activities"""
    student_email = "student@mergington.edu"
    
    # Sign up for Basketball Team
    response1 = client.post(
        "/activities/Basketball Team/signup",
        params={"email": student_email}
    )
    assert response1.status_code == 200
    
    # Sign up for Soccer Club
    response2 = client.post(
        "/activities/Soccer Club/signup",
        params={"email": student_email}
    )
    assert response2.status_code == 200
    
    # Verify both signups were successful
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert student_email in activities["Basketball Team"]["participants"]
    assert student_email in activities["Soccer Club"]["participants"]


def test_signup_multiple_students_same_activity(client, reset_activities):
    """Test multiple students can sign up for the same activity"""
    # First student
    response1 = client.post(
        "/activities/Soccer Club/signup",
        params={"email": "student1@mergington.edu"}
    )
    assert response1.status_code == 200
    
    # Second student
    response2 = client.post(
        "/activities/Soccer Club/signup",
        params={"email": "student2@mergington.edu"}
    )
    assert response2.status_code == 200
    
    # Verify both were added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert len(activities["Soccer Club"]["participants"]) == 2
    assert "student1@mergington.edu" in activities["Soccer Club"]["participants"]
    assert "student2@mergington.edu" in activities["Soccer Club"]["participants"]
