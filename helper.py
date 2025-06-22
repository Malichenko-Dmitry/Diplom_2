from faker import Faker
import allure
import requests
from urls import URL
import time

fake = Faker(locale="ru_RU")

class Helper:

    @staticmethod
    def generate_unique_email():
        timestamp = int(time.time() * 1000)
        return f"{fake.first_name().lower()}.{timestamp}@example.com"

    @staticmethod
    def generate_credentials_user():
        return {
            "email": Helper.generate_unique_email(),
            "password": fake.password(),
            "name": fake.first_name()
        }


class StellarBurgersApi:

    @staticmethod
    def auth_headers(token):
        return {"Authorization": token}

    @staticmethod
    @allure.step("Создание пользователя")
    def create_user(body):
        return requests.post(URL.CREATE_USER, json=body)

    @staticmethod
    @allure.step("Удаление пользователя")
    def delete_user(headers):
        return requests.delete(URL.CHANGE_USER, headers=headers)

    @staticmethod
    @allure.step("Логин пользователя")
    def login_user(body):
        return requests.post(URL.LOGIN_USER, json=body)

    @staticmethod
    @allure.step("Обновление данных пользователя")
    def update_user(body, headers=None):
        if headers is None:
            headers = {}
        return requests.patch(URL.CHANGE_USER, json=body, headers=headers)

    @staticmethod
    @allure.step("Создание заказа")
    def create_order(body, headers=None):
        if headers is None:
            headers = {}
        return requests.post(URL.CREATE_ORDER, json=body, headers=headers)


    @staticmethod
    @allure.step("Получение заказов пользователя")
    def get_order_user(headers=None):
        if headers is None:
            headers = {}
        return requests.get(URL.CREATE_ORDER, headers=headers)

    @staticmethod
    @allure.step("Получение списка ингредиентов")
    def get_ingredients():
        return requests.get(URL.GET_INGREDIENTS)