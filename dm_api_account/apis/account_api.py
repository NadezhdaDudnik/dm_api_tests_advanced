import requests

from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self,
            json_data
    ):
        """
        /v1/account
        Register new user
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=json_data
        )
        return response

    def get_v1_account(
            self,
            **kwargs
    ):
        """
        /v1/account
        Get current user
        :return:
        """
        response = self.get(
            path=f'/v1/account',
            **kwargs
        )
        return response

    def put_v1_account_token(
            self,
            token
    ):
        """
        /v1/account/{token}
        Activate registered user
        :param token:
        :return:
        """
        headers = {
            'accept': 'text/plain',
        }
        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        return response

    def put_v1_account_change_email(
            self,
            json_data,
            **kwargs
    ):
        """
        /v1/account/email
        Change registered user email
        :param json_data:
        :return:
        """

        response = self.put(
            path=f'/v1/account/email',
            json=json_data,
            **kwargs
        )
        return response

    def post_v1_account_password(
            self,
            json_data,
            **kwargs
    ):
        """
        /v1/account/password
        Reset registered user password
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account/password',
            json=json_data,
            **kwargs
        )
        return response

    def put_v1_account_change_password(
            self,
            json_data,
            **kwargs
    ):
        """
        /v1/account/password
        Change registered user password
        :param json_data:
        :return:
        """
        response = self.put(
            path=f'/v1/account/password',
            json=json_data,
            **kwargs
        )
        return response

    def delete_v1_account_login(self, **kwargs):
        """
                /v1/account/login
                Logout as current user
                :return:
                """
        response = self.delete(
            path=f'/v1/account/login',
            **kwargs
        )
        return response

    def delete_v1_account_login_all(self, **kwargs):
        """
                /v1/account/login/all
                Logout from every device
                :return:
                """
        response = self.delete(
            path=f'/v1/account/login/all',
            **kwargs
        )
        return response