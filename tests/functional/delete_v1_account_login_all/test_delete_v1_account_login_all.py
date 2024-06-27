def test_delete_v1_account_login_all(account_helper, prepare_user, auth_account_helper):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)

    account_helper.user_login(login=login, password=password)

    auth_account_helper.logout_user_all_devices()
