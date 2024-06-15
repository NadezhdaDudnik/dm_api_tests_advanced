from json import loads

import structlog
from faker import Faker

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4, ensure_ascii=True
            # sort_keys=True
        )
    ]
)


def test_put_v1_account_email():
    # Регистрация пользователя
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMApiAccount(dm_api_configuration)
    mailhog = MailHogApi(mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    fake = Faker("en_US")
    login = fake.first_name_female() + '12345'
    password = '123456789'
    email = f'{login}@mail.ru'
    change_email = f'{login}@mail.ru'
    account_helper.register_new_user(login=login, password=password, email=email)

    # Авторизация пользователя
    account_helper.user_login(login=login, password=password)

    # Смена пароля

    account_helper.change_email(login=login, password=password, email=change_email)

    # Повторная Авторизация пользователя после смены почты и без активации токена

    account_helper.user_login_403(login=login, password=password)

    account_helper.activation_user_after_change_email(email=change_email)

    # Повторная Авторизация пользователя
    account_helper.user_login(login=login, password=password)
