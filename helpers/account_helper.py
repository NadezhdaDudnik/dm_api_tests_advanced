import json
import re
import time
from json import loads

import allure
import curlify

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from restclient.utilities import allure_attach
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
            dm_account_api,
            mailhog
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(
            self,
            login,
            password
    ):
        response = self.user_login(login=login, password=password)
        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)
        return response

    def register_new_user(
            self,
            login,
            password,
            email,
            validate_response=False
    ):
        with allure.step("Регистрация нового пользователя"):
            registration = Registration(login=login, email=email, password=password)
            self.dm_account_api.account_api.post_v1_account(registration=registration)

        token = self.get_token(login=login, token_type="activation")
        assert token is not None, f"Токен для пользователя {login} не получен"

        with allure.step("Активация пользователя"):
            response = self.dm_account_api.account_api.put_v1_account_token(
                token=token, validate_response=validate_response
            )
        return response

    def user_login(
            self,
            login,
            password,
            remember_me=True,
            validate_response=False,
            validate_headers=False
    ):
        with allure.step("Аутентификация пользователя"):
            login_credentials = LoginCredentials(login=login, password=password, remember_me=remember_me)
            response = self.dm_account_api.login_api.post_v1_account_login(
                login_credentials=login_credentials, validate_response=validate_response
            )
            if validate_headers:
                assert response.headers["x-dm-auth-token"], "Токен для пользователя не был получен"
            return response

    def change_email(
            self,
            login,
            password,
            email,
            validate_response=False
    ):
        with allure.step("Изменение Email пользователя"):
            change_email = ChangeEmail(login=login, email=email, password=password)
            self.dm_account_api.account_api.put_v1_account_change_email(
                change_email=change_email, validate_response=validate_response
            )
            token = self.get_activation_token_by_login_after_change_email(email)
            assert token is not None, f"Токен для пользователя c {email} не получен"
            self.dm_account_api.account_api.put_v1_account_token(token=token, validate_response=validate_response)

    def change_password(
            self,
            login,
            email,
            old_password,
            new_password,
            validate_response=False
    ):
        with allure.step("Сброс и изменение пароля пользователя"):
            token = self.user_login(login=login, password=old_password)
            reset_password = ResetPassword(login=login, email=email)
            headers = {
                "x-dm-auth-token": token.headers["x-dm-auth-token"]
            }
            self.dm_account_api.account_api.post_v1_account_password(reset_password=reset_password, headers=headers)
            token = self.get_token(login=login, token_type="reset")
            change_password = ChangePassword(login=login, email=email, old_password=old_password, new_password=new_password)
            self.dm_account_api.account_api.put_v1_account_change_password(change_password=change_password)

    def logout_user(
            self
    ):
        with allure.step("Выход из системы пользователя"):
            self.dm_account_api.login_api.delete_v1_account_login()

    def logout_user_all_devices(
            self
    ):
        with allure.step("Выход из всех устройств пользователя"):
            self.dm_account_api.login_api.delete_v1_account_login_all()

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(
            self,
            login
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

    @retry(stop_max_attempt_number=10, retry_on_result=retry_if_result_none, wait_fixed=2000)
    def get_activation_token_by_login_after_change_email(
            self,
            change_email
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

        with allure.step("Получение токена из почтовых сообщений"):
            for item in response.json()["items"]:
                user_data = loads(item["Content"]["Body"])
                user_login = user_data["Login"]
                activation_token = user_data.get("ConfirmationLinkUrl")
                reset_token = user_data.get("ConfirmationLinkUri")

                if user_login == login:
                    if token_type == "activation" and activation_token:
                        token = activation_token.split("/")[-1]
                    elif token_type == "reset" and reset_token:
                        token = reset_token.split("/")[-1]

                    if token:
                        masked_token = token[:4] + "****" + token[-4:]  # Маскировка токена
                        allure.attach(
                            f"Полученный токен: {masked_token}", name="Token",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        break

        return token
