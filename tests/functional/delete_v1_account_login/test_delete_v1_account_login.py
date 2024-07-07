import allure


@allure.suite("Тесты на проверку метода DELETE v1/account/login")
@allure.sub_suite("Позитивные тесты")
class TestsDeleteV1AccountLogin:
    @allure.title("Проверка выхода пользователя из системы")
    def test_delete_v1_account_login(
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
            email=email)

        account_helper.auth_client(
            login=login,
            password=password
        )

        account_helper.logout_user()
