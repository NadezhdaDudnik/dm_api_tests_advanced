import allure

from checkers.http_checkers import check_status_code_http
from checkers.get_v1_account import GetV1Account
@allure.suite("Account Management")
@allure.epic("GET User")
@allure.feature("Get User Functionality")
@allure.story("GET /v1/account")
@allure.sub_suite("Positive Tests")
class TestsGetV1AccountAuth:
    @allure.title("Проверка получения аутентифицированного пользователя")

    def test_get_v1_account_auth(
            self,
            account_helper,
            prepare_user
    ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(
            login=login,
            password=password,
            email=email
        )

        account_helper.auth_client(
            login=login,
            password=password
        )
        response = account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
        # with check_status_code_http():
        #     response = account_helper.dm_account_api.account_api.get_v1_account()
        #     GetV1Account.check_response_values(response)

class TestsGetV1AccountNoAuth:
    @allure.title("Проверка получения неаутентифицированного пользователя")


    def test_get_v1_account_no_auth(
            self,
            auth_account_helper
    ):

        with check_status_code_http(401, 'User must be authenticated'):
            auth_account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
