import allure

@allure.suite("Account Management")
@allure.epic("User Change Email")
@allure.feature("Change Email Functionality")
@allure.story("PUT v1/account/email")
@allure.sub_suite("Positive Tests")

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

        account_helper.change_email(login=login, password=password, email=change_email, validate_response=False)

