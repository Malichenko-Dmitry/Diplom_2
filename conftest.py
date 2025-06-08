import pytest
from helper import Helper
from helper import StellarBurgersApi

@pytest.fixture()
def manage_user_credentials():
    payload = Helper.generate_credentials_user()
    yield payload
    response = StellarBurgersApi.login_user(payload)
    if response.status_code == 200:
        access_token = response.json()["accessToken"]
        headers = StellarBurgersApi.auth_headers(access_token)
        test = StellarBurgersApi.delete_user(headers=headers)

@pytest.fixture()
def register_new_user_and_return_credentials():
    payload = Helper.generate_credentials_user()
    response = StellarBurgersApi.create_user(payload)
    if response.status_code == 200:
        access_token = response.json()["accessToken"]
        yield {
            "payload": payload,
            "access_token": access_token
        }
        headers = StellarBurgersApi.auth_headers(access_token)
        StellarBurgersApi.delete_user(headers=headers)
    else:
        pytest.fail(f"Не удалось зарегистрировать пользователя: {response.status_code}, {response.text}")

@pytest.fixture()
def get_ingredients():
    response = StellarBurgersApi.get_ingredients()
    ingredients = response.json()["data"]
    return ingredients

@pytest.fixture()
def make_order_body_ingredients(get_ingredients):
    return {
            "ingredients": [get_ingredients[0]['_id']],
        }
