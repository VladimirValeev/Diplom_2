from src import endpoints as ep


def test_login_existing_user_success(api, created_user):
    payload = created_user["payload"]
    r = api.request("POST", ep.LOGIN, json={"email": payload["email"], "password": payload["password"]})
    assert r.status_code == 200
    data = r.json()
    assert data["success"] is True
    assert "accessToken" in data
    assert "refreshToken" in data
    assert data["user"]["email"] == payload["email"]


def test_login_wrong_credentials_401(api):
    r = api.request("POST", ep.LOGIN, json={"email": "nope@test.ru", "password": "wrong"})
    assert r.status_code == 401
    data = r.json()
    assert data["success"] is False
    assert data["message"] == "email or password are incorrect"
