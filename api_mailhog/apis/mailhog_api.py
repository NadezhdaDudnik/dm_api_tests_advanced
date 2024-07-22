import allure
import requests

from restclient.client import RestClient
from restclient.utilities import allure_attach


class MailhogApi(RestClient):

    def get_api_v2_messages(self, limit=50):
        with allure.step("Получить все письма"):
            params = {'limit': limit}
            response = self.get(
                path='/api/v2/messages',
                params=params,
                verify=False
            )
            allure_attach(response)  # Attach response to allure report
            return response
