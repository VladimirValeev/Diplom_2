import allure

from src.api_client import ApiClient
from src import endpoints as ep
from tests import data


@allure.feature("User")
class TestUserLogin:

    @allure.story("Login")
    def test_login_existing_user_success(self, created_user):
        api = ApiClient()
        payload = created_user["payload"]

        with allure.step("POST /api/auth/login — login existing user"):
            r = api.request(
                "POST",
                ep.LOGIN,
                json={"email": payload["email"], "password": payload["password"]},
            )

        assert r.status_code == 200, r.text
        body = r.json()
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body["user"]["email"] == payload["email"]

    @allure.story("Login")
    def test_login_wrong_credentials_returns_401(self):
        api = ApiClient()

        with allure.step("POST /api/auth/login — wrong credentials"):
            r = api.request(
                "POST",
                ep.LOGIN,
                json={"email": "nope@test.ru", "password": "wrong"},
            )

        assert r.status_code == 401, r.text
        body = r.json()
        assert body["success"] is False
        assert body["message"] == data.MSG_LOGIN_WRONG
