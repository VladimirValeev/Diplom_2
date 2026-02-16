import allure

from src.api_client import ApiClient
from src import endpoints as ep
from tests import data


@allure.feature("Orders")
class TestOrders:

    @allure.story("Create order")
    def test_create_order_with_auth_success(self, auth_header, ingredient_ids):
        api = ApiClient()

        with allure.step("POST /api/orders — create order with auth"):
            r = api.request(
                "POST",
                ep.ORDERS,
                headers=auth_header,
                json={"ingredients": ingredient_ids},
            )

        assert r.status_code == 200, r.text
        body = r.json()
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]

    @allure.story("Create order")
    def test_create_order_without_auth_success(self, ingredient_ids):
        """
        На текущем стенде заказ создаётся без авторизации (200).
        Тест фиксирует фактическое поведение стенда.
        """
        api = ApiClient()

        with allure.step("POST /api/orders — create order WITHOUT auth"):
            r = api.request(
                "POST",
                ep.ORDERS,
                json={"ingredients": ingredient_ids},
            )

        assert r.status_code == 200, r.text
        body = r.json()
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]

    @allure.story("Create order")
    def test_create_order_without_ingredients_returns_400(self, auth_header):
        api = ApiClient()

        with allure.step("POST /api/orders — create order with EMPTY ingredients"):
            r = api.request(
                "POST",
                ep.ORDERS,
                headers=auth_header,
                json={"ingredients": []},
            )

        assert r.status_code == 400, r.text
        body = r.json()
        assert body["success"] is False
        assert body["message"] == data.MSG_EMPTY_INGREDIENTS

    @allure.story("Create order")
    def test_create_order_with_invalid_ingredient_hash_returns_400(self, auth_header):
        """
        На текущем стенде невалидный id ингредиента даёт 400.
        Тест фиксирует фактическое поведение стенда.
        """
        api = ApiClient()

        with allure.step("POST /api/orders — create order with INVALID ingredient id"):
            r = api.request(
                "POST",
                ep.ORDERS,
                headers=auth_header,
                json={"ingredients": [data.INVALID_INGREDIENT_HASH]},
            )

        assert r.status_code == 400, r.text
        body = r.json()
        assert body["success"] is False
        assert body["message"] == data.MSG_BAD_INGREDIENT
