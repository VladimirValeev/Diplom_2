import pytest
from src import endpoints as ep


def test_create_unique_user_success(api, user_payload):
    r = api.request("POST", ep.REGISTER, json=user_payload)
    assert r.status_code == 200
    data = r.json()
    assert data["success"] is True
    assert "accessToken" in data
    assert "refreshToken" in data
    assert data["user"]["email"] == user_payload["email"]
    assert data["user"]["name"] == user_payload["name"]


def test_create_existing_user_403(api, user_payload):
    r1 = api.request("POST", ep.REGISTER, json=user_payload)
    assert r1.status_code == 200

    r2 = api.request("POST", ep.REGISTER, json=user_payload)
    assert r2.status_code == 403
    data = r2.json()
    assert data["success"] is False
    assert data["message"] == "User already exists"


@pytest.mark.parametrize("field", ["email", "password", "name"])
def test_create_user_missing_required_field_403(api, user_payload, field):
    payload = dict(user_payload)
    payload.pop(field)

    r = api.request("POST", ep.REGISTER, json=payload)
    assert r.status_code == 403
    data = r.json()
    assert data["success"] is False
    assert data["message"] == "Email, password and name are required fields"
