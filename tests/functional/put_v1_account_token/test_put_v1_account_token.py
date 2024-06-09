from json import loads

from api_mailhog.apis.mailhog_api import MailhogApi
from dm_api_account_adv.apis.account_api import AccountApi


def test_put_v1_account_token():
    account_api = AccountApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    login = 'Nadin7'
    password = '123456789'

    # Получение письма из почтового сервера

    response = mailhog_api.get_api_v2_messages()
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не получены"

    # Получение активационного токена
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Токен для пользователя {login} не получен"

    # Активация пользователя

    response = account_api.put_v1_account_token(token=token)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не активирован"


def get_activation_token_by_login(
        login,
        response
):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            print(user_login)
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(token)
    return token
