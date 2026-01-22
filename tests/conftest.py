import uuid
import pytest

from src.api_client import ApiClient
from src import endpoints as ep


@pytest.fixture
def api():
    return ApiClient()


@pytest.fixture
def user_payload():
    uniq = uuid.uuid4().hex[:10]
    return {
        "email": f"vova_{uniq}@test.ru",
        "password": "Passw0rd!",
        "name": f"Vova_{uniq}"
    }


@pytest.fixture
def created_user(api, user_payload):
    r = api.request("POST", ep.REGISTER, json=user_payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data.get("success") is True
    assert "accessToken" in data and "refreshToken" in data
    return {
        "payload": user_payload,
        "accessToken": data["accessToken"],
        "refreshToken": data["refreshToken"],
    }


@pytest.fixture
def auth_header(created_user):
    return {"Authorization": created_user["accessToken"]}


@pytest.fixture
def ingredient_ids(api):
    r = api.request("GET", ep.INGREDIENTS)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data.get("success") is True
    items = data.get("data")
    assert items and isinstance(items, list)
    return [items[0]["_id"], items[1]["_id"]]
