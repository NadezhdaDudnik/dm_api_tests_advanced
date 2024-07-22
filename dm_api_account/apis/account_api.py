import allure
import requests

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient
from restclient.utilities import allure_attach


class AccountApi(RestClient):

    def post_v1_account(self, registration: Registration):
        with allure.step("Зарегистрировать нового пользователя"):
            allure_attach(registration)
            response = self.post(
                path='/v1/account',
                json=registration.model_dump(exclude_none=True, by_alias=True)
            )
            return response

    def get_v1_account(self, validate_response=True, **kwargs):
        with allure.step("Получить информацию по пользователю"):
            response = self.get(
                path='/v1/account',
                **kwargs
            )
            if validate_response:
                return UserDetailsEnvelope(**response.json())
            return response

    def put_v1_account_token(self, token, validate_response=True):
        with allure.step("Активировать пользователя"):
            headers = {
                'accept': 'text/plain',
            }
            response = self.put(
                path=f'/v1/account/{token}',
                headers=headers
            )
            if validate_response:
                return UserEnvelope(**response.json())
            return response

    def put_v1_account_change_email(self, change_email: ChangeEmail, validate_response=True, **kwargs):
        with allure.step("Изменить адрес электронной почты пользователя"):
            allure_attach(change_email)
            response = self.put(
                path='/v1/account/email',
                json=change_email.model_dump(exclude_none=True, by_alias=True),
                **kwargs
            )
            if validate_response:
                return UserEnvelope(**response.json())
            return response

    def post_v1_account_password(self, reset_password: ResetPassword, validate_response=False, **kwargs):
        with allure.step("Сбросить пароль пользователя"):
            allure_attach(reset_password)
            response = self.post(
                path='/v1/account/password',
                json=reset_password.model_dump(exclude_none=True, by_alias=True),
                **kwargs
            )
            if validate_response:
                return UserEnvelope(**response.json())
            return response

    def put_v1_account_change_password(self, change_password: ChangePassword, validate_response=False, **kwargs):
        with allure.step("Изменить пароль пользователя"):
            allure_attach(change_password)
            response = self.put(
                path='/v1/account/password',
                json=change_password.model_dump(exclude_none=True, by_alias=True),
                **kwargs
            )
            if validate_response:
                return UserEnvelope(**response.json())
            return response
