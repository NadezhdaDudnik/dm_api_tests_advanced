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
        # Регистрация пользователя
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"Пользователь не создан {response.json()}"

        # Получение активационного токена
        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f"Токен для пользователя {login} не получен"

        # Активация пользователя
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не активирован"
        return response

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):
        # Авторизация пользователя

        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }

        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, "Пользователь не авторизован"
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

        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f"Токен для пользователя {login} не получен"

    def user_login_403(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):
        # Авторизация пользователя

        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }

        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 403, "Пользователь авторизован ошибочно"
        return response

    def activation_user_after_change_email(
            self,
            email: str
    ):

        # Получение активационного токена

        token = self.get_activation_token_by_login_after_change_email(email)
        assert token is not None, f"Токен для пользователя c {email} не получен"

        # Активация пользователя

        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не активирован"

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(
            self,
            login,
    ):
        token = None
        # Получение письма из почтового сервера
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
