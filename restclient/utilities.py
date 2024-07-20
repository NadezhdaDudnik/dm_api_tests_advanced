import json
import allure
import curlify
import re

# Function to mask sensitive data
def mask_sensitive_data(data, keys_to_mask):
    if not data:
        return data
    if isinstance(data, dict):
        return {k: (mask_sensitive_data(v, keys_to_mask) if k not in keys_to_mask else '*****') for k, v in data.items()}
    return data

# Function to mask sensitive data in curl commands
def mask_curl_command(curl_command, keys_to_mask):
    for key in keys_to_mask:
        curl_command = re.sub(rf'("{key}": ")([^"]+)', rf'\1*****', curl_command)
        curl_command = re.sub(rf"('{key}': ')([^']+)", rf'\1*****', curl_command)
        curl_command = re.sub(rf'({key}=)([^&]+)', rf'\1*****', curl_command)
    return curl_command

# Decorator for attaching requests and responses to Allure reports with masking
def allure_attach(fn):
    def wrapper(*args, **kwargs):
        keys_to_mask = ['password', 'login', 'token', 'access_token', 'authorization', 'X-Dm-Auth-Token']

        # Mask the request body
        body = kwargs.get("json")
        if body:
            masked_body = mask_sensitive_data(body, keys_to_mask)
            allure.attach(
                json.dumps(masked_body, indent=4),
                name="request_body",
                attachment_type=allure.attachment_type.JSON,
            )

        response = fn(*args, **kwargs)

        # Mask the curl command
        curl = curlify.to_curl(response.request)
        masked_curl = mask_curl_command(curl, keys_to_mask)
        allure.attach(masked_curl, name="curl", attachment_type=allure.attachment_type.TEXT)

        try:
            response_json = response.json()
        except json.decoder.JSONDecodeError:
            response_text = response.text
            status_code = f"status_code = {response.status_code}"
            allure.attach(
                response_text if len(response_text) > 0 else status_code,
                name="response_body",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            masked_response_json = mask_sensitive_data(response_json, keys_to_mask)
            allure.attach(
                json.dumps(masked_response_json, indent=4),
                name="response_body",
                attachment_type=allure.attachment_type.JSON,
            )
        return response
    return wrapper
