import allure
import pytest
import data
from helper import StellarBurgersApi


@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Успешное создание уникального пользователя с корректными данными")
    def test_create_user_returns_200_success_response(self, manage_user_credentials):
        response = StellarBurgersApi.create_user(manage_user_credentials)
        response_json = response.json()
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        assert response_json.get('success') is True, f"Response success: {response_json.get('success')}"
        user = response_json.get('user', {})
        assert user.get('email') == manage_user_credentials['email']
        assert user.get('name') == manage_user_credentials['name']
        assert 'accessToken' in response_json
        assert 'refreshToken' in response_json

    @allure.title("Невозможность создания пользователя с уже существующими данными")
    def test_create_user_fails_for_duplicate_create(self, manage_user_credentials):
        StellarBurgersApi.create_user(manage_user_credentials)
        response = StellarBurgersApi.create_user(manage_user_credentials)
        response_json = response.json()
        assert response.status_code == 403, f"Unexpected status code: {response.status_code}"
        assert response_json.get('success') is False
        assert response_json.get('message') == data.ERROR_MESSAGE_USER_ALREADY_EXISTS

    @allure.title("Невозможность создания пользователя при отсутствии одного из обязательных полей")
    @pytest.mark.parametrize('data_test', [
        data.USER_CREDENTIALS_WITHOUT_EMAIL,
        data.USER_CREDENTIALS_WITHOUT_PASSWORD,
        data.USER_CREDENTIALS_WITHOUT_NAME
    ])
    def test_create_user_without_required_fields(self, data_test):
        response = StellarBurgersApi.create_user(data_test)
        response_json = response.json()
        assert response.status_code == 403, f"Unexpected status code: {response.status_code}"
        assert response_json.get('success') is False
        assert response_json.get('message') == data.ERROR_MESSAGE_REQUIRED_FIELDS