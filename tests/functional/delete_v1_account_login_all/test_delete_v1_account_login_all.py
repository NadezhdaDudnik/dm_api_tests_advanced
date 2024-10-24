import allure


@allure.suite("Account Management")
@allure.epic("User Logaut all devices")
@allure.feature("Logaut Functionality")
@allure.story("DELETE /v1/account/login/all")
@allure.sub_suite("Positive Tests")
class TestsDeleteV1AccountLoginAll:
    @allure.title("Проверка выхода пользователя из системы из всех устройств")

    def test_delete_v1_account_login_all(self, account_helper, prepare_user):
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

        account_helper.logout_user_all_devices()
