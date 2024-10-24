import allure

@allure.suite("Account Management")
@allure.epic("Activation Token")
@allure.feature("Token Functionality")
@allure.story("PUT v1/account/token")
@allure.sub_suite("Positive Tests")

class TestsPostV1Account:
    @allure.title("Проверка активации токена для пользователя")
    def test_put_v1_account_token(
            self,
            account_helper,
            prepare_user
            ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(login=login, password=password, email=email)
