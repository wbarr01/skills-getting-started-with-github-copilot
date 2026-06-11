from src.app import activities


def test_root_redirects_to_static_index(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.url.path == "/static/index.html"


def test_get_activities_returns_current_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"

    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


def test_signup_adds_participant_to_activity(client):
    email = "new.student@mergington.edu"

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert email in activities["Chess Club"]["participants"]


def test_signup_rejects_duplicate_participant(client):
    email = "michael@mergington.edu"

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post("/activities/Unknown Activity/signup?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_participant_from_activity(client):
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_returns_404_for_missing_participant(client):
    response = client.delete("/activities/Chess Club/signup?email=not-enrolled@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete("/activities/Unknown Activity/signup?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
