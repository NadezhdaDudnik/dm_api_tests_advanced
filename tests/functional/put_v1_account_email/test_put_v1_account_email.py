
def test_put_v1_account_email(
        account_helper,
        prepare_user,
        auth_account_helper
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    change_email = prepare_user.change_email

    account_helper.register_new_user(login=login, password=password, email=email)

    account_helper.user_login(login=login, password=password)

    auth_account_helper.change_email(login=login, password=password, email=change_email)

