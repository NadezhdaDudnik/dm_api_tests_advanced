import allure


@allure.suite("Account Management")
@allure.epic("User Authentication")
@allure.feature("Login Functionality")
@allure.story("POST /v1/account/login")
@allure.sub_suite("Positive Tests")
class TestsPostV1AccountLogin:
    @allure.title("Successful User Login")
    def test_post_v1_account_login(
            self,
            account_helper,
            prepare_user
    ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(login=login, password=password, email=email)

        account_helper.user_login(login=login, password=password)
