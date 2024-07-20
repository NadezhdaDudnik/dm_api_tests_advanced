from json import JSONDecodeError
from requests import session, HTTPError, exceptions
import structlog
import uuid
import curlify
from restclient.configuration import Configuration
from restclient.utilities import allure_attach


def mask_sensitive_data(data, keys_to_mask):
    """Функция для маскировки чувствительных данных."""
    if not data:
        return data
    if isinstance(data, dict):
        return {k: (mask_sensitive_data(v, keys_to_mask) if k not in keys_to_mask else '*****') for k, v in data.items()}
    return data

class RestClient:
    def __init__(self, configuration: Configuration):
        self.host = configuration.host
        self.set_headers(configuration.headers)
        self.disable_log = configuration.disable_log
        self.session = session()
        self.log = structlog.get_logger(__name__).bind(service='api')

    def set_headers(self, headers):
        if headers:
            self.session.headers.update(headers)

    def post(self, path, **kwargs):
        return self._send_request(method='POST', path=path, **kwargs)

    def get(self, path, **kwargs):
        return self._send_request(method='GET', path=path, **kwargs)

    def put(self, path, **kwargs):
        return self._send_request(method='PUT', path=path, **kwargs)

    def delete(self, path, **kwargs):
        return self._send_request(method='DELETE', path=path, **kwargs)

    @allure_attach
    def _send_request(self, method, path, **kwargs):
        log = self.log.bind(event_id=str(uuid.uuid4()))
        full_url = self.host + path

        # Определяем ключи, которые нужно маскировать
        keys_to_mask = ['password', 'login']

        if self.disable_log:
            rest_response = self.session.request(method=method, url=full_url, **kwargs)
            rest_response.raise_for_status()
            return rest_response

        masked_params = mask_sensitive_data(kwargs.get('params'), keys_to_mask)
        masked_headers = mask_sensitive_data(kwargs.get('headers'), keys_to_mask)
        masked_json = mask_sensitive_data(kwargs.get('json'), keys_to_mask)
        masked_data = mask_sensitive_data(kwargs.get('data'), keys_to_mask)

        log.msg(
            event='Request',
            method=method,
            full_url=full_url,
            params=masked_params,
            headers=masked_headers,
            json=masked_json,
            data=masked_data
        )

        rest_response = self.session.request(method=method, url=full_url, **kwargs)
        curl = curlify.to_curl(rest_response.request)
        print(curl)

        log.msg(
            event='Response',
            status_code=rest_response.status_code,
            headers=rest_response.headers,
            json=self._get_json(rest_response),
        )
        rest_response.raise_for_status()
        return rest_response

    @staticmethod
    def _get_json(rest_response):
        try:
            return rest_response.json()
        except JSONDecodeError:
            return {}
