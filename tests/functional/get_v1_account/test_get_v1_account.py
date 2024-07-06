from checkers.http_checkers import check_status_code_http
from checkers.get_v1_account import GetV1Account


def test_get_v1_account_auth(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(
        login=login,
        password=password,
        email=email
    )

    account_helper.auth_client(
        login=login,
        password=password
    )
    with check_status_code_http():
        response = account_helper.dm_account_api.account_api.get_v1_account()
        GetV1Account.check_response_values(response)


def test_get_v1_account_no_auth(
        account_helper
):
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
