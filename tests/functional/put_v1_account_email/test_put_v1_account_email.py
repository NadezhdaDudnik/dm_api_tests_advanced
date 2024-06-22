
def test_put_v1_account_email(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    change_email = prepare_user.change_email

    # Регистрация пользователя
    account_helper.register_new_user(login=login, password=password, email=email)

    # Авторизация пользователя
    account_helper.user_login(login=login, password=password)

    # Смена пароля

    account_helper.change_email(login=login, password=password, email=change_email)

    # Повторная Авторизация пользователя
    account_helper.user_login(login=login, password=password)
