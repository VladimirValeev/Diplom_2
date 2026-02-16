import allure
import pytest

from src.api_client import ApiClient
from src import endpoints as ep
from tests import data


@allure.feature("User")
class TestUserCreate:

    @allure.story("Register")
    def test_create_unique_user_success(self, user_payload):
        api = ApiClient()

        with allure.step("POST /api/auth/register — create unique user"):
            r = api.request("POST", ep.REGISTER, json=user_payload)

        assert r.status_code == 200, r.text
        body = r.json()
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body["user"]["email"] == user_payload["email"]
        assert body["user"]["name"] == user_payload["name"]

    @allure.story("Register")
    def test_create_existing_user_returns_403(self, user_payload):
        api = ApiClient()

        with allure.step("POST /api/auth/register — create user first time"):
            r1 = api.request("POST", ep.REGISTER, json=user_payload)
        assert r1.status_code == 200, r1.text

        with allure.step("POST /api/auth/register — create same user second time"):
            r2 = api.request("POST", ep.REGISTER, json=user_payload)

        assert r2.status_code == 403, r2.text
        body = r2.json()
        assert body["success"] is False
        assert body["message"] == data.MSG_USER_EXISTS

    @allure.story("Register")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_create_user_missing_required_field_returns_403(self, user_payload, field):
        api = ApiClient()
        payload = dict(user_payload)
        payload.pop(field)

        with allure.step(f"POST /api/auth/register — missing required field: {field}"):
            r = api.request("POST", ep.REGISTER, json=payload)

        assert r.status_code == 403, r.text
        body = r.json()
        assert body["success"] is False
        assert body["message"] == data.MSG_REQUIRED_FIELDS
