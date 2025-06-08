user_email = "example_user@gmail.com"
user_password = "SecurePass123!"
user_name = "John Doe"


USER_CREDENTIALS_WITHOUT_EMAIL = {
    "email": "",
    "password": user_password,
    "name": user_name
}

USER_CREDENTIALS_WITHOUT_PASSWORD = {
    "email": user_email,
    "password": "",
    "name": user_name
}

USER_CREDENTIALS_WITHOUT_NAME = {
    "email": user_email,
    "password": user_password,
    "name": ""
}


ERROR_MESSAGE_USER_ALREADY_EXISTS = "User already exists"
ERROR_MESSAGE_REQUIRED_FIELDS = "Email, password and name are required fields"
ERROR_MESSAGE_INVALID_CREDENTIALS = "email or password are incorrect"
ERROR_MESSAGE_UNAUTHORIZED = "You should be authorised"
ERROR_MESSAGE_INGREDIENTS_REQUIRED = "Ingredient ids must be provided"