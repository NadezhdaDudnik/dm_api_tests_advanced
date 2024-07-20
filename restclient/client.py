import uuid
from json import JSONDecodeError
from requests import session
import structlog
import curlify
from restclient.configuration import Configuration
from restclient.utilities import (
    mask_sensitive_data,
    mask_curl_command,
    allure_attach,
)


class RestClient:
    def __init__(self, configuration: Configuration):
        self.host = configuration.host
        self.session = session()
        self.set_headers(configuration.headers)
        self.disable_log = configuration.disable_log
        self.log = structlog.get_logger(__name__).bind(service='api')

    def set_headers(self, headers):
        if headers:
            self.session.headers.update(headers)

    @allure_attach
    def post(self, path, **kwargs):
        return self._send_request('POST', path, **kwargs)

    @allure_attach
    def get(self, path, **kwargs):
        return self._send_request('GET', path, **kwargs)

    @allure_attach
    def put(self, path, **kwargs):
        return self._send_request('PUT', path, **kwargs)

    @allure_attach
    def delete(self, path, **kwargs):
        return self._send_request('DELETE', path, **kwargs)

    def _send_request(self, method, path, **kwargs):
        log = self.log.bind(event_id=str(uuid.uuid4()))
        full_url = self.host + path
        keys_to_mask = ['password', 'login', 'token', 'access_token', 'authorization', 'X-Dm-Auth-Token']

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
        masked_curl = mask_curl_command(curl, keys_to_mask)
        print(masked_curl)

        log.msg(
            event='Response',
            status_code=rest_response.status_code,
            headers={k: (v if k not in keys_to_mask else '*****') for k, v in rest_response.headers.items()},
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
