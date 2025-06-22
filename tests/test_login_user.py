import allure
import pytest
import data
from helper import StellarBurgersApi

@allure.feature("Логин пользователя")
class TestLoginUser:

    @allure.title("Авторизация существующего пользователя с корректными данными")
    def test_login_exist_user_success_response(self, register_new_user_and_return_credentials):
        user = register_new_user_and_return_credentials
        user_payload = user['payload']
        response = StellarBurgersApi.login_user(user_payload)
        response_json = response.json()
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        assert response_json.get('success') is True, f"Response success: {response_json.get('success')}"
        assert response_json.get('user', {}).get('email') == user_payload['email'], "Email in response does not match"
        assert response_json.get('user', {}).get('name') == user_payload['name'], "Name in response does not match"
        assert 'accessToken' in response_json, "Missing accessToken in response"
        assert 'refreshToken' in response_json, "Missing refreshToken in response"


    @allure.title("Невозможность авторизации с неправильным логином или паролем")
    @pytest.mark.parametrize('field,data_field', [
        ('email', 'this_is_fake@mail.com'),
        ('password', 'fake_password')
    ])
    def test_login_with_incorrect_login_or_password(self, register_new_user_and_return_credentials, field, data_field):
        user = register_new_user_and_return_credentials
        user_payload = dict(user['payload'])
        user_payload[field] = data_field
        response = StellarBurgersApi.login_user(user_payload)
        response_json = response.json()
        assert response.status_code == 401, f"Unexpected status code: {response.status_code}"
        assert response_json.get('success') is False, f"Response success: {response_json.get('success')}"
        assert response_json.get('message') == data.ERROR_MESSAGE_INVALID_CREDENTIALS, \
            f"Unexpected message: {response_json.get('message')}"