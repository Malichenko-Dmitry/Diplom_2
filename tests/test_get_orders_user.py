import allure
import data
from helper import StellarBurgersApi


@allure.feature("Получение заказов пользователя")
class TestGetUserOrders:

    @allure.title("Возможность получения списка заказов авторизованным пользователем")
    def test_get_orders_with_authorization_returns_user_orders(self, register_new_user_and_return_credentials, make_order_body_ingredients):
        user = register_new_user_and_return_credentials
        token = user['access_token']
        headers = StellarBurgersApi.auth_headers(token)
        payload = make_order_body_ingredients
        create_response = StellarBurgersApi.create_order(payload, headers)
        assert create_response.status_code == 200, "Ошибка при создании заказа"
        response = StellarBurgersApi.get_order_user(headers)
        assert response.status_code == 200, "Некорректный статус ответа"
        response_json = response.json()
        assert response_json['success'] is True, "Ответ не содержит success=True"
        orders = response_json.get('orders', [])
        assert any(order['ingredients'] == payload['ingredients'] for order in orders), \
            "Созданный заказ не найден в списке заказов"


    @allure.title("Невозможность получения заказа неавторизованным пользователем")
    def test_get_orders_without_authorization_fails_with_401(self):

        response = StellarBurgersApi.get_order_user()
        assert response.status_code == 401, "Ожидался статус 401 для неавторизованного доступа"
        response_json = response.json()
        assert response_json['success'] is False, "Ответ должен содержать success=False"
        assert response_json['message'] == data.ERROR_MESSAGE_UNAUTHORIZED, \
            "Сообщение об ошибке не совпадает с ожидаемым"