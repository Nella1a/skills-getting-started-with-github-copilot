from urllib.parse import quote

from src import app as app_module


def test_get_activities_returns_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["description"] == (
        "Learn strategies and compete in chess tournaments"
    )


def test_signup_new_student(client):
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"

    response = client.post(f"/activities/{quote(activity_name)}/signup?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_duplicate_student(client):
    email = "michael@mergington.edu"
    activity_name = "Chess Club"

    response = client.post(f"/activities/{quote(activity_name)}/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_unknown_activity(client):
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{quote('Unknown Activity')}/signup?email={email}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_student(client):
    email = "michael@mergington.edu"
    activity_name = "Chess Club"

    response = client.delete(f"/activities/{quote(activity_name)}/unregister?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_student_not_found(client):
    email = "ghost@mergington.edu"
    activity_name = "Chess Club"

    response = client.delete(f"/activities/{quote(activity_name)}/unregister?email={email}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_unknown_activity(client):
    email = "newstudent@mergington.edu"

    response = client.delete(f"/activities/Unknown Activity/unregister?email={email}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
