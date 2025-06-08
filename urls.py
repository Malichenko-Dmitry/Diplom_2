class URL:
    BASE_URL = 'https://stellarburgers.nomoreparties.site'

    CREATE_USER = f'{BASE_URL}/api/auth/register'
    GET_INGREDIENTS = f'{BASE_URL}/api/ingredients'
    LOGIN_USER = f'{BASE_URL}/api/auth/login'
    CHANGE_USER = f'{BASE_URL}/api/auth/user'
    CREATE_ORDER = f'{BASE_URL}/api/orders'
    RECEIVE_ORDER = f'{BASE_URL}/api/orders'