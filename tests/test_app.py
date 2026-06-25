import copy
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    original_state = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_state)


def test_unregister_participant_removes_email_from_activity():
    client = TestClient(app)
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"

    response = client.delete(
        f"/activities/{quote(activity_name)}/participants/{quote(participant_email)}"
    )

    assert response.status_code == 200
    assert participant_email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Removed {participant_email} from {activity_name}"


def test_unregister_participant_returns_404_for_unknown_participant():
    client = TestClient(app)
    activity_name = "Chess Club"
    participant_email = "missing@mergington.edu"

    response = client.delete(
        f"/activities/{quote(activity_name)}/participants/{quote(participant_email)}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
