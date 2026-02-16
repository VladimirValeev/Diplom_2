import uuid
import pytest
import allure

from src.api_client import ApiClient
from src import endpoints as ep
from tests import data


@pytest.fixture
def user_payload():
    uniq = uuid.uuid4().hex[:10]
    return {
        "email": f"{data.EMAIL_PREFIX}{uniq}@test.ru",
        "password": data.PASSWORD,
        "name": f"{data.NAME_PREFIX}{uniq}",
    }


@pytest.fixture
def created_user(user_payload):
    api = ApiClient()

    with allure.step("POST /api/auth/register — create user"):
        r = api.request("POST", ep.REGISTER, json=user_payload)

    if r.status_code != 200:
        pytest.fail(f"Failed to create user. Status={r.status_code}, body={r.text}")

    body = r.json()
    if body.get("success") is not True:
        pytest.fail(f"User creation returned success!=True: {body}")

    if "accessToken" not in body or "refreshToken" not in body:
        pytest.fail(f"Tokens not found in response: {body}")

    return {
        "payload": user_payload,
        "accessToken": body["accessToken"],
        "refreshToken": body["refreshToken"],
    }


@pytest.fixture
def auth_header(created_user):
    return {"Authorization": created_user["accessToken"]}


@pytest.fixture
def ingredient_ids():
    api = ApiClient()

    with allure.step("GET /api/ingredients — fetch ingredient ids"):
        r = api.request("GET", ep.INGREDIENTS)

    if r.status_code != 200:
        pytest.fail(f"Failed to fetch ingredients. Status={r.status_code}, body={r.text}")

    body = r.json()
    if body.get("success") is not True:
        pytest.fail(f"Ingredients response success!=True: {body}")

    items = body.get("data")
    if not items or not isinstance(items, list) or len(items) < 2:
        pytest.fail(f"Not enough ingredients in response: {body}")

    return [items[0]["_id"], items[1]["_id"]]
