from json import loads

from dm_api_account_adv.apis.login_api import LoginApi


def test_post_v1_account_login():
    # Авторизация пользователя
    login_api = LoginApi(host='http://5.63.153.31:5051')

    login = 'Nadin4'
    password = '123456789'

    json_data = {
        'login': login,
        'password': password,
    }

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не авторизован"
