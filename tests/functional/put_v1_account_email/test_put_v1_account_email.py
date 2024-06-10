from json import loads

from dm_api_account_adv.apis.account_api import AccountApi
from dm_api_account_adv.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi


def test_put_v1_account_email():
    # Регистрация пользователя
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    login = 'Nadin36'
    password = '123456789'
    email = f'{login}@mail.ru'
    change_email = f'{login}01@mail.ru'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f"Пользователь не создан {response.json()}"

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

    # Авторизация пользователя

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не авторизован"

    # Смена пароля

    json_data = {
        'login': login,
        'email': change_email,
        'password': password,
    }
    response = account_api.put_v1_account_change_email(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Адрес электронной почты пользователя не изменен"

    # Повторная Авторизация пользователя после смены почты и без активации токена

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 403, "Пользователь авторизован ошибочно"

    # Получение письма из почтового сервера после смены адреса электронной почты

    response = mailhog_api.get_api_v2_messages()
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не получены"

    # Получение активационного токена

    token = get_activation_token_by_login_after_change_email(change_email, response)
    assert token is not None, f"Токен для пользователя c {change_email} не получен"

    # Активация пользователя

    response = account_api.put_v1_account_token(token=token)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не активирован"

    # Повторная Авторизация пользователя

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не авторизован"


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


def get_activation_token_by_login_after_change_email(
        change_email,
        response
):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_email = item['Content']['Headers']['To'][0]

        if user_email == change_email:
            print(user_email)
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(token)
    return token