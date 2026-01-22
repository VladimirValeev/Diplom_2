import allure
import requests

from .endpoints import BASE_URL


class ApiClient:
    def __init__(self):
        self.session = requests.Session()

    @allure.step("HTTP {method} {path}")
    def request(self, method: str, path: str, *, headers=None, json=None):
        url = BASE_URL + path
        resp = self.session.request(method, url, headers=headers, json=json)

        # полезные вложения в Allure
        allure.attach(str(resp.status_code), name="status_code", attachment_type=allure.attachment_type.TEXT)
        allure.attach(resp.text, name="response_text", attachment_type=allure.attachment_type.TEXT)

        return resp
