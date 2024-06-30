import time
from json import loads

from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount
from retrying import retry


def retry_if_result_none(
        result
):
    return result is None


def retrier(
        function
):
    def wrapper(
            *args,
            **kwargs
    ):
        token = None
        count = 0
        while token is None:
            print(f"Попытка получения токена номер {count}!")
            token = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError("Превышено количество попыток получения активационного токена!")
            if token:
                return token
            time.sleep(1)

    return wrapper


class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(
            self,
            login: str,
            password: str
    ):
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data={
                'login': login,
                'password': password
            }
        )
        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }

        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"Пользователь не создан {response.json()}"

        #token = self.get_activation_token_by_login(login=login)
        token = self.get_token(login=login, token_type="activation")
    
        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f"Токен для пользователя {login} не получен"


        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не активирован"
        return response

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            expected_status_code=200,
            fail_message="Пользователь не авторизован"
    ):

        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }

        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == expected_status_code, fail_message
        return response

    def change_email(
            self,
            login: str,
            password: str,
            email: str
    ):

        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }

        response = self.dm_account_api.account_api.put_v1_account_change_email(json_data=json_data)
        assert response.status_code == 200, "Адрес электронной почты пользователя не изменен"

        token = self.get_activation_token_by_login_after_change_email(email)
        assert token is not None, f"Токен для пользователя c {email} не получен"

        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не активирован"

    def change_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str
    ):
        token = self.user_login(login=login, password=old_password)
        json_data = {
            'login': login,
            'email': email
        }
        headers = {
            "x-dm-auth-token": token.headers["x-dm-auth-token"]
        }

        self.dm_account_api.account_api.post_v1_account_password(
            json_data=json_data,
            headers=headers
        )

        token = self.get_token(login=login, token_type="reset")
        assert token is not None, f"Авторизационный токен для пользователя не получен"

        json_data1 = {
            'login': login,
            'oldPassword': old_password,
            'newPassword': new_password,
            'token': token,
        }

        response = self.dm_account_api.account_api.put_v1_account_change_password(json_data=json_data1)
        assert response.status_code == 200, "Пароль пользователя не изменен"


    def logout_user(self):
        response = self.dm_account_api.account_api.delete_v1_account_login()
        assert response.status_code == 204, "Пользователь не разлогинен"

    def logout_user_all_devices(self):
        response = self.dm_account_api.account_api.delete_v1_account_login_all()
        assert response.status_code == 204, "Пользователь не разлогинен со всех устройств"

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(
            self,
            login,
    ):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                print(user_login)
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                print(token)
        return token

    # @retrier
    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login_after_change_email(
            self,
            change_email,
    ):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_email = item['Content']['Headers']['To'][0]
            if user_email == change_email:
                print(user_email)
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                print(token)
        return token

    @retry(stop_max_attempt_number=10, retry_on_result=retry_if_result_none, wait_fixed=2000)
    def get_token(
            self,
            login,
            token_type="activation"
    ):
        """
        Получение токена активации или сброса пароля
        Args:
            login: логин пользователя
            token_type: тип токена (activation или reset)
        Returns:
            токен активации или сброса пароля
        """
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()["items"]:
            user_data = loads(item["Content"]["Body"])
            user_login = user_data["Login"]
            activation_token = user_data.get("ConfirmationLinkUrl")
            reset_token = user_data.get("ConfirmationLinkUri")
            if user_login == login and activation_token and token_type == "activation":
                token = activation_token.split("/")[-1]
            elif user_login == login and reset_token and token_type == "reset":
                token = reset_token.split("/")[-1]

        return token
