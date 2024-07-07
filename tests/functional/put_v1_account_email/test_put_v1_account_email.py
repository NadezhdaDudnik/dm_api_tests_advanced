import allure


@allure.suite("Тесты на проверку метода PUT v1/account/email")
@allure.sub_suite("Позитивные тесты")
class TestsPostV1AccountEmail:
    @allure.title("Проверка смены Email пользователя")
    def test_put_v1_account_email(
            self,
            account_helper,
            prepare_user
    ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        change_email = prepare_user.change_email

        account_helper.register_new_user(login=login, password=password, email=email)

        account_helper.auth_client(
            login=login,
            password=password
        )

        account_helper.change_email(login=login, password=password, email=change_email)

