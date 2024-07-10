def test_put_v1_account_password(
        account_helper,
        prepare_user,
        auth_account_helper
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    change_password = prepare_user.change_password

    account_helper.register_new_user(login=login, password=password, email=email)

    account_helper.user_login(login=login, password=password)

    account_helper.change_password(login=login, email=email, old_password=password, new_password=change_password, validate_response=False)

    account_helper.user_login(login=login, password=change_password)
