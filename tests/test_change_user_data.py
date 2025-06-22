import allure
import pytest
import data
from helper import StellarBurgersApi


@allure.feature("Изменение данных пользователя")
class TestChangeUserData:

    @allure.title("Обновление email или имени авторизованным пользователем")
    @pytest.mark.parametrize(
        'field, data_field',
        [
            ('email', 'update_email_user@example123.com'),
            ('name', 'update_name_user')
        ]
    )
    def test_update_email_or_name_with_authorization(self, register_new_user_and_return_credentials, field, data_field):
        user = register_new_user_and_return_credentials
        token = user['access_token']
        payload = user['payload'].copy()
        payload[field] = data_field
        headers = StellarBurgersApi.auth_headers(token)
        response = StellarBurgersApi.update_user(payload, headers)
        response_json = response.json()
        assert response.status_code == 200
        assert response_json['success'] is True
        assert response_json['user'][field] == data_field


    @allure.title("Обновление пароля авторизованным пользователем и авторизация с новым паролем")
    def test_update_password_with_authorization(self, register_new_user_and_return_credentials):
        user = register_new_user_and_return_credentials
        token = user['access_token']
        payload = user['payload'].copy()
        new_password = "update_password_user"
        payload['password'] = new_password
        headers = StellarBurgersApi.auth_headers(token)
        update_response = StellarBurgersApi.update_user(payload, headers)
        assert update_response.status_code == 200
        assert update_response.json()['success'] is True
        login_response = StellarBurgersApi.login_user(payload)
        assert login_response.status_code == 200
        assert login_response.json()['success'] is True


    @allure.title("Невозможность изменения данных пользователя без авторизации")
    @pytest.mark.parametrize(
        'field, data_field',
        [
            ('email', 'update_email_user@example123.com'),
            ('password', 'update_password_user'),
            ('name', 'update_name_user')
        ]
    )
    def test_update_data_user_without_authorization(self, register_new_user_and_return_credentials, field, data_field):
        user = register_new_user_and_return_credentials
        payload = user['payload'].copy()
        payload[field] = data_field
        response = StellarBurgersApi.update_user(payload)
        response_json = response.json()
        assert response.status_code == 401
        assert response_json['success'] is False
        assert response_json['message'] == data.ERROR_MESSAGE_UNAUTHORIZED