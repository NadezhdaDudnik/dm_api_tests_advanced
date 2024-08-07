import pytest

from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account


def test_post_v1_account(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)

    response = account_helper.user_login(login=login, password=password, validate_response=True)

    PostV1Account.check_response_values(response)


@pytest.mark.parametrize(
    'login, email, password', [
        ('login_47', 'login_47233@mail.ru', 'login'),
        ('login789', 'login_47222mail.ru', 'login_55'),
        ('l', 'login47222@mail.ru', 'login_55')
    ]
)
def test_post_v1_account_negative(
        login,
        email,
        password,
        account_helper
):
    with check_status_code_http(400, "Validation failed"):
        account_helper.register_new_user(login=login, password=password, email=email)
