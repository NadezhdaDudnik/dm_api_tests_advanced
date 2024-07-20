import allure
import pytest

from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account


@allure.suite("Тесты на проверку метода POST v1/account")
@allure.sub_suite("Позитивные тесты")
class TestsPostV1Account:
    @allure.title("Проверка регистрации нового пользователя")
    def test_post_v1_account(
            self,
            account_helper,
            prepare_user
    ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(login=login, password=password, email=email)

        response = account_helper.user_login(login=login, password=password, validate_response=True)

        PostV1Account.check_response_values(response)


@pytest.mark.parametrize(
    'login, email, password', [
        ('login_47', 'login_47233@mail.ru', 'login'),
        ('login789', 'login_47222mail.ru', 'login_55'),
        ('l', 'login47222@mail.ru', 'login_55')
    ]
)
@allure.sub_suite("Негативные тесты")
class TestsNegativePostV1Account:
    @allure.title("Проверка 400 статус кода")
    def test_post_v1_account_negative(
            self,
            login,
            email,
            password,
            account_helper
    ):
        with check_status_code_http(400, "Validation failed"):
            account_helper.register_new_user(login=login, password=password, email=email)
