import allure
import requests

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient
from restclient.utilities import allure_attach


class LoginApi(RestClient):

    def post_v1_account_login(self, login_credentials: LoginCredentials, validate_response=True):
        with allure.step("Авторизовать пользователя"):
            allure_attach(login_credentials)
            response = self.post(
                path='/v1/account/login',
                json=login_credentials.model_dump(exclude_none=True, by_alias=True)
            )
            if validate_response:
                return UserEnvelope(**response.json())
            return response

    def delete_v1_account_login(self, **kwargs):
        with allure.step("Разлогинить пользователя"):
            response = self.delete(
                path='/v1/account/login',
                **kwargs
            )
            return response

    def delete_v1_account_login_all(self, **kwargs):
        with allure.step("Разлогинить пользователя из всех устройств"):
            response = self.delete(
                path='/v1/account/login/all',
                **kwargs
            )
            return response
