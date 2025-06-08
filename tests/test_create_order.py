import allure
import data
from helper import StellarBurgersApi


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Успешное создание заказа авторизованным пользователем с валидными ингредиентами")
    def test_create_order_with_authorization_and_valid_ingredients_returns_success(self, register_new_user_and_return_credentials, make_order_body_ingredients):
        user = register_new_user_and_return_credentials
        token = user['access_token']
        headers = StellarBurgersApi.auth_headers(token)
        payload = make_order_body_ingredients
        response = StellarBurgersApi.create_order(payload, headers=headers)
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        json_response = response.json()
        assert json_response.get(
            'success') is True, f"Expected 'success' to be True, but got {json_response.get('success')}"
        assert 'order' in json_response, "Response JSON should contain 'order'"
        assert 'number' in json_response['order'], "Order should contain 'number'"

    @allure.title("Успешное создание заказа неавторизованным пользователем с валидными ингредиентами")
    def test_create_order_without_authorization_with_valid_ingredients_returns_success(self, make_order_body_ingredients):
        payload = make_order_body_ingredients
        response = StellarBurgersApi.create_order(payload)
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        json_response = response.json()
        assert json_response.get(
            'success') is True, f"Expected 'success' to be True, but got {json_response.get('success')}"
        assert 'order' in json_response, "Response JSON should contain 'order'"
        assert 'number' in json_response['order'], "Order should contain 'number'"


    @allure.title("Создание заказа без ингредиентов возвращает ошибку 400")
    def test_create_order_without_ingredients_returns_400_error(self):

        payload = {}
        response = StellarBurgersApi.create_order(payload)
        assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
        json_response = response.json()
        assert json_response.get(
            'success') is False, f"Expected 'success' to be False, but got {json_response.get('success')}"
        expected_message = data.ERROR_MESSAGE_INGREDIENTS_REQUIRED
        actual_message = json_response.get('message')
        assert actual_message == expected_message, \
            f"Expected message '{expected_message}', but got '{actual_message}'"


    @allure.title("Создание заказа с невалидными ингредиентами возвращает ошибку 500")
    def test_create_order_with_invalid_ingredients_returns_500_error(self):
        payload = {
            "ingredients": [
                "fakeidingredient",
                "anotherfakeid"
            ]
        }
        response = StellarBurgersApi.create_order(payload)
        assert response.status_code == 500, f"Expected status code 500, but got {response.status_code}"
