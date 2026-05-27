from urllib.parse import quote

from src import app as app_module


def test_get_activities_returns_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant(client):
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"

    response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email in response.json()["message"]
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    email = "michael@mergington.edu"
    activity_name = "Chess Club"

    response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_unknown_activity_returns_404(client):
    response = client.post(
        "/activities/Unknown%20Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant(client):
    email = "michael@mergington.edu"
    activity_name = "Chess Club"

    response = client.delete(
        f"/activities/{quote(activity_name)}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]
    assert "Unregistered" in response.json()["message"]


def test_remove_unknown_participant_returns_404(client):
    email = "unknown@mergington.edu"
    activity_name = "Chess Club"

    response = client.delete(
        f"/activities/{quote(activity_name)}/participants",
        params={"email": email},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
